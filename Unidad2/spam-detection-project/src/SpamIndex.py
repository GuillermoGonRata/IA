import re
import pandas as pd
from urllib.parse import urlparse

# Estructura del dataset
data = {
    'remitente': [],
    'asunto': [],
    'contenido': [],
    'tiene_enlaces': [],
    'tiene_adjuntos': [],
    'es_spam': []  # 1 para spam, 0 para legítimo
}

class SpamDetectorReglas:
    def __init__(self):
        self.reglas = []
        self.dominios_sospechosos = ['promo', 'offer', 'free', 'winner', 'prize']
        self.palabras_clave_spam = [
            'gratis', 'ganador', 'urgente', 'oferta', 'promoción',
            'descuento', 'dinero', 'millonario', 'click aquí'
        ]
    
    def agregar_regla(self, nombre, funcion):
        self.reglas.append({'nombre': nombre, 'funcion': funcion})
    
    def analizar_remitente(self, email):
        """Regla 1: Análisis del remitente"""
        dominio = email.split('@')[-1] if '@' in email else ''
        puntuacion = 0
        
        # Verificar dominio sospechoso
        for dominio_sos in self.dominios_sospechosos:
            if dominio_sos in dominio.lower():
                puntuacion += 2
        
        return puntuacion
    
    def analizar_asunto(self, asunto):
        """Regla 2: Análisis del asunto"""
        puntuacion = 0
        asunto_lower = asunto.lower()
        
        for palabra in self.palabras_clave_spam:
            if palabra in asunto_lower:
                puntuacion += 1
        
        # Patrones sospechosos
        if re.search(r'[!]{2,}', asunto):  # Múltiples exclamaciones
            puntuacion += 1
        if re.search(r'\b(100%|gratis|urgente)\b', asunto_lower):
            puntuacion += 2
            
        return puntuacion
    
    def analizar_enlaces(self, contenido):
        """Regla 3: Detección de enlaces sospechosos"""
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', contenido)
        puntuacion = 0
        
        for url in urls:
            dominio = urlparse(url).netloc.lower()
            # Verificar dominios acortados
            if any(acortador in dominio for acortador in ['bit.ly', 'tinyurl', 'goo.gl']):
                puntuacion += 2
            # Verificar IPs en lugar de dominios
            if re.match(r'\d+\.\d+\.\d+\.\d+', dominio):
                puntuacion += 3
                
        return min(puntuacion, 5)  # Máximo 5 puntos
    
    def analizar_contenido(self, contenido):
        """Regla 4: Análisis del contenido del mensaje"""
        contenido_lower = contenido.lower()
        puntuacion = 0
        
        # Palabras clave en contenido
        palabras_encontradas = sum(1 for palabra in self.palabras_clave_spam 
                                 if palabra in contenido_lower)
        puntuacion += min(palabras_encontradas, 3)
        
        # Patrones de urgencia
        if re.search(r'\b(urgente|inmediato|ahora mismo)\b', contenido_lower):
            puntuacion += 2
            
        return puntuacion
    
    def es_spam(self, email_data):
        """Aplicar todas las reglas y determinar si es spam"""
        puntuacion_total = 0
        
        puntuacion_total += self.analizar_remitente(email_data['remitente'])
        puntuacion_total += self.analizar_asunto(email_data['asunto'])
        puntuacion_total += self.analizar_enlaces(email_data['contenido'])
        puntuacion_total += self.analizar_contenido(email_data['contenido'])
        
        # Umbral para considerar spam
        return puntuacion_total >= 3, puntuacion_total

# Documentación de reglas
REGLAS_DOCUMENTADAS = """
Reglas implementadas:
1. Análisis del remitente: Verifica dominios sospechosos
2. Análisis del asunto: Detecta palabras clave y patrones de urgencia
3. Detección de enlaces: Identifica URLs acortadas y IPs
4. Análisis de contenido: Busca patrones de spam en el cuerpo del mensaje

Umbral: 3 puntos o más = SPAM
"""

def evaluar_sistema(detector, datos_prueba):
    """Evaluar el rendimiento del sistema"""
    verdaderos_positivos = 0
    falsos_positivos = 0
    verdaderos_negativos = 0
    falsos_negativos = 0
    
    for email in datos_prueba:
        es_spam_real = email['es_spam']
        es_spam_predicho, _ = detector.es_spam(email)
        
        if es_spam_real and es_spam_predicho:
            verdaderos_positivos += 1
        elif not es_spam_real and not es_spam_predicho:
            verdaderos_negativos += 1
        elif not es_spam_real and es_spam_predicho:
            falsos_positivos += 1
        else:
            falsos_negativos += 1
    
    precision = verdaderos_positivos / (verdaderos_positivos + falsos_positivos) if (verdaderos_positivos + falsos_positivos) > 0 else 0
    recall = verdaderos_positivos / (verdaderos_positivos + falsos_negativos) if (verdaderos_positivos + falsos_negativos) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'verdaderos_positivos': verdaderos_positivos,
        'falsos_positivos': falsos_positivos
    }

# Plantilla para el informe de reflexión
INFORME_REFLECCION = """
## Informe de Reflexión - Sistema de Detección de Spam

### Metodología Utilizada
{metodologia}

### Resultados Obtenidos
- Emails spam detectados: {spam_detectados}
- Precisión del sistema: {precision}
- Falsos positivos: {falsos_positivos}

### Efectividad de las Reglas
{analisis_reglas}

### Mejoras Identificadas
{mejoras_identificadas}

### Conclusión
{conclusion}
"""

if __name__ == "__main__":
    # Ejemplo de emails de prueba
    emails_prueba = [
        {
            'remitente': 'promo@ofertas.com',
            'asunto': '¡Gana dinero urgente!',
            'contenido': 'Haz click aquí para ganar dinero gratis. http://bit.ly/spam',
            'tiene_enlaces': True,
            'tiene_adjuntos': False,
            'es_spam': 1
        },
        {
            'remitente': 'amigo@correo.com',
            'asunto': 'Reunión mañana',
            'contenido': 'Hola, ¿nos vemos mañana en la oficina?',
            'tiene_enlaces': False,
            'tiene_adjuntos': False,
            'es_spam': 0
        },
        {
            'remitente': 'winner@prize.com',
            'asunto': '¡Felicidades! Eres el ganador',
            'contenido': 'Has sido seleccionado para recibir un premio. http://tinyurl.com/premio',
            'tiene_enlaces': True,
            'tiene_adjuntos': False,
            'es_spam': 1
        },
        {
            'remitente': 'info@empresa.com',
            'asunto': 'Factura de este mes',
            'contenido': 'Adjuntamos la factura correspondiente al mes actual.',
            'tiene_enlaces': False,
            'tiene_adjuntos': True,
            'es_spam': 0
        }
    ]

    detector = SpamDetectorReglas()
    print("Resultados individuales de detección:\n")
    for i, email in enumerate(emails_prueba, 1):
        predicho, puntuacion = detector.es_spam(email)
        print(f"Email {i}:")
        print(f"  Remitente: {email['remitente']}")
        print(f"  Asunto: {email['asunto']}")
        print(f"  Es SPAM real: {email['es_spam']} | Detectado: {int(predicho)} | Puntuación: {puntuacion}")
        print("-" * 50)

    resultados = evaluar_sistema(detector, emails_prueba)
    print("\nResumen de métricas del sistema:")
    print(f"  Precisión: {resultados['precision']:.2f}")
    print(f"  Recall: {resultados['recall']:.2f}")
    print(f"  F1 Score: {resultados['f1_score']:.2f}")
    print(f"  Verdaderos positivos: {resultados['verdaderos_positivos']}")
    print(f"  Falsos positivos: {resultados['falsos_positivos']}")