# rules.py

class Rule:
    def __init__(self, name, condition, action):
        self.name = name
        self.condition = condition
        self.action = action

    def evaluate(self, email_data):
        if self.condition(email_data):
            return self.action(email_data)
        return False

def contains_keyword(keywords):
    def condition(email_data):
        return any(keyword in email_data['contenido'].lower() or keyword in email_data['asunto'].lower() for keyword in keywords)
    
    def action(email_data):
        return True  # Mark as spam

    return Rule("Contains Keyword", condition, action)

def has_suspicious_links():
    def condition(email_data):
        return 'http' in email_data['contenido']  # Simplified check for links
    
    def action(email_data):
        return True  # Mark as spam

    return Rule("Has Suspicious Links", condition, action)

def is_from_suspicious_sender(suspicious_domains):
    def condition(email_data):
        sender_domain = email_data['remitente'].split('@')[-1]
        return any(domain in sender_domain for domain in suspicious_domains)
    
    def action(email_data):
        return True  # Mark as spam

    return Rule("Is From Suspicious Sender", condition, action)

# Example of defining rules
suspicious_domains = ['spam.com', 'malicious.com']
keywords = ['gratis', 'urgente', 'oferta']

rules = [
    contains_keyword(keywords),
    has_suspicious_links(),
    is_from_suspicious_sender(suspicious_domains)
]