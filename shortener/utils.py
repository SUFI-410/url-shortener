import random
import string
from .models import ShortURL


def generate_unique_code(length=6):

    chars = string.ascii_letters + string.digits

    while True:

        code = ''.join(
            random.choice(chars)
            for _ in range(length)
        )

        exists = ShortURL.objects.filter(
            short_code=code
        ).exists()

        if not exists:
            return code
