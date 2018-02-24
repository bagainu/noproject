from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# validate string format of email
def is_email_format(email_address):
    try:
        validate_email(email_address)
    except ValidationError:
        return False
    return True

    