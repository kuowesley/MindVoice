import torch
import torch.nn as nn
import torch.nn.functional as F


def Conv1d_Maker(in_channels, out_channels, kernel_size, padding=1, stride=1):
    return nn.Conv1d(in_channels, out_channels, kernel_size, padding=padding, stride=stride)

class ConvResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super(ConvResidualBlock, self).__init__()
        self.conv1 = Conv1d_Maker(in_channels, out_channels, kernel_size, padding=padding, stride=stride)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = Conv1d_Maker(out_channels, out_channels, kernel_size, padding=padding, stride=stride)
        self.bn2 = nn.BatchNorm1d(out_channels)
        self.adjust_dimensions = in_channels != out_channels or stride != 1
        if self.adjust_dimensions:
            self.downsample = nn.Sequential(
                Conv1d_Maker(in_channels, out_channels, 1, stride=stride),
                nn.BatchNorm1d(out_channels)
            )
        else:
            self.downsample = nn.Identity()

    def forward(self, x):
        identity = self.downsample(x)
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        if out.size(2) != identity.size(2):
            identity = F.interpolate(identity, size=out.size(2), mode='linear')

        out += identity
        out = self.relu(out)
        return out

class EEGAutoencoderClassifier(nn.Module):
    def __init__(self, num_classes):
        super(EEGAutoencoderClassifier, self).__init__()
        self.encoder = nn.Sequential(
            ConvResidualBlock(64, 128, kernel_size=3),
            nn.MaxPool1d(2, 2),
            nn.Dropout(0.5),
            ConvResidualBlock(128, 256, kernel_size=3),
            nn.MaxPool1d(2, 2),
            nn.Dropout(0.5),
            nn.Conv1d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool1d(1)
        )
        self.fc = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.encoder(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
