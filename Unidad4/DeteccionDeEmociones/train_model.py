import os, json, argparse
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.utils as nn_utils
from torchvision import transforms, models
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from tqdm import tqdm
import json

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

def build_dataloaders(data_root, batch_size=16, img_size=224, num_workers=4):
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
    model = models.resnet18(pretrained=pretrained)
    in_ft = model.fc.in_features
    model.fc = nn.Linear(in_ft, num_classes)
    return model

def train(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    train_loader, valid_loader, train_ds, valid_ds, num_classes = build_dataloaders(
        args.data_root, batch_size=args.batch_size, img_size=args.img_size, num_workers=args.num_workers)
    
    model = create_model(num_classes, pretrained=args.pretrained).to(device)
    
    # Congelar backbone si se solicita
    if args.freeze_backbone:
        for name, p in model.named_parameters():
            if not name.startswith('fc'):
                p.requires_grad = False
        print("Backbone congelado. Solo entrenando FC layer.")
    
    # ===== BALANCEO DE CLASES =====
    class_counts = [0] * num_classes
    for _, lbl in train_ds.samples:
        class_counts[lbl] += 1
    
    total_samples = sum(class_counts)
    class_weights = [(total_samples / c) if c > 0 else 0.0 for c in class_counts]
    class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(device)
    
    print(f"Distribución de clases: {class_counts}")
    print(f"Pesos de clase: {class_weights}")
    
    # WeightedRandomSampler para balanceo en entrenamiento
    sample_weights = [class_weights[lbl] for _, lbl in train_ds.samples]
    sampler = WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)
    
    train_loader = DataLoader(
        train_ds, 
        batch_size=args.batch_size, 
        sampler=sampler,  # usa sampler en lugar de shuffle
        num_workers=args.num_workers
    )
    
    # Loss con pesos de clase
    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    
    # Optimizador
    optimizer = optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()), 
        lr=args.lr, 
        weight_decay=1e-4
    )
    
    # Scheduler
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    
    # Salvar label_map
    best_acc = 0.0
    os.makedirs(args.output_dir, exist_ok=True)
    
    inv = {v: k for k, v in train_ds.id2label.items()}
    label_map = {str(i): train_ds.cat_map.get(inv[i], str(inv[i])) for i in inv}
    with open(os.path.join(args.output_dir, 'label_map.json'), 'w', encoding='utf-8') as f:
        json.dump(label_map, f, ensure_ascii=False, indent=2)
    
    # ===== EARLY STOPPING =====
    no_improve_epochs = 0
    weight_small_change_epochs = 0
    prev_params = nn_utils.parameters_to_vector(model.parameters()).detach().cpu()
    
    for epoch in range(1, args.epochs + 1):
        # ENTRENAMIENTO
        model.train()
        running_loss = running_corrects = total = 0
        
        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch} [TRAIN]"):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            running_corrects += (preds == labels).sum().item()
            total += images.size(0)
        
        train_loss = running_loss / total
        train_acc = running_corrects / total
        
        # VALIDACIÓN
        model.eval()
        val_loss = val_corrects = val_total = 0
        
        with torch.no_grad():
            for images, labels in tqdm(valid_loader, desc=f"Epoch {epoch} [VALID]"):
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                val_corrects += (preds == labels).sum().item()
                val_total += images.size(0)
        
        val_loss = val_loss / val_total
        val_acc = val_corrects / val_total
        
        # CAMBIO DE PESOS
        curr_params = nn_utils.parameters_to_vector(model.parameters()).detach().cpu()
        delta = (curr_params - prev_params).norm().item()
        prev_params = curr_params
        
        print(f"\nEpoch {epoch}/{args.epochs}")
        print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
        print(f"  Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.4f}")
        print(f"  Weight delta L2: {delta:.6e}")
        print(f"  LR: {optimizer.param_groups[0]['lr']:.6f}")
        
        # Scheduler
        scheduler.step()
        
        # ===== EARLY STOPPING POR VALIDACIÓN =====
        if val_acc > best_acc + 1e-6:
            best_acc = val_acc
            no_improve_epochs = 0
            torch.save(model.state_dict(), os.path.join(args.output_dir, 'best_model.pth'))
            print(f"  ✓ Guardado mejor modelo (val_acc={best_acc:.4f})")
        else:
            no_improve_epochs += 1
        
        # ===== EARLY STOPPING POR CAMBIO DE PESOS =====
        if delta < args.weight_change_tol:
            weight_small_change_epochs += 1
        else:
            weight_small_change_epochs = 0
        
        # Condiciones de parada
        if no_improve_epochs >= args.early_stop_patience:
            print(f"\n⚠ PARADA TEMPRANA: Sin mejora en validación por {no_improve_epochs} épocas")
            break
        
        if weight_small_change_epochs >= args.weight_patience:
            print(f"\n⚠ PARADA TEMPRANA: Pesos cambiaron < {args.weight_change_tol} por {weight_small_change_epochs} épocas")
            break
    
    print(f"\n✓ Entrenamiento finalizado. Mejor val_acc: {best_acc:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', default='data', help='Ruta a dataset')
    parser.add_argument('--output_dir', default='models', help='Directorio para guardar modelos')
    parser.add_argument('--epochs', type=int, default=50, help='Número de épocas')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size')
    parser.add_argument('--lr', type=float, default=1e-4, help='Learning rate')
    parser.add_argument('--img_size', type=int, default=224, help='Tamaño de imagen')
    parser.add_argument('--num_workers', type=int, default=4, help='Workers para DataLoader')
    parser.add_argument('--pretrained', action='store_true', help='Usar pesos preentrenados ImageNet')
    parser.add_argument('--freeze_backbone', action='store_true', help='Congelar ResNet backbone')
    parser.add_argument('--early_stop_patience', type=int, default=5, 
                        help='Paciencia epochs sin mejora en validación')
    parser.add_argument('--weight_change_tol', type=float, default=1e-5,
                        help='Umbral L2 de cambio de pesos')
    parser.add_argument('--weight_patience', type=int, default=5,
                        help='Paciencia epochs con cambio de pesos pequeño')
    
    args = parser.parse_args()
    train(args)