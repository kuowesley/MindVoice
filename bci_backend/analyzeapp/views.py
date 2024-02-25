from django.http import JsonResponse
from django.conf import settings
import torch
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import os
from django.views.decorators.csrf import csrf_exempt

import json
from .newEncoder import EEGAutoencoderClassifier


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EEGAutoencoderClassifier(num_classes=5)  # 移除 hidden_units 参数
model_path = os.path.join(settings.BASE_DIR, 'analyzeapp', 'eeg_CNNautoencoder_classifier_72.07.pth')
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

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

        # 将输入数据转换为张量，并添加一个批次维度
        input_tensor = torch.Tensor(input_data).to(device)
        input_tensor = input_tensor.unsqueeze(0)  # 现在形状应该是 [1, 64, 795]

        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output.data, 1)
            predicted_label = predicted.item()

        response = {
            'label': predicted_label,
            'time': user_time,
            'UserName': user_name
        }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'This endpoint only supports POST requests.'})



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
            return JsonResponse({'response': True, 'reason': 'yes'})
        else:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'response': False, 'reason': 'wrong password'})
            else:
                return JsonResponse({'response': False, 'reason': 'no user'})
    return JsonResponse({'response': False, 'reason': 'login failed'})

@csrf_exempt
def health(request):
    return JsonResponse({'status': 'ok'})