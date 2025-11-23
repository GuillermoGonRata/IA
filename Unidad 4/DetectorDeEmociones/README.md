# Detector de Emociones (Visión por Computadora + IA)

Descripción
- Repositorio base para crear una aplicación que detecte emociones/afectos desde la cámara de tu laptop.
- Incluye ejemplo de captura con OpenCV, detección de cara con MediaPipe (rápido) y un pipeline para inferencia con un modelo de Keras/TensorFlow.
- También contiene un scaffold para entrenar tu propio modelo (opción con transfer learning) usando datasets públicos (FER2013, AffectNet, RAF-DB).

Advertencia importante
- Los sistemas de detección de emociones faciales tienen limitaciones: sesgos demográficos, imprecisión en contextos reales, y riesgos de privacidad. Úsalos con cuidado, solicita consentimiento y cumple la normativa local (GDPR, etc.).
- Este repositorio es educativo: no lo uses para decisiones críticas sin validación humana.

Qué incluye
- app.py: aplicación que accede a la cámara y muestra predicciones en tiempo real.
- train.py: script para entrenar un modelo con un dataset tipo FER2013 o con imágenes en carpetas.
- model.py: definición del modelo (transfer learning y un ejemplo de CNN simple).
- utils.py: utilidades (preprocesado, mapeo de etiquetas).
- requirements.txt: dependencias.
- .gitignore, LICENSE.

Modelos recomendados (rápido resumen)
- Para prototipos y laptop:
  - Transfer learning con MobileNetV2 o EfficientNetB0 (entrada 96x96 o 128x128) — buena relación velocidad/precisión.
  - Modelos ligeros (MobileNetV2) para inferencia en CPU.
- Para mejor rendimiento (si tienes GPU):
  - ResNet50 / EfficientNet + fine-tuning en AffectNet o RAF-DB.
- Para valence-arousal (sentimientos en continuo):
  - Modelos de regresión entrenados en AffectNet (etiquetas de valence/arousal).
- Alternativas ya entrenadas:
  - DeepFace (librería Python), FER (python-fer), servicios comerciales (Affectiva, Azure Face, AWS Rekognition). Comercial tiene costo / privacidad.

Datasets útiles
- FER2013 — CSV (48x48 grayscale), usado para emociones discretas (7 categorías).
- AffectNet — amplio, con anotaciones de emociones discretas y valence/arousal (mejor pero grande).
- RAF-DB — buena calidad de anotaciones.
- CK+, KDEF — pequeños, controlados (útiles para validar).

Cómo entrenarlo (resumen práctico)
1. Elegir etiquetas: emociones discretas (ej. angry, disgust, fear, happy, sad, surprise, neutral) o valence-arousal (regresión).
2. Reunir datos: usar FER2013 / AffectNet o recopilar datos propios (consentimiento).
3. Preprocesado: detección de cara → recorte → normalización; redimensionar a resolución del modelo (48x48 para CNN sencillo, 96/128 para MobileNet).
4. Data augmentation: rotación pequeñas, flip horizontal, variación de brillo/contraste.
5. Transfer learning: inicializar MobileNetV2 con pesos de ImageNet, reemplazar cabeza, entrenar capa superior, luego “unfreeze” y ajustar.
6. Métricas: accuracy, precision/recall por clase, F1, matriz de confusión; para valence/arousal: MSE, CCC.
7. Validación cruzada y conjunto de test separado para evitar sobreajuste.
8. Exportar modelo (SavedModel o .h5) y usarlo en la app en tiempo real.

Privacidad y ética
- Informa a las personas, recolecta consentimiento explícito, permite borrar datos.
- Cuidado con decisiones automatizadas: no usar para selección laboral, salud, etc. sin supervisión humana.
- Considera sesgo: evalúa rendimiento por demografía.

Cómo ejecutar el demo (ejemplo rápido)
1. Crear un entorno virtual y activar.
2. Instalar dependencias:
   pip install -r requirements.txt
3. Ejecutar la app:
   python app.py
4. Para entrenar:
   - Preparar data en estructura tipo ImageDataGenerator (carpeta por clase).
   - Ejecutar:
     python train.py --data-dir data/train --val-dir data/val --epochs 30

Contribuciones
- Pull requests bienvenidos: mejoras en modelos, soporte para audio/text (multimodal), scripts de evaluación y notebooks.

Licencia
- MIT (archivo LICENSE).
