import random
import string

class PasswordGenerator:
    def generate(self, length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
        characters = ""
        if use_upper: characters += string.ascii_uppercase
        if use_lower: characters += string.ascii_lowercase
        if use_digits: characters += string.digits
        if use_special: characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not characters:
            raise ValueError("At least one character type must be selected")
        
        return ''.join(random.choice(characters) for _ in range(length))