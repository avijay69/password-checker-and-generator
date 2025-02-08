from password_checker import PasswordChecker

checker = PasswordChecker()
test_passwords = [
    "123",          # Weak
    "Password123",  # Medium
    "P@ssw0rd!",    # Strong
    "A$5vF^q9X*"    # Very Strong
]

for pwd in test_passwords:
    strength, score = checker.calculate_strength(pwd)
    print(f"Password: {pwd} → {strength} ({score}%)")