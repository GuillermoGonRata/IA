"""
Utilidades: preprocesado de caras, mapeo de etiquetas, helpers.
"""

import cv2
import numpy as np

# Etiquetas por defecto (FER-style 7 clases)
EMOTION_LABELS = [
    "angry",
    "disgust",
    "fear",
    "happy",
    "sad",
    "surprise",
    "neutral"
]

def preprocess_face(face_img, target_size=(96,96)):
    """
    face_img: BGR image (OpenCV)
    Devuelve: imagen normalizada para pasar al modelo (float32), rango [0,1]
    - Convierte a RGB, redimensiona y normaliza.
    - Si tu modelo espera escala diferente o grayscale, ajustar aquí.
    """
    if face_img is None or face_img.size == 0:
        return np.zeros((target_size[0], target_size[1], 3), dtype=np.float32)

    img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, target_size)
    x = img_resized.astype("float32") / 255.0
    return x