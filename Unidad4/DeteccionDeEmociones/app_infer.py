import os, json, cv2, torch
from torchvision import transforms, models
from PIL import Image

def load_model(model_path, num_classes, device):
    model = models.resnet18(pretrained=False)
    in_ft = model.fc.in_features
    model.fc = torch.nn.Linear(in_ft, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device).eval()
    return model

def preprocess(face, img_size=224):
    pil = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
    tf = transforms.Compose([
        transforms.Resize(int(img_size*1.14)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    return tf(pil).unsqueeze(0)

if __name__ == "__main__":
    models_dir = "models"
    model_path = os.path.join(models_dir, "best_model.pth")
    label_path = os.path.join(models_dir, "label_map.json")
    assert os.path.exists(model_path), "models/best_model.pth missing"
    assert os.path.exists(label_path), "models/label_map.json missing"
    with open(label_path, 'r', encoding='utf-8') as f:
        label_map = json.load(f)
    inv_label = {int(k): v for k,v in label_map.items()}
    num_classes = len(inv_label)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = load_model(model_path, num_classes, device)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            face = frame[y:y+h, x:x+w]
            inp = preprocess(face).to(device)
            with torch.no_grad():
                out = model(inp)
                pred = int(out.argmax(dim=1).item())
            label = inv_label.get(pred, str(pred))
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0),2)
        cv2.imshow("Detect & Emotion", frame)
        if cv2.waitKey(1) & 0xFF == 27: break
    cap.release(); cv2.destroyAllWindows()