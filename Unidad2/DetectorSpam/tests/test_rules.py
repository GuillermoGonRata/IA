import unittest
from src.rules import some_rule_function  # Remplaza con la función real a probar

class TestSpamDetectionRules(unittest.TestCase):

    def test_some_rule_function(self):
        # caso de prueba para una función de regla específica
        input_data = {
            'remitente': 'test@example.com',
            'asunto': 'Congratulations! You have won a prize!',
            'contenido': 'Click here to claim your free gift!',
            'tiene_enlaces': True,
            'tiene_adjuntos': False
        }
        expected_output = True  # salida esperada basada en la lógica de la regla
        self.assertEqual(some_rule_function(input_data), expected_output)

    def test_another_rule_function(self):
        # Otra prueba para otra función de regla
        input_data = {
            'remitente': 'legit@example.com',
            'asunto': 'Meeting Reminder',
            'contenido': 'Don\'t forget our meeting tomorrow.',
            'tiene_enlaces': False,
            'tiene_adjuntos': False
        }
        expected_output = False  # salida esperada basada en la lógica de la regla
        self.assertEqual(some_rule_function(input_data), expected_output)

if __name__ == '__main__':
    unittest.main()