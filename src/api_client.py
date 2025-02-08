import hashlib
import requests

class PwnedAPI:
    def __init__(self):
        self.base_url = "https://api.pwnedpasswords.com/range/"

    def is_password_breached(self, password):
        # Hash the password using SHA-1
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]

        # Fetch hashes from API
        try:
            response = requests.get(f"{self.base_url}{prefix}", timeout=5)
            if response.status_code == 200:
                hashes = (line.split(":") for line in response.text.splitlines())
                return any(suffix in h for h, _ in hashes)
            return False  # Assume safe if API fails
        except requests.exceptions.RequestException:
            return False  # Offline mode