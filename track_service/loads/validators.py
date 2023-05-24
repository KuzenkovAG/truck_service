import re

from django.core.exceptions import ValidationError


def validate_zip_code(value):
    if not re.match(r'\d{5}', value) and not re.match(r'\d{5}-\d{4}', value):
        raise ValidationError(
            "Zip code should be in 99999 or 99999-9999 format"
        )
