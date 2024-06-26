
import random
import string
from api.models import Organization


def generate_code(length):
    """Generate a random alphanumeric code."""
    while True:
        code = code_artisan(length)
        if not Organization.objects.filter(code=code).exists():
            code = code_artisan(length)
            break
    return code

def code_artisan(length):
    """Generate a random alphanumeric string of given length."""
    code = "ORG_" + ''.join(random.choices(string.ascii_uppercase, k=length))
    return code