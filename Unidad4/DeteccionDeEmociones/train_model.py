import os, json, argparse
from PIL import Image
from tqdm import tqdm
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from torchvision.models import resnet18, ResNet18_Weights
import torch.nn as nn


class CocoClassificationDataset(Dataset):
    def __init__(self, ann_path, images_dir, transform=None):
        with open(ann_path, 'r', encoding='utf-8') as f:
            coco = json.load(f)
        imgs = {img['id']: img['file_name'] for img in coco.get('images', [])}
        ann_by_image = {}
        for ann in coco.get('annotations', []):
            img_id = ann['image_id']
            if img_id not in ann_by_image:
                ann_by_image[img_id] = ann['category_id']
        categories = coco.get('categories', [])
        self.cat_map = {c['id']: c['name'] for c in categories}
        cat_ids = sorted({c['id'] for c in categories})
        self.id2label = {cid: i for i, cid in enumerate(cat_ids)}
        self.samples = []
        for img_id, fname in imgs.items():
            if img_id in ann_by_image:
                cid = ann_by_image[img_id]
                label = self.id2label.get(cid)
                if label is None: continue
                self.samples.append((os.path.join(images_dir, fname), label))
        self.transform = transform

    def __len__(self): return len(self.samples)
    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert('RGB')
        if self.transform: img = self.transform(img)
        return img, label

def build_dataloaders(data_root, batch_size=32, img_size=224, num_workers=4):
    train_ann = os.path.join(data_root, 'train', '_annotations.coco.json')
    valid_ann = os.path.join(data_root, 'valid', '_annotations.coco.json')
    train_img_dir = os.path.join(data_root, 'train')
    valid_img_dir = os.path.join(data_root, 'valid')

    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(img_size),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.1, 0.1, 0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    valid_transform = transforms.Compose([
        transforms.Resize(int(img_size*1.14)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    train_ds = CocoClassificationDataset(train_ann, train_img_dir, transform=train_transform)
    valid_ds = CocoClassificationDataset(valid_ann, valid_img_dir, transform=valid_transform)

    # CORRECCIÓN: obtener número correcto de clases desde el mapeo del dataset
    num_classes = len(train_ds.id2label)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    valid_loader = DataLoader(valid_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return train_loader, valid_loader, train_ds, valid_ds, num_classes

def create_model(num_classes, pretrained=True):
    if pretrained:
        # Usa los pesos más recientes de ImageNet
        weights = ResNet18_Weights.DEFAULT
    else:
        weights = None

    model = resnet18(weights=weights)
    in_ft = model.fc.in_features
    if pretrained:
        for param in model.parameters():
            param.requires_grad = False
        model.fc = nn.Linear(in_ft, num_classes)

    return model


def train(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_loader, valid_loader, train_ds, valid_ds, num_classes = build_dataloaders(
        args.data_root, batch_size=args.batch_size, img_size=args.img_size, num_workers=args.num_workers)

    # Crear modelo con pesos preentrenados
    model = create_model(num_classes, pretrained=args.pretrained).to(device)
    criterion = nn.CrossEntropyLoss()

    # Fase 1: entrenar solo la capa final
    optimizer = optim.Adam(model.fc.parameters(), lr=args.lr)
    best_acc = 0.0
    os.makedirs(args.output_dir, exist_ok=True)

    inv = {v:k for k,v in train_ds.id2label.items()}
    label_map = {str(i): train_ds.cat_map.get(inv[i], str(inv[i])) for i in inv}
    with open(os.path.join(args.output_dir, 'label_map.json'), 'w', encoding='utf-8') as f:
        json.dump(label_map, f, ensure_ascii=False, indent=2)

    print("=== Fase 1: entrenando solo la capa final ===")
    for epoch in range(1, args.epochs_phase1+1):
        best_acc = run_epoch(model, train_loader, valid_loader, criterion, optimizer, device, epoch, best_acc, args.output_dir)

    # Fase 2: descongelar todo el modelo y entrenar con LR más pequeño
    for param in model.parameters():
        param.requires_grad = True
    optimizer = optim.Adam(model.parameters(), lr=args.lr_phase2)

    print("=== Fase 2: fine-tuning completo ===")
    for epoch in range(args.epochs_phase1+1, args.epochs_phase1+args.epochs_phase2+1):
        best_acc = run_epoch(model, train_loader, valid_loader, criterion, optimizer, device, epoch, best_acc, args.output_dir)

    print("Finished. Best val acc:", best_acc)


def run_epoch(model, train_loader, valid_loader, criterion, optimizer, device, epoch, best_acc, output_dir):
    model.train()
    running_loss = running_corrects = total = 0
    for images, labels in tqdm(train_loader, desc=f"Epoch {epoch} [train]"):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward(); optimizer.step()
        running_loss += loss.item() * images.size(0)
        preds = outputs.argmax(dim=1)
        running_corrects += (preds == labels).sum().item()
        total += images.size(0)
    train_acc = running_corrects/total

    model.eval()
    val_loss = val_corrects = val_total = 0
    with torch.no_grad():
        for images, labels in tqdm(valid_loader, desc=f"Epoch {epoch} [valid]"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images); loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            val_corrects += (preds == labels).sum().item(); val_total += images.size(0)
    val_acc = val_corrects/val_total

    print(f"Epoch {epoch}: train_acc={train_acc:.4f} val_acc={val_acc:.4f}")
    if val_acc > best_acc:
        best_acc = val_acc
        torch.save(model.state_dict(), os.path.join(output_dir, 'best_model.pth'))
        print(f"Saved best model (val_acc={best_acc:.4f})")
    return best_acc

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', default='data')
    parser.add_argument('--output_dir', default='models')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--img_size', type=int, default=224)
    parser.add_argument('--num_workers', type=int, default=4)
    parser.add_argument('--pretrained', action='store_true')
    parser.add_argument('--epochs_phase1', type=int, default=5)   # solo capa final
    parser.add_argument('--epochs_phase2', type=int, default=15)  # fine-tuning completo
    parser.add_argument('--lr_phase2', type=float, default=1e-4)  # LR más pequeño para fine-tuning
    args = parser.parse_args()
    train(args)