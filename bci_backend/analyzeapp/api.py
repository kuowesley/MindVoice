from flask import Flask, request, jsonify
import torch
import numpy as np
from ..model.autoencoder_2 import EEGAutoencoderClassifier  # 確保將您的模型類存儲在名為 model.py 的文件中

app = Flask(__name__)

# 載入模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = EEGAutoencoderClassifier(num_classes=5, hidden_units=[1024, 512, 256]).to(device)
model_path = 'eeg_autoencoder_classifier_500.pth'  # 修改為您的模型檔案路徑
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

@app.route('/analyze', methods=['POST'])
def analyze_data():
    # 解析傳入的 JSON 資料
    data = request.get_json(force=True)
    input_data = data['data']
    user_time = data['time']  # 接收傳入的時間
    user_name = data['UserName']  # 接收傳入的使用者名稱

    # 轉換資料為適合模型的格式
    input_tensor = torch.Tensor(input_data).to(device)
    input_tensor = input_tensor.view(1, -1)  # 假設輸入為單個樣本

    # 進行預測
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output.data, 1)
        predicted_label = predicted.item()

    # 返回預測結果和接收到的時間、使用者名稱
    response = {
        'label': predicted_label,
        'time': user_time,
        'UserName': user_name
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8868, debug=True,threaded=True)
