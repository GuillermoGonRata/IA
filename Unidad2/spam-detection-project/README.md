# Análisis y Mapeo de Detección de Spam

Este proyecto tiene como objetivo desarrollar un sistema robusto para detectar correos electrónicos no deseados (spam) utilizando reglas y análisis de datos. A continuación, se documenta el proceso siguiendo los pasos sugeridos en las instrucciones.

---

## 1. Recogida de datos

Se utilizó el dataset público [`spam.csv`](../data/spam.csv), que contiene mensajes etiquetados como "spam" o "ham" (legítimos).  
**Características del dataset:**

- **Remitente:** No disponible en este dataset.
- **Asunto:** No disponible en este dataset.
- **Contenido:** Disponible en la columna `Message`.
- **Enlaces:** Se detectan buscando patrones de URLs en el contenido.
- **Archivos adjuntos:** No disponible en este dataset.

El dataset fue adaptado para el análisis y la detección de spam, mapeando las columnas a la estructura esperada por el sistema.

---

## 2. Creación de reglas

Se desarrollaron reglas basadas en patrones comunes de spam, implementadas en [`src/SpamIndex.py`](../src/SpamIndex.py) y [`src/rules.py`](../src/rules.py):

- **Palabras clave:** Si el contenido contiene palabras como "gratis", "urgente", "win", "prize", "cash", "claim", se suma puntuación de spam.
- **Enlaces sospechosos:** Si el mensaje contiene enlaces (http, www), se suma puntuación.
- **Remitente sospechoso:** (No aplicable en este dataset, pero la regla existe para datasets con remitente).
- **Exceso de signos de exclamación o frases típicas de spam:** Se suma puntuación si se detectan patrones como "!!!" o frases como "100% gratis".

**Ejemplo de regla en código:**

```python
def contains_keyword(keywords):
    def condition(email_data):
        return any(keyword in email_data['contenido'].lower() for keyword in keywords)
    def action(email_data):
        return True
    return Rule("Contains Keyword", condition, action)
```

## 3. Implementación de la detección de spam

El sistema aplica las reglas a cada mensaje del dataset y determina si es spam según la puntuación acumulada.

```python
import pandas as pd
from src.SpamIndex import SpamDetectorReglas, adaptar_spam_csv

df = pd.read_csv('data/spam.csv', encoding='latin-1')
df = adaptar_spam_csv(df)
detector = SpamDetectorReglas()

for i, row in df.iterrows():
    email = row.to_dict()
    predicho, puntuacion = detector.es_spam(email)
    print(f"Mensaje {i+1}: Real: {email['es_spam']} | Detectado: {int(predicho)} | Puntuación: {puntuacion}")
```

Visualización de la distribución:

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 5))
sns.countplot(x='es_spam', data=df)
plt.title('Distribución de Correos Spam y Legítimos')
plt.xlabel('¿Es Spam? (1 = Sí, 0 = No)')
plt.ylabel('Cantidad')
plt.xticks(ticks=[0, 1], labels=['Legítimo', 'Spam'])
plt.show()
```

Nube de palabras de spam:

```python
from wordcloud import WordCloud

spam_text = ' '.join(df[df['es_spam'] == 1]['contenido'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(spam_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Nube de Palabras de Correos Spam')
plt.show()
```

## 4. Reflexión y análisis

**Eficacia de las reglas:**
Las reglas basadas en palabras clave y enlaces detectan la mayoría de los mensajes spam, pero pueden generar falsos positivos si un mensaje legítimo contiene palabras sospechosas.

**Resultados:**
El sistema detecta correctamente la mayoría de los mensajes spam del dataset spam.csv.
Se recomienda probar con otros datasets y ajustar las reglas según los resultados.

**Conclusión**
Este proyecto proporciona una base sólida para comprender y experimentar con mecanismos de detección de spam. La modularidad del sistema permite agregar nuevas reglas o integrar modelos de machine learning en el futuro.
