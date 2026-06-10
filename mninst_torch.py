import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import os

# ══════════════════════════════════════════════════════════
# 1. DEVICE
# ══════════════════════════════════════════════════════════
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

# ══════════════════════════════════════════════════════════
# 2. DATI  (train / val / test)
# ══════════════════════════════════════════════════════════
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))   # media/std di MNIST
])

train_full = datasets.MNIST("data", train=True,  download=True, transform=transform)
test_ds    = datasets.MNIST("data", train=False, download=True, transform=transform)

# Ricava un validation set dal training
val_size   = 10_000
train_size = len(train_full) - val_size
train_ds, val_ds = torch.utils.data.random_split(train_full, [train_size, val_size])

train_loader = DataLoader(train_ds, batch_size=64, shuffle=True,  num_workers=2)
val_loader   = DataLoader(val_ds,   batch_size=256, shuffle=False, num_workers=2)
test_loader  = DataLoader(test_ds,  batch_size=256, shuffle=False, num_workers=2)

# ══════════════════════════════════════════════════════════
# 3. MODELLO
# ══════════════════════════════════════════════════════════
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # --- Blocco convoluzionale 1 ---
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)   # 28×28 → 28×28
        self.bn1   = nn.BatchNorm2d(32)
        # --- Blocco convoluzionale 2 ---
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # 14×14 → 14×14
        self.bn2   = nn.BatchNorm2d(64)
        # --- Classificatore fully-connected ---
        self.dropout = nn.Dropout(0.5)
        self.fc1     = nn.Linear(64 * 7 * 7, 128)
        self.fc2     = nn.Linear(128, 10)

    def forward(self, x):
        # conv → BN → ReLU → MaxPool
        x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), 2)  # → 32×14×14
        x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), 2)  # → 64×7×7
        # Flatten
        x = x.view(x.size(0), -1)                             # → 64*7*7 = 3136
        # FC
        x = F.relu(self.fc1(self.dropout(x)))
        x = self.fc2(x)                                        # logits (no softmax)
        return x

model = Net().to(device)
print(model)
print(f"Parametri: {sum(p.numel() for p in model.parameters()):,}")

# ══════════════════════════════════════════════════════════
# 4. LOSS, OTTIMIZZATORE, SCHEDULER
# ══════════════════════════════════════════════════════════
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
# ogni 3 epoche dimezza il learning rate

# ══════════════════════════════════════════════════════════
# 5. FUNZIONI DI TRAINING E VALUTAZIONE
# ══════════════════════════════════════════════════════════
def train_one_epoch(loader):
    model.train()
    total_loss, correct = 0.0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        out  = model(X)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(y)
        correct    += (out.argmax(1) == y).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)

@torch.no_grad()
def evaluate(loader):
    model.eval()
    total_loss, correct = 0.0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        out  = model(X)
        total_loss += criterion(out, y).item() * len(y)
        correct    += (out.argmax(1) == y).sum().item()
    return total_loss / len(loader.dataset), correct / len(loader.dataset)

# ══════════════════════════════════════════════════════════
# 6. TRAINING LOOP  con best-model checkpoint
# ══════════════════════════════════════════════════════════
EPOCHS       = 10
best_val_acc = 0.0
best_path    = "best_model.pth"

print(f"\n{'Epoch':>5} {'Train Loss':>11} {'Train Acc':>10} {'Val Loss':>10} {'Val Acc':>9} {'LR':>8}")
print("─" * 60)

for epoch in range(1, EPOCHS + 1):
    tr_loss, tr_acc = train_one_epoch(train_loader)
    vl_loss, vl_acc = evaluate(val_loader)
    scheduler.step()

    lr = optimizer.param_groups[0]["lr"]
    print(f"{epoch:>5}   {tr_loss:>10.4f}   {tr_acc:>9.2%}   {vl_loss:>9.4f}   {vl_acc:>8.2%}   {lr:.5f}")

    if vl_acc > best_val_acc:
        best_val_acc = vl_acc
        torch.save(model.state_dict(), best_path)
        print(f"        ✔ nuovo best salvato (val_acc={vl_acc:.2%})")

# ══════════════════════════════════════════════════════════
# 7. TEST FINALE  con il best model
# ══════════════════════════════════════════════════════════
model.load_state_dict(torch.load(best_path))
_, test_acc = evaluate(test_loader)
print(f"\nTest accuracy (best model): {test_acc:.2%}")
