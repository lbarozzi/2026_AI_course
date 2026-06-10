import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
# ── 1. Modello ────────────────────────────────────────────
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 16)   # 4 feature → 16 neuroni
        self.fc2 = nn.Linear(16, 3)   # 16 → 3 classi

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)               # logits grezzi (no softmax)
        return x

model = Net()

# ── 2. Dati ──────────────────────────────────────────────
iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) # random_state=42)

scaler = StandardScaler()
X_train = torch.tensor(scaler.fit_transform(X_train), dtype=torch.float32)
X_test  = torch.tensor(scaler.transform(X_test),      dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
y_test  = torch.tensor(y_test,  dtype=torch.long)

# ── 3. Loss e ottimizzatore ───────────────────────────────
criterion = nn.CrossEntropyLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4, foreach=True)

# ── 4. Training loop ──────────────────────────────────────
for epoch in range(100):
    model.train()
    loss = criterion(model(X_train), y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1:3d} | loss: {loss.item():.4f}")

# ── 5. Valutazione ────────────────────────────────────────
model.eval()
with torch.no_grad():
    preds = model(X_test).argmax(dim=1)
    acc   = (preds == y_test).float().mean()
    print(f"\nTest accuracy: {acc:.2%}")