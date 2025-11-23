#!/usr/bin/env python3
"""
Demo en tiempo real: captura cámara -> detecta caras -> predice emoción con modelo Keras.
Requiere: OpenCV, MediaPipe, TensorFlow/Keras.
"""

import cv2
import numpy as np
try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except Exception:
    mp = None
    HAS_MEDIAPIPE = False
try:
    from tensorflow.keras.models import load_model
    HAS_TF = True
except Exception:
    load_model = None
    HAS_TF = False
from utils import preprocess_face, EMOTION_LABELS

# Ruta por defecto al modelo entrenado (cambia si usas otro)
MODEL_PATH = "models/emotion_model.h5"

def main(camera_index=0):
    # Cargar modelo si existe (sino la app mostrará la cámara sin predicción)
    model = None
    if HAS_TF and load_model is not None:
        try:
            model = load_model(MODEL_PATH)
            print(f"Modelo cargado desde {MODEL_PATH}")
        except Exception as e:
            print("No se pudo cargar el modelo:", e)
            print("La app seguirá mostrando la cámara sin predicciones.")
    else:
        print("TensorFlow/Keras no disponible — la app continuará sin predicciones.")

    # Preparar detector: usar MediaPipe si está disponible, si no usar Haar cascade de OpenCV
    if HAS_MEDIAPIPE:
        mp_face = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        face_detector = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)
    else:
        face_detector = None
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(camera_index)

    if HAS_MEDIAPIPE:
        # Usar MediaPipe dentro del context manager
        with face_detector:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detector.process(frame_rgb)

                if results.detections:
                    for det in results.detections:
                        bbox = det.location_data.relative_bounding_box
                        h, w, _ = frame.shape
                        x1 = int(bbox.xmin * w)
                        y1 = int(bbox.ymin * h)
                        box_w = int(bbox.width * w)
                        box_h = int(bbox.height * h)
                        x2 = x1 + box_w
                        y2 = y1 + box_h

                        # Asegurar límites
                        x1c, y1c = max(0, x1), max(0, y1)
                        x2c, y2c = min(w, x2), min(h, y2)
                        face_img = frame[y1c:y2c, x1c:x2c]

                        label = "No model"
                        if model is not None and face_img.size != 0:
                            x_in = preprocess_face(face_img)
                            preds = model.predict(np.expand_dims(x_in, axis=0), verbose=0)
                            if preds.shape[-1] == 1:
                                label = f"val:{preds[0][0]:.2f}"
                            else:
                                idx = int(np.argmax(preds[0]))
                                prob = float(np.max(preds[0]))
                                label = f"{EMOTION_LABELS[idx]} ({prob:.2f})"

                        cv2.rectangle(frame, (x1c, y1c), (x2c, y2c), (0,255,0), 2)
                        cv2.putText(frame, label, (x1c, max(0, y1c-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                cv2.imshow("Emotion detector - q to quit", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
    else:
        # Fallback: Haar cascade (funciona sin mediapipe)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

            for (x, y, w, h) in faces:
                x1c, y1c, x2c, y2c = x, y, x + w, y + h
                face_img = frame[y1c:y2c, x1c:x2c]

                label = "No model"
                if model is not None and face_img.size != 0:
                    x_in = preprocess_face(face_img)
                    preds = model.predict(np.expand_dims(x_in, axis=0), verbose=0)
                    if preds.shape[-1] == 1:
                        label = f"val:{preds[0][0]:.2f}"
                    else:
                        idx = int(np.argmax(preds[0]))
                        prob = float(np.max(preds[0]))
                        label = f"{EMOTION_LABELS[idx]} ({prob:.2f})"

                cv2.rectangle(frame, (x1c, y1c), (x2c, y2c), (0,255,0), 2)
                cv2.putText(frame, label, (x1c, max(0, y1c-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            cv2.imshow("Emotion detector - q to quit", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()