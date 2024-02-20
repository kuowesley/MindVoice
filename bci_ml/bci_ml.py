import numpy as np
import torch 
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim
# from model.autoencoder_1 import EEGTransformer
from model.autoencoder_2 import EEGAutoencoderClassifier
import os
import argparse
from torch.nn.utils.rnn import pad_sequence


def data_loader(data_path):
    """
    # check if train_data.npy test_data.npy train_label.npy test_label.npy exist,
    # if not, throw error
    """
    if not os.path.exists(data_path + 'train_data.npy') or not os.path.exists(data_path + 'test_data.npy') or not os.path.exists(data_path + 'train_label.npy') or not os.path.exists(data_path + 'test_label.npy'):
        print("ERROR: Dataset not found. Please download the dataset from 'https://drive.google.com/drive/folders/1ykR-mn4d4KfFeeNrfR6UdtebsNRY8PU2?usp=sharing'")
        print("\n\n")
        raise FileNotFoundError("Please download the dataset from 'https://drive.google.com/drive/folders/1ykR-mn4d4KfFeeNrfR6UdtebsNRY8PU2?usp=sharing'")
    
    print("Loading data from ", data_path)
    train_data = np.load(data_path + 'train_data.npy')
    test_data = np.load(data_path + 'test_data.npy')
    train_label = np.load(data_path + 'train_label.npy')
    test_label = np.load(data_path + 'test_label.npy')

    #To convert the data into PyTorch tensors
    x_train_tensor = torch.Tensor(train_data) 
    y_train_tensor = torch.LongTensor(train_label) 
    x_test_tensor = torch.Tensor(test_data)
    y_test_tensor = torch.LongTensor(test_label)
    
    return x_train_tensor, y_train_tensor, x_test_tensor, y_test_tensor

def train_eval(data_path, n_epoch):
    x_train_tensor, y_train_tensor, x_test_tensor, y_test_tensor = data_loader(data_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    train_dataset = TensorDataset(x_train_tensor.to(device), y_train_tensor.to(device))
    train_loader = DataLoader(train_dataset, batch_size=64, drop_last=True, shuffle=True)
    test_dataset = TensorDataset(x_test_tensor.to(device), y_test_tensor.to(device))
    test_loader = DataLoader(test_dataset, batch_size=64,  drop_last=True,shuffle=False)

    num_classes = 5
    # model =  EEGTransformer(num_classes).to(device)
    model = EEGAutoencoderClassifier(num_classes, hidden_units=[1024, 512, 256]).to(device) 
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = n_epoch
    print("Training data with ", num_epochs, " epochs")
    for epoch in range(num_epochs):
        model.train()
        for data, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}')


    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for data, labels in test_loader:
            outputs = model(data)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    print(f'Test Accuracy: {accuracy * 100:.2f}%')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default='data/')
    parser.add_argument('--n_epoch', type=int, default=20)
    args = parser.parse_args()
    train_eval(args.data_path, args.n_epoch)
    # grid_search(args.data_path, args.n_epoch)

if __name__ == '__main__':
    flag = torch.cuda.is_available()
    if flag:
        print("CUDA can use")
    else:
        print("CUDA can not use")

    ngpu= 1
    os.environ['CUDA_VISIBLE_DEVICES'] ='0'
    # Decide which device we want to run on
    device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
    torch.cuda.set_device(0)
    print("GPU device:",device)
    print("GPU type: ",torch.cuda.get_device_name(0))
    main()