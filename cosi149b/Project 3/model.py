import torch
import torch_geometric
import numpy as np
from torch_geometric.data import Data
from torch_geometric.data import DataLoader
from torch_geometric.datasets import MoleculeNet
import pickle as pkl

#load datasets
#12 property tasks for predictions
train_dataset = torch.load("train_data.pt")
valid_dataset = torch.load("valid_data.pt")
test_dataset = torch.load("test_data.pt")

print(f'Size of training set: {len(train_dataset)}')
print(f'Size of validation set: {len(valid_dataset)}')
print(f'Size of test set: {len(test_dataset)}')

#example of preparing data loadesr
#you can use any batch size and see what happens in model performance

from torch_geometric.loader import DataLoader

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

#example of creating one mini-batch
batch = next(iter(train_loader))
print(batch)

#visualize one 2D molecule
from rdkit import Chem
#Chem.MolFromSmiles(g.smiles)

# Atom Encoder

class AtomEncoder(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(AtomEncoder, self).__init__()

        self.embeddings = torch.nn.ModuleList()

        for i in range(9):
            self.embeddings.append(torch.nn.Embedding(100, hidden_channels))
    
    def reset_parameters(self):
        for embedding in self.embeddings:
            embedding.reset_parameters()
    
    def forward(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(1)
        
        out = 0
        for i in range(x.size(1)):
            out += self.embeddings[i](x[:, i])
        return out

from torch_geometric.nn import GATv2Conv
from torch_geometric.nn import global_mean_pool as gap
import torch.nn.functional as F
from torch.nn import Linear
class GAT(torch.nn.Module):
    def __init__(self, hidden_channels, num_node_features, num_classes):
        super(GAT, self).__init__()
        torch.manual_seed(42)
        self.emb = AtomEncoder(hidden_channels=32)
        self.conv1 = GATv2Conv(hidden_channels,hidden_channels)
        self.conv2 = GATv2Conv(hidden_channels,hidden_channels)
        self.conv3 = GATv2Conv(hidden_channels,hidden_channels)
        self.lin = Linear(hidden_channels, num_classes)
    
    def forward(self, batch):
        x, edge_index, batch_size = batch.x, batch.edge_index, batch.batch
        x = self.emb(x)
        # 1. Obtain node embeddings
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        # 2. Readout layer
        x = gap(x, batch_size)      # [batch_size, hidden_channels]
        # 3. Apply a final classifier
        x = F.dropout(x, p=0.12, training=self.training)
        x = self.lin(x)
        return x


# create model
model = GAT(32, 9, 12)

# prediction
out = model(batch)
print(out.shape) #(num_of_graph, num_of_task)

# loss function and optimizer
import torch.nn as nn
import torch.optim as optim
import focal_loss_function
optimizer = optim.Adam(model.parameters(), lr=15e-4, weight_decay=1e-7)
criterion = nn.BCEWithLogitsLoss(reduction = "none")

from sklearn.metrics import roc_auc_score
def train(model, device, loader, optimizer):
    model.train()

    for step, batch in enumerate(loader):
        batch = batch.to(device)
        pred = model(batch)
        y = batch.y.view(pred.shape).to(torch.float64)

        optimizer.zero_grad()
        ## ignore nan targets (unlabeled) when computing training loss
        is_labeled = batch.y == batch.y
        loss = criterion(pred.to(torch.float32)[is_labeled], batch.y.to(torch.float32)[is_labeled]).mean()
        loss.backward()
        optimizer.step()

import csv
def eval(model, device, loader):
    model.eval()
    y_true = []
    y_pred = []
    # for every batch in test loader
    for batch in loader:

        batch = batch.to(device)
        if batch.x.shape[0] == 1:
            pass
        else:
            with torch.no_grad():
                pred = model(batch)
            
            y_true.append(batch.y.view(pred.shape))
            y_pred.append(pred)
    
    y_true = torch.cat(y_true, dim = 0).numpy()
    y_pred = torch.cat(y_pred, dim = 0).numpy()
    # compute the ROC - AUC score and store as history
    rocauc_list = []

    for i in range(y_true.shape[1]):
        # AUC is only defined when there is at least one positive data
        if np.sum(y_true[:, i] == 1) > 0 and np.sum(y_true[:, i] == 0) > 0:
            # ignore nan values
            is_labeled = y_true[:, i] == y_true[:, i]
            rocauc_list.append(roc_auc_score(y_true[is_labeled,i], y_pred[is_labeled,i]))

    if len(rocauc_list) == 0:
        raise RuntimeError('No positively labeled data available. Cannot compute ROC-AUC.')
    return {'rocauc': sum(rocauc_list)/len(rocauc_list)}


# Training
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print("Start training...")
for epoch in range(1, 8):
    print("====epoch " + str(epoch))

    # training
    train(model, device, train_loader, optimizer)

    # evaluating
    train_acc = eval(model, device, train_loader)
    val_acc = eval(model, device, val_loader)
    print({'Train': train_acc, 'Validation': val_acc})

# test prediction
y_pred = []
for batch in test_loader:
    batch = batch.to(device)
    if batch.x.shape[0] == 1:
        pass
    else:
        with torch.no_grad():
            pred = model(batch)
        y_pred.append(pred)

y_pred = torch.cat(y_pred, dim = 0).numpy()

with open("test_output.csv", mode='w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar=' ')

    # write each prediction to file
    for pred_all_attributes in y_pred:
        string_preds = [str(element) for element in pred_all_attributes]
        line = ', '.join(string_preds)
        writer.writerow([line])
print(f"predictions saved to test_output.csv")