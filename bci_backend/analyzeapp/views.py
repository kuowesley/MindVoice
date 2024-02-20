from django.http import JsonResponse
from django.conf import settings
import torch
import os
from django.views.decorators.csrf import csrf_exempt

import json
from .autoencoder_2 import EEGAutoencoderClassifier

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EEGAutoencoderClassifier(num_classes=5, hidden_units=[1024, 512, 256])
model_path = os.path.join(settings.BASE_DIR, 'analyzeapp', 'eeg_autoencoder_classifier_500.pth')
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

@csrf_exempt
def analyze(request):
    if request.method == 'POST':
        # 使用 request.body 獲取原始請求體，並解析 JSON 數據
        try:
            data = json.loads(request.body.decode('utf-8'))
            input_data = data.get('data')
            user_time = data.get('time')
            user_name = data.get('UserName')
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 確保 input_data 不是 None
        if input_data is None:
            return JsonResponse({'error': 'No data provided'}, status=400)
        input_tensor = torch.Tensor(input_data).to(device)
        input_tensor = input_tensor.view(1, -1)
        
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

