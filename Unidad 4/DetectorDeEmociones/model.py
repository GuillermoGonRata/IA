"""
Definición de modelos: opción de transfer learning (MobileNetV2) y una CNN sencilla.
"""

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

def create_mobilenetv2_model(input_shape=(96,96,3), num_classes=7, dropout=0.4):
    base = MobileNetV2(include_top=False, input_shape=input_shape, weights="imagenet")
    x = base.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Dense(128, activation="relu")(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    model = models.Model(inputs=base.input, outputs=outputs)
    return model

def create_simple_cnn(input_shape=(48,48,1), num_classes=7):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, (3,3), activation='relu'),
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model