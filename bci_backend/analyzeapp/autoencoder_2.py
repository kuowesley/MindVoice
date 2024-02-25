import torch.nn as nn

class EEGAutoencoderClassifier(nn.Module):
    def __init__(self, num_classes, hidden_units=[256, 128, 64]):
        super(EEGAutoencoderClassifier, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(64 * 795, hidden_units[0]), # Input dimention is 64 channel * 795 time point, and use 256 units for first NN layer
            # nn.ReLU(), # Use ReLu function for NN training 
            nn.Softplus(),
            nn.Linear(hidden_units[0], hidden_units[1]), # 256 NN units to 128 units
            # nn.ReLU(),
            nn.Softplus(),
            nn.Linear(hidden_units[1], hidden_units[2]),#  128 NN units to 64 units
            # nn.ReLU()
            nn.Softplus(),
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_units[2], num_classes), # num_classes is 5 (hello,” “help me,” “stop,” “thank you,” and “yes”)
            nn.LogSoftmax(dim=1)  # Use LogSoftmax for multi-class classification
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.encoder(x)
        
        # import pdb;pdb.set_trace()
        x = self.classifier(x)
        return x