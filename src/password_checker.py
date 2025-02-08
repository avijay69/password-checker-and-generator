import re

class PasswordChecker:
    def __init__(self):
        self.breached_passwords = ["123456", "password", "123456789", "password123"]  # Add more breached passwords as needed

    def calculate_strength(self, password):
        if not password:
            return None

        length_score = min(len(password), 10) * 10  # Cap length score at 100
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

        # Ensure all criteria are met for a strong password
        if has_upper and has_lower and has_digit and has_symbol and len(password) >= 10:
            strength_value = length_score
            strength_text = "Very Strong"
        elif has_upper and has_lower and has_digit and has_symbol and len(password) >= 8:
            strength_value = length_score * 0.9
            strength_text = "Strong"
        elif (has_upper and has_lower and has_digit) or (has_upper and has_lower and has_symbol) or (has_lower and has_digit and has_symbol):
            strength_value = length_score * 0.75
            strength_text = "Medium"
        else:
            strength_value = length_score * 0.5
            strength_text = "Weak"

        return strength_text, strength_value

    def check_breach(self, password):
        return password in self.breached_passwords