import base64
from io import BytesIO
import re
import uuid
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
import os
from django.views.decorators.csrf import csrf_exempt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import json
import replicate
# load auth token from .env file
from dotenv import load_dotenv
from asgiref.sync import async_to_sync, sync_to_async
from .models import LabelUsage

matplotlib.use('Agg')

load_dotenv()
DEV_MODE = os.environ.get('DEV_MODE') == 'True'
if DEV_MODE:
    print("DEV_MODE=True. Will use local predictor.")
    from model.predict import Predictor

    predictor = Predictor()
    predictor.set_model_dir(os.path.join(settings.BASE_DIR, 'model'))
    predictor.setup()


def success(data):
    return JsonResponse(data, status=200)


def error(data):
    return JsonResponse(data, status=400)


async def save_usage(user_id, label):
    user = await sync_to_async(User.objects.get)(id=user_id)
    await sync_to_async(LabelUsage.objects.create)(user=user, label=label)


@csrf_exempt
def log_usage(request):
    if request.method != 'POST':
        return error({'error': 'This endpoint only supports POST requests.'})

    if not request.user.is_authenticated:
        return error({'error': 'User is not authenticated'})
    
    label = None
    try:
        data = json.loads(request.body.decode('utf-8'))
        label = data.get('label')
    except json.JSONDecodeError:
        return error({'error': 'Invalid JSON'})
    
    if label is not None:
        try:
            print('Saving usage data:', request.user.id, label)
            async_to_sync(save_usage)(request.user.id, label)
        except Exception as e:
            print('Failed to save usage data:', str(e))
            return error({'error': str(e)})
    
    return success({'status': 'success'})


@csrf_exempt
def analyze(request):
    print("Running prediction...")
    if request.method != 'POST':
        return error({'error': 'This endpoint only supports POST requests.'})

    try:
        data = json.loads(request.body.decode('utf-8'))
        input_data = data.get('data')  # 这里是一个包含64个列表的列表，每个子列表有795个浮点数
        user_time = data.get('time')
        user_name = data.get('UserName')
    except json.JSONDecodeError:
        return error({'error': 'Invalid JSON'})

    if input_data is None:
        return error({'error': 'No data provided'})

    label = predict(input_data)

    if request.user.is_authenticated:
        try:
            print('Saving usage data:', request.user.id, label)
            async_to_sync(save_usage)(request.user.id, label)
        except Exception as e:
            print('Failed to save usage data:', str(e))

    return success(data={
        'label': label,
        'time': user_time,
        'UserName': user_name
    })


def predict(eeg_data) -> int:
    if DEV_MODE:
        return predictor.predict_local(eeg_data)
    # generate file name based on the hash of the data
    file_name = str(uuid.uuid4()) + "-" + str(hash(str(eeg_data))) + '.json'
    json_data = {
        "data": eeg_data
    }
    # save to a temp file
    try:
        with open(file_name, 'w') as f:
            json.dump(json_data, f)
        with open(file_name, 'rb') as f:
            output = replicate.run(
                "fanyi-zhao/bci-backend:977ca5966281eeaf1cd7ee40950cafd38cd855cecc6678e71caefdf452d24a42",
                input={"eeg_data": f},
            )
        return int(output)
    finally:
        os.remove(file_name)


@csrf_exempt
def get_user_emails(request):
    if request.method == 'GET':
        users = User.objects.filter(email__isnull=False).exclude(email__exact='')
        emails = [user.email for user in users]
        return success({'emails': emails})
    else:
        return error({'error': 'This endpoint only supports GET requests.'})


def plot_data_and_get_image_base64(data):
    plt.hist(data, bins=30)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


@csrf_exempt
def send_email_notifications(request):
    if request.method != 'GET' and request.method != 'POST':
        return error({'error': 'This endpoint only supports GET and POST requests.'})
    try:
        subject = 'Test Email'
        html = f"""
        <html>
            <body>
            <h1>Welcome to our newsletter!</h1>
            <p>Here's some interesting data we've collected:</p>
            <!-- Insert histogram here -->
            <img src="data:image/png;base64,{plot_data_and_get_image_base64(np.random.randn(1000))}" alt="Histogram" />
            </body>
        </html>
        """
        from_email = 'cs555team11@gmail.com'
        recipient_list = list(
            User.objects.filter(email__isnull=False).exclude(email__exact='').values_list('email', flat=True))
    except Exception:
        return error({'error': 'Failed to generate email content'})

    # 发送邮件
    for recipient in recipient_list:
        try:
            print('Sending email to', recipient)
            send_mail(subject, "", from_email, [recipient], fail_silently=False, html_message=html)
        except Exception as e:
            print('Failed to send email to', recipient, 'with error:', str(e))
    return success({'status': 'success', 'message': 'Mail sent successfully'})


USER_PASSWORD_RULE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
USER_EMAIL_RULE = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('user')
            password = data.get('password')
            email = data.get('email')
            username = username.strip()
            password = password.strip()
            email = email.strip()

            # 檢查密碼複雜度
            if not USER_PASSWORD_RULE.match(password):
                return error({'response': False, 'reason': 'Password complexity requirement not met'})

            if not USER_EMAIL_RULE.match(email):
                return error({'response': False, 'reason': 'Invalid email address'})

            # 檢查用戶名是否已存在
            if User.objects.filter(username=username).exists():
                return error({'response': False, 'reason': 'Username already exists'})

            # 創建用戶
            User.objects.create_user(username=username, password=password, email=email)
            return success({'response': True})
        except Exception:
            return error({'response': False, 'reason': 'Registration failed'})


@csrf_exempt
def get_user_info(request):
    if not request.user.is_authenticated:
        return error({'response': False, 'reason': 'Not logged in'})
    user = User.objects.get(id=request.user.id)
    # return JsonResponse({'response': True, 'email': user.email})
    return success({'response': True, 'email': user.email})


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return error({'response': False, 'reason': 'login failed'})

    data = json.loads(request.body.decode('utf-8'))
    username = data.get('user')
    password = data.get('password')

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        # if user is the same: update session expiry time
        if user.username == username:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return success(
                {'response': True, 'reason': 'Already logged in', 'session_key': request.session.session_key})
        # if user is not the same: logout
        else:
            print('Logging out user', user.username)
            logout(request)

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        request.session['user_id'] = user.id
        return success({'response': True, 'reason': 'login success', 'session_key': request.session.session_key})
    return error({'response': False, 'reason': 'login failed'})


@csrf_exempt
def health(request):
    return success({'status': 'ok'})
