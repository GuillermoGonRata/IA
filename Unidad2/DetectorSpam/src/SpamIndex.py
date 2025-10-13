import os
import re
import pandas as pd
from urllib.parse import urlparse
import random


    
class SpamDetectorReglas:       #Clase que implementa un detector de spam basado en reglas simples.
    #Evalúa remitente, asunto, enlaces y contenido para asignar una puntuación de spam.
    
    def __init__(self):  #Inicializa las listas de dominios sospechosos y palabras clave de spam.
        self.dominios_sospechosos = ['promo', 'offer', 'free', 'winner', 'prize']
        self.palabras_clave_spam = [
            'gratis', 'ganador', 'urgente', 'oferta', 'promoción',
            'descuento', 'dinero', 'millonario', 'click aquí', 'free', 'win', 'prize', 'winner', 'cash', 'claim'
        ]
        
        #Inicializa las listas de dominios sospechosos y palabras clave de spam.
        
    



    def analizar_remitente(self, email):
        #Analiza el dominio del remitente para detectar palabras sospechosas.
        #Args:
        #    email (str): Dirección de correo electrónico del remitente.
        #Returns:
        #    int: Puntuación asignada al remitente.
        
        dominio = email.split('@')[-1] if '@' in email and email else ''
        puntuacion = 0
        for dominio_sos in self.dominios_sospechosos:
            if dominio_sos in dominio.lower():
                puntuacion += 2
        return puntuacion
    
    def analizar_asunto(self, asunto):
        
        
        #Analiza el asunto del correo buscando palabras clave y patrones sospechosos.
        #Args:
        #    asunto (str): Asunto del correo.
        #Returns:
        #    int: Puntuación asignada al asunto.
        
        puntuacion = 0
        asunto_lower = asunto.lower() if asunto else ''
        for palabra in self.palabras_clave_spam:
            if palabra in asunto_lower:
                puntuacion += 1
        if re.search(r'[!]{2,}', asunto_lower):
            puntuacion += 1
        if re.search(r'\b(100%|gratis|urgente|free|win|prize|winner|cash|claim)\b', asunto_lower):
            puntuacion += 2
        return puntuacion
    
    def analizar_enlaces(self, contenido):
        
        #Busca enlaces en el contenido y evalúa si son sospechosos (acortadores o IPs).
        #Args:
        #    contenido (str): Cuerpo del mensaje.
        #Returns:
        #    int: Puntuación asignada por enlaces sospechosos (máximo 5).
        
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', contenido)
        puntuacion = 0
        for url in urls:
            dominio = urlparse(url).netloc.lower()
            if any(acortador in dominio for acortador in ['bit.ly', 'tinyurl', 'goo.gl']):
                puntuacion += 2
            if re.match(r'\d+\.\d+\.\d+\.\d+', dominio):
                puntuacion += 3
        return min(puntuacion, 5)
    
    def analizar_contenido(self, contenido):
        
        # Analiza el contenido buscando palabras clave y patrones urgentes.
        #Args:
        #contenido (str): Cuerpo del mensaje.
        #Returns:
        #    int: Puntuación asignada al contenido.

        contenido_lower = contenido.lower()
        puntuacion = 0
        palabras_encontradas = sum(1 for palabra in self.palabras_clave_spam if palabra in contenido_lower)
        puntuacion += min(palabras_encontradas, 3)
        if re.search(r'\b(urgente|inmediato|ahora mismo|free|win|prize|winner|cash|claim)\b', contenido_lower):
            puntuacion += 2
        return puntuacion
    
    def es_spam(self, email_data):
        
        #Evalúa un correo electrónico y determina si es spam según la puntuación total.
        #Args:
        #    email_data (dict): Diccionario con las claves 'remitente', 'asunto' y 'contenido'.
        #Returns:
        #    tuple: (bool, int) donde el primer valor indica si es spam y el segundo la puntuación total.
        
        puntuacion_total = 0
        puntuacion_total += self.analizar_remitente(email_data['remitente'])
        puntuacion_total += self.analizar_asunto(email_data['asunto'])
        puntuacion_total += self.analizar_enlaces(email_data['contenido'])
        puntuacion_total += self.analizar_contenido(email_data['contenido'])
        return puntuacion_total >= 3, puntuacion_total

def adaptar_spam_csv(df):
    #Adapta un DataFrame de spam.csv al formato esperado por el detector.
    #Args:
    #   df (pd.DataFrame): DataFrame original con columnas 'Category' y 'Message'.
    #Returns:
    #    pd.DataFrame: DataFrame adaptado con columnas estándar.
    
    df = df.rename(columns={'Category': 'es_spam', 'Message': 'contenido'})
    df['es_spam'] = df['es_spam'].map({'spam': 1, 'ham': 0})
    df['remitente'] = ''  # No hay remitente en spam.csv
    df['asunto'] = ''     # No hay asunto en spam.csv
    df['tiene_enlaces'] = df['contenido'].str.contains('http|www', case=False)
    df['tiene_adjuntos'] = False
    columnas = ['remitente', 'asunto', 'contenido', 'tiene_enlaces', 'tiene_adjuntos', 'es_spam']
    return df[columnas]

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'spam.csv')
    df = pd.read_csv(data_path, encoding='latin-1')
    df = adaptar_spam_csv(df)
    detector = SpamDetectorReglas()

    # Seleccionar aleatoriamente hasta 100 mensajes para mostrar
    sample_df = df.sample(n=min(1, len(df)), random_state=42)

    print("Resultados individuales de detección en una muestra de spam.csv:\n")
    for i, row in sample_df.iterrows():
        email = row.to_dict()
        predicho, puntuacion = detector.es_spam(email)
        print(f"Mensaje {i+1}:")
        print(f"  Contenido: {email['contenido']}")
        print(f"  Es SPAM real: {email['es_spam']} | Detectado: {int(predicho)} | Puntuación: {puntuacion}")
        if puntuacion >= 3:
            print("  Este mensaje es SPAM o es muy probable que sea SPAM.")
        elif puntuacion == 2:
            print("  Este mensaje podría ser SPAM, revisar con precaución.")
        else:
            print("  Este mensaje parece legítimo.")
        print("-" * 50)