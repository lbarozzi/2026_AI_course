import argparse
import json
import random
import time
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms
from PIL import Image


def set_seed(seed: int) -> None:
	random.seed(seed)
	torch.manual_seed(seed)
	torch.cuda.manual_seed_all(seed)


class Net(nn.Module):
	"""Rete di classificazione basata su ResNet18.

	Didatticamente: separiamo backbone (feature extractor) e layer finale
	(classificatore) cosi e chiaro dove avviene il transfer learning.
	"""

	def __init__(self, num_classes: int, freeze_backbone: bool, pretrained: bool = True):
		super().__init__()

		weights = models.ResNet18_Weights.DEFAULT if pretrained else None
		self.backbone = models.resnet18(weights=weights)

		if freeze_backbone:
			for p in self.backbone.parameters():
				p.requires_grad = False

		in_features = self.backbone.fc.in_features
		self.backbone.fc = nn.Linear(in_features, num_classes)
		self.arch = "resnet18"

	def forward(self, x):
		return self.backbone(x)


class NetCustom(nn.Module):
	"""Rete CNN didattica con strati espliciti per immagini RGB 224x224."""

	def __init__(self, num_classes: int):
		super().__init__()

		self.features = nn.Sequential(
			nn.Conv2d(3, 32, kernel_size=3, padding=1),
			nn.BatchNorm2d(32),
			nn.ReLU(inplace=True),
			nn.MaxPool2d(kernel_size=2),  # 224 -> 112

			nn.Conv2d(32, 64, kernel_size=3, padding=1),
			nn.BatchNorm2d(64),
			nn.ReLU(inplace=True),
			nn.MaxPool2d(kernel_size=2),  # 112 -> 56

			nn.Conv2d(64, 128, kernel_size=3, padding=1),
			nn.BatchNorm2d(128),
			nn.ReLU(inplace=True),
			nn.MaxPool2d(kernel_size=2),  # 56 -> 28

			nn.Conv2d(128, 256, kernel_size=3, padding=1),
			nn.BatchNorm2d(256),
			nn.ReLU(inplace=True),
			nn.AdaptiveAvgPool2d((1, 1)),
		)

		self.classifier = nn.Sequential(
			nn.Flatten(),
			nn.Dropout(p=0.3),
			nn.Linear(256, 128),
			nn.ReLU(inplace=True),
			nn.Dropout(p=0.2),
			nn.Linear(128, num_classes),
		)

		self.arch = "custom_cnn"

	def forward(self, x):
		x = self.features(x)
		x = self.classifier(x)
		return x


def build_transforms(img_size: int):
	train_tf = transforms.Compose([
		transforms.RandomResizedCrop(img_size),
		transforms.RandomHorizontalFlip(),
		transforms.RandomRotation(10),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])

	eval_tf = transforms.Compose([
		transforms.Resize(int(img_size * 1.15)),
		transforms.CenterCrop(img_size),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])
	return train_tf, eval_tf


def make_splits(data_dir: Path, img_size: int, val_ratio: float, test_ratio: float, seed: int):
	# Trasformazioni diverse: augmentation in train, preprocess stabile in eval.
	train_tf, eval_tf = build_transforms(img_size)
	full_eval_ds = datasets.ImageFolder(str(data_dir), transform=eval_tf)

	n_total = len(full_eval_ds)
	n_test = int(n_total * test_ratio)
	n_val = int(n_total * val_ratio)
	n_train = n_total - n_val - n_test

	if n_train <= 0 or n_val <= 0 or n_test <= 0:
		raise ValueError("Split non valido: riduci val-ratio/test-ratio o usa piu immagini")

	gen = torch.Generator().manual_seed(seed)
	train_idx, val_idx, test_idx = random_split(range(n_total), [n_train, n_val, n_test], generator=gen)

	train_ds = datasets.ImageFolder(str(data_dir), transform=train_tf)
	eval_ds = datasets.ImageFolder(str(data_dir), transform=eval_tf)

	train_subset = torch.utils.data.Subset(train_ds, train_idx.indices)
	val_subset = torch.utils.data.Subset(eval_ds, val_idx.indices)
	test_subset = torch.utils.data.Subset(eval_ds, test_idx.indices)

	return train_subset, val_subset, test_subset, full_eval_ds.classes


def build_model(num_classes: int, freeze_backbone: bool, arch: str = "resnet18"):
	if arch == "resnet18":
		return Net(num_classes=num_classes, freeze_backbone=freeze_backbone, pretrained=True)
	if arch == "custom_cnn":
		return NetCustom(num_classes=num_classes)
	raise ValueError(f"Architettura non supportata: {arch}")


def run_epoch(model, loader, criterion, optimizer, device):
	model.train()
	total_loss = 0.0
	total_correct = 0
	total_count = 0

	for x, y in loader:
		x, y = x.to(device), y.to(device)
		optimizer.zero_grad()
		logits = model(x)
		loss = criterion(logits, y)
		loss.backward()
		optimizer.step()

		total_loss += loss.item() * x.size(0)
		preds = torch.argmax(logits, dim=1)
		total_correct += (preds == y).sum().item()
		total_count += x.size(0)

	return total_loss / total_count, total_correct / total_count


@torch.no_grad()
def evaluate(model, loader, criterion, device):
	model.eval()
	total_loss = 0.0
	total_correct = 0
	total_count = 0

	for x, y in loader:
		x, y = x.to(device), y.to(device)
		logits = model(x)
		loss = criterion(logits, y)

		total_loss += loss.item() * x.size(0)
		preds = torch.argmax(logits, dim=1)
		total_correct += (preds == y).sum().item()
		total_count += x.size(0)

	return total_loss / total_count, total_correct / total_count


def save_checkpoint(path: Path, model, classes, img_size: int):
	ckpt = {
		"state_dict": model.state_dict(),
		"classes": classes,
		"img_size": img_size,
		"arch": getattr(model, "arch", "resnet18"),
	}
	path.parent.mkdir(parents=True, exist_ok=True)
	torch.save(ckpt, path)


def train_one_arch(arch, args, classes, train_loader, val_loader, test_loader, device):
	"""Allena una singola architettura e restituisce metriche e path checkpoint."""
	print(f"\n=== Training architettura: {arch} ===")

	model = build_model(
		num_classes=len(classes),
		freeze_backbone=args.freeze_backbone,
		arch=arch,
	).to(device)
	criterion = nn.CrossEntropyLoss()

	params = [p for p in model.parameters() if p.requires_grad]
	optimizer = torch.optim.Adam(params, lr=args.lr)

	best_val_acc = 0.0
	best_path = Path(args.output_dir) / f"flower_{arch}.pt"

	for epoch in range(1, args.epochs + 1):
		tr_loss, tr_acc = run_epoch(model, train_loader, criterion, optimizer, device)
		va_loss, va_acc = evaluate(model, val_loader, criterion, device)

		print(
			f"[{arch}] Epoch {epoch:02d}/{args.epochs} | "
			f"train_loss={tr_loss:.4f} train_acc={tr_acc:.4f} | "
			f"val_loss={va_loss:.4f} val_acc={va_acc:.4f}"
		)

		if va_acc > best_val_acc:
			best_val_acc = va_acc
			save_checkpoint(best_path, model, classes, args.img_size)

	ckpt = torch.load(best_path, map_location=device)
	model.load_state_dict(ckpt["state_dict"])
	te_loss, te_acc = evaluate(model, test_loader, criterion, device)
	print(f"[{arch}] Test: loss={te_loss:.4f} acc={te_acc:.4f}")

	return {
		"checkpoint": str(best_path),
		"best_val_acc": best_val_acc,
		"test_acc": te_acc,
		"test_loss": te_loss,
	}


def train_app(args):
	set_seed(args.seed)
	data_dir = Path(args.data_dir)
	if not data_dir.exists():
		raise FileNotFoundError(f"Dataset non trovato: {data_dir}")

	# 1) Caricamento dataset e split train/val/test.
	train_ds, val_ds, test_ds, classes = make_splits(
		data_dir=data_dir,
		img_size=args.img_size,
		val_ratio=args.val_ratio,
		test_ratio=args.test_ratio,
		seed=args.seed,
	)

	device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
	train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers)
	val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)
	test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)

	print(f"Classi trovate: {classes}")
	print(f"Split: train={len(train_ds)} val={len(val_ds)} test={len(test_ds)}")
	print(f"Device: {device}")
	print(f"Output directory: {args.output_dir}")

	archs = ["resnet18", "custom_cnn"] if args.arch == "both" else [args.arch]
	results = {}

	# 2) Training di una o entrambe le architetture.
	for arch in archs:
		results[arch] = train_one_arch(
			arch=arch,
			args=args,
			classes=classes,
			train_loader=train_loader,
			val_loader=val_loader,
			test_loader=test_loader,
			device=device,
		)

	# 3) Report unico con metriche di tutte le reti addestrate.
	report_path = Path(args.report_path)
	report_path.parent.mkdir(parents=True, exist_ok=True)
	with open(report_path, "w", encoding="utf-8") as f:
		json.dump(
			{
				"classes": classes,
				"results": results,
				"img_size": args.img_size,
				"epochs": args.epochs,
				"batch_size": args.batch_size,
				"lr": args.lr,
			},
			f,
			indent=2,
		)

	for arch in archs:
		print(f"Modello salvato in: {results[arch]['checkpoint']}")
	print(f"Report salvato in: {report_path}")


@torch.no_grad()
def predict_one(args):
	device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
	arch_to_model_path = {
		"resnet18": Path(args.model_resnet18),
		"custom_cnn": Path(args.model_custom),
	}

	archs = ["resnet18", "custom_cnn"] if args.arch == "both" else [args.arch]
	# archs = ["custom_cnn", "resnet18", ] if args.arch == "both" else [args.arch]
	results = []

	for arch in archs:
		model_path = arch_to_model_path[arch]
		if not model_path.exists():
			print(f"Checkpoint non trovato per {arch}: {model_path}")
			continue

		ckpt = torch.load(model_path, map_location=device)
		classes = ckpt["classes"]
		img_size = ckpt.get("img_size", 224)
		ckpt_arch = ckpt.get("arch", arch)

		model = build_model(num_classes=len(classes), freeze_backbone=False, arch=ckpt_arch).to(device)
		model.load_state_dict(ckpt["state_dict"])
		model.eval()

		_, eval_tf = build_transforms(img_size)
		img = Image.open(args.image).convert("RGB")
		x = eval_tf(img).unsqueeze(0).to(device)

		# Warmup: evita di misurare l'overhead della prima inferenza.
		for _ in range(args.warmup_runs):
			_ = model(x)
			if device.type == "cuda":
				torch.cuda.synchronize()

		times_ms = []
		logits = None
		for _ in range(args.benchmark_runs):
			start_t = time.perf_counter()
			logits = model(x)
			if device.type == "cuda":
				torch.cuda.synchronize()
			times_ms.append((time.perf_counter() - start_t) * 1000.0)

		elapsed_ms = sum(times_ms) / len(times_ms)
		min_ms = min(times_ms)
		max_ms = max(times_ms)

		probs = torch.softmax(logits, dim=1)
		conf, idx = torch.max(probs, dim=1)

		pred_label = classes[idx.item()]
		conf_value = conf.item()
		results.append((arch, pred_label, conf_value, elapsed_ms, min_ms, max_ms, str(model_path)))

	if not results:
		raise FileNotFoundError("Nessun checkpoint valido trovato per la predizione")

	print("\nConfronto modelli su immagine:")
	for arch, pred_label, conf_value, elapsed_ms, min_ms, max_ms, model_path in results:
		print(
			f"- {arch:<10} | predizione: {pred_label:<12} | "
			f"confidenza: {conf_value:.4f} | tempo medio: {elapsed_ms:8.3f} ms "
			f"(min: {min_ms:8.3f}, max: {max_ms:8.3f}) | file: {model_path}"
		)

	best = max(results, key=lambda item: item[2])
	print(f"\nMiglior confidenza: modello={best[0]} classe={best[1]} conf={best[2]:.4f}")

	fastest = min(results, key=lambda item: item[3])
	print(f"Piu veloce: modello={fastest[0]} tempo={fastest[3]:.3f} ms")


def parse_args():
	p = argparse.ArgumentParser(description="Flower classifier con PyTorch")
	p.add_argument("--mode", choices=["train", "predict"], default="train")
	p.add_argument("--data-dir", default="tf_files/flower_photos")
	p.add_argument("--output-dir", default="models")
	p.add_argument("--model-resnet18", default="models/flower_resnet18.pt")
	p.add_argument("--model-custom", default="models/flower_custom_cnn.pt")
	p.add_argument("--report-path", default="models/training_report.json")
	p.add_argument("--image", default=None)
	p.add_argument("--epochs", type=int, default=10)
	p.add_argument("--batch-size", type=int, default=32)
	p.add_argument("--lr", type=float, default=1e-3)
	p.add_argument("--img-size", type=int, default=224)
	p.add_argument("--val-ratio", type=float, default=0.15)
	p.add_argument("--test-ratio", type=float, default=0.15)
	p.add_argument("--num-workers", type=int, default=2)
	p.add_argument("--seed", type=int, default=42)
	p.add_argument("--freeze-backbone", action="store_true")
	p.add_argument("--arch", choices=["resnet18", "custom_cnn", "both"], default="both")
	p.add_argument("--warmup-runs", type=int, default=5)
	p.add_argument("--benchmark-runs", type=int, default=30)
	p.add_argument("--cpu", action="store_true")
	return p.parse_args()


def main():
	args = parse_args()
	if args.mode == "train":
		train_app(args)
	else:
		if not args.image:
			raise ValueError("In modalita predict devi passare --image")
		predict_one(args)


if __name__ == "__main__":
	main()
