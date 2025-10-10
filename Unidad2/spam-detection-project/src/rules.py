import re

class Rule:
    def __init__(self, name, condition, action):
        self.name = name
        self.condition = condition
        self.action = action

    def evaluate(self, email_data):
        if self.condition(email_data):
            return self.action(email_data)
        return False

def contains_keywords(keywords):
    def condition(email_data):
        contenido = email_data['contenido'].lower()
        return any(keyword in contenido for keyword in keywords)
    def action(email_data):
        return True
    return Rule("Contiene palabras clave", condition, action)

def has_suspicious_links():
    def condition(email_data):
        # Busca patrones de enlaces http, https o www
        return bool(re.search(r'(http[s]?://|www\.)', email_data['contenido'].lower()))
    def action(email_data):
        return True
    return Rule("Contiene enlaces sospechosos", condition, action)

def has_money_offer():
    def condition(email_data):
        contenido = email_data['contenido'].lower()
        # Busca ofertas de dinero, premios o sorteos
        return bool(re.search(r'(prize|win|winner|cash|award|guaranteed|claim|selected|congratulations|£|\$|\beuros?\b|\bpounds?\b)', contenido))
    def action(email_data):
        return True
    return Rule("Ofrece dinero o premios", condition, action)

def has_urgent_language():
    def condition(email_data):
        contenido = email_data['contenido'].lower()
        # Busca lenguaje urgente o presión para actuar
        return any(word in contenido for word in ['urgent', 'act now', 'final notice', 'limited time', 'only today', 'last chance', 'reply now'])
    def action(email_data):
        return True
    return Rule("Lenguaje urgente", condition, action)

def has_numeric_shortcode():
    def condition(email_data):
        # Busca códigos cortos numéricos típicos de SMS premium
        return bool(re.search(r'\b\d{4,6}\b', email_data['contenido']))
    def action(email_data):
        return True
    return Rule("Contiene shortcode numérico", condition, action)

def has_excessive_caps():
    def condition(email_data):
        # Detecta si hay muchas palabras en mayúsculas (más de 5)
        return len(re.findall(r'\b[A-Z]{3,}\b', email_data['contenido'])) > 5
    def action(email_data):
        return True
    return Rule("Exceso de mayúsculas", condition, action)

# Palabras clave ampliadas para spam.csv
keywords = [
    'free', 'win', 'prize', 'winner', 'cash', 'claim', 'urgent', 'guaranteed', 'award', 'selected',
    'congratulations', 'offer', 'special', 'membership', 'txt', 'text', 'call', 'reply', 'now', 'click',
    'subscription', 'ringtone', 'voucher', 'bonus', 'gift', 'promo', 'exclusive', 'discount'
]

rules = [
    contains_keywords(keywords),
    has_suspicious_links(),
    has_money_offer(),
    has_urgent_language(),
    has_numeric_shortcode(),
    has_excessive_caps()
]