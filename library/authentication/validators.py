from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from authentication.constants import MAX_EMAIL_CHARACTERS, MAX_NAME_CHARACTERS, MAX_BOOK_NAME, MAX_BOOK_DESCRIPTION


def valid_bio_info(*args):
    for arg in args:

        if arg and len(arg) > MAX_NAME_CHARACTERS:
            raise ValidationError

    else:
        return True


def valid_email(email):
    try:
        validate_email(email)

        if len(email) > MAX_EMAIL_CHARACTERS:
            raise ValidationError
    
    except ValidationError:
        raise

    else:
        return True


def valid_book_info(book_name=None, book_description=None, count=10):
    if book_name and len(book_name) > MAX_BOOK_NAME:
        raise ValidationError

    if book_description and len(book_description) > MAX_BOOK_DESCRIPTION:
        raise ValidationError

    if count < 0:
        raise ValidationError

    return True

