# save this as find_specific_labels_and_save.py

import numpy as np
import json


def load_data_and_label(data_path, label_path):
    test_data = np.load(data_path)
    test_label = np.load(label_path)
    return test_data, test_label


def find_data_by_label(data, labels, target_labels):
    for target_label in target_labels:
        idxs = np.where(labels == target_label)[0]
        if len(idxs) > 0:  # 確保找到了匹配的資料
            idx = idxs[0]  # 使用第一個匹配的索引
            yield data[idx], labels[idx]
        else:
            print(f'Warning: No data found for label {target_label}')


def save_json_to_file(data_label_pair, file_path):
    with open(file_path, 'w') as file:
        json_str = json.dumps(data_label_pair, indent=4)
        file.write(json_str)


def main():
    # 'train_data.npy'
    data_path = input("Enter the data path: ")
    # 'train_label.npy'
    label_path = input("Enter the label path: ")
    test_data, test_label = load_data_and_label(data_path, label_path)
    # 定義需要找到的標籤
    target_labels = [1, 2, 3, 4, 0]

    for data, label in find_data_by_label(test_data, test_label, target_labels):
        # 將找到的資料和標籤轉換為 JSON 可接受的格式
        data_label_pair = {
            'data': data.tolist(),
            'label': label.tolist() if hasattr(label, 'tolist') else label
        }

        # 指定 JSON 檔案名稱
        json_file_path = f'{label}.json'

        # 保存 JSON
        save_json_to_file(data_label_pair, json_file_path)
        print(f'Label {label} data has been saved to {json_file_path}')

if __name__ == '__main__':
    main()