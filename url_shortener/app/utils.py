import string
import random

ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length: int = 6) -> str:
    """Rastgele ve benzersiz bir kısa kod üretir."""
    return ''.join(random.choices(ALPHABET, k=length))
