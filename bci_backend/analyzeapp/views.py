import re
import uuid
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import os
from django.views.decorators.csrf import csrf_exempt

import json
import replicate
# load auth token from .env file
from dotenv import load_dotenv
load_dotenv()
DEV_MODE = os.environ.get('DEV_MODE') == 'True'
if DEV_MODE:
    print("DEV_MODE=True. Will use local predictor.")
    from model.predict import Predictor
    predictor = Predictor()
    predictor.set_model_dir(os.path.join(settings.BASE_DIR, 'model'))
    predictor.setup()

@csrf_exempt
def analyze(request):
    print("Running prediction...")
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            input_data = data.get('data')  # 这里是一个包含64个列表的列表，每个子列表有795个浮点数
            user_time = data.get('time')
            user_name = data.get('UserName')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if input_data is None:
            return JsonResponse({'error': 'No data provided'}, status=400)

        response = {
            'label': predict(input_data),
            'time': user_time,
            'UserName': user_name
        }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'This endpoint only supports POST requests.'})

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
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('user')
            password = data.get('password')

            # 檢查密碼複雜度
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
                return JsonResponse({'response': False, 'reason': 'Password complexity requirement not met'})

            # 檢查用戶名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'response': False, 'reason': 'Username already exists'})
            
            # 創建用戶
            User.objects.create_user(username=username, password=password)
            return JsonResponse({'response': True})
        except Exception as e:
            return JsonResponse({'response': False, 'reason': 'Registration failed'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('user')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'response': True, 'reason': 'login success'})
    return JsonResponse({'response': False, 'reason': 'login failed'})

@csrf_exempt
def health(request):
    return JsonResponse({'status': 'ok'})