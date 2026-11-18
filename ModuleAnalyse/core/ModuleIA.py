from torch import nn, Dataset


class ModuleIA(nn.Module):
    def __init__(self):
        pass
    
    def train(self, fonction_perte, donnees_entrainement, ):
        pass

    def save_model(self):
        pass

class CreationDonneesEntrainementIA:
    pass

class DonneesEntrainementIA(Dataset):
    def __init__(self, target, feature):
        self.target = target
        self.feature = feature

    def __len__(self):
        return len(self.target)
    
    def __getitem__(self, idx):
        x = self.target[idx]
        y = self.feature[idx]
        return (x, y)
