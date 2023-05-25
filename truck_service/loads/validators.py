import re

from django.core.exceptions import ValidationError


def validate_zip_code(value):
    """Validate zip code."""
    if not re.match(r'\d{5}', value) and not re.match(r'\d{5}-\d{4}', value):
        raise ValidationError(
            "Zip code should be in 99999 or 99999-9999 format"
        )


def validate_truck_uid(value):
    """Validate UID of truck."""
    if not re.match(r'^[1-9]{1}\d{3}[A-Z]{1}$', value):
        raise ValidationError(
            "UID should be in format from 1000A to 9999Z"
        )
