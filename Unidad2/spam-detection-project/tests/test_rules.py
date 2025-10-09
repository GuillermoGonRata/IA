import unittest
from src.rules import some_rule_function  # Replace with actual function names from rules.py

class TestSpamDetectionRules(unittest.TestCase):

    def test_some_rule_function(self):
        # Test case for the rule function
        input_data = {
            'remitente': 'test@example.com',
            'asunto': 'Congratulations! You have won a prize!',
            'contenido': 'Click here to claim your free gift!',
            'tiene_enlaces': True,
            'tiene_adjuntos': False
        }
        expected_output = True  # Expected output based on the rule logic
        self.assertEqual(some_rule_function(input_data), expected_output)

    def test_another_rule_function(self):
        # Another test case for a different rule function
        input_data = {
            'remitente': 'legit@example.com',
            'asunto': 'Meeting Reminder',
            'contenido': 'Don\'t forget our meeting tomorrow.',
            'tiene_enlaces': False,
            'tiene_adjuntos': False
        }
        expected_output = False  # Expected output based on the rule logic
        self.assertEqual(some_rule_function(input_data), expected_output)

if __name__ == '__main__':
    unittest.main()