#!/usr/bin/env python3
"""
Script de entrenamiento (ejemplo con ImageDataGenerator).
Soporta carpetas con estructura:
data/train/<class>/*.jpg
data/val/<class>/*.jpg

Uso básico:
python train.py --data-dir data/train --val-dir data/val --epochs 20 --batch 32 --out models/emotion_model.h5
"""

import argparse
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from model import create_mobilenetv2_model

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", required=True, help="Directorio de entrenamiento (carpetas por clase)")
    p.add_argument("--val-dir", required=True, help="Directorio de validación (carpetas por clase)")
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--out", default="models/emotion_model.h5")
    p.add_argument("--img-size", type=int, default=96)
    p.add_argument("--lr", type=float, default=1e-4)
    return p.parse_args()

def main():
    args = parse_args()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        horizontal_flip=True,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        brightness_range=(0.8,1.2)
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        args.data_dir,
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch,
        class_mode="categorical"
    )
    val_gen = val_datagen.flow_from_directory(
        args.val_dir,
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch,
        class_mode="categorical"
    )

    num_classes = len(train_gen.class_indices)
    print("Clases:", train_gen.class_indices)

    model = create_mobilenetv2_model(input_shape=(args.img_size, args.img_size, 3), num_classes=num_classes)
    model.compile(optimizer=Adam(learning_rate=args.lr), loss="categorical_crossentropy", metrics=["accuracy"])

    callbacks = [
        ModelCheckpoint(args.out, save_best_only=True, monitor="val_accuracy", mode="max"),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1)
    ]

    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        callbacks=callbacks
    )

if __name__ == "__main__":
    main()