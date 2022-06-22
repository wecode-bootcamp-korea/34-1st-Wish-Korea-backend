import re

from django.core.exceptions import ValidationError

def username_validate(username):
    if not username:
        raise ValidationError(message = 'Invalid_Username')
         
def email_validate(email):
    EMAIL_REGEX  = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.match(EMAIL_REGEX, email):
        raise ValidationError(message = 'Invalid_Email')
        
def password_validate(password):
    PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

    if not re.match(PASSWORD_REGEX, password):
        raise ValidationError(message = 'Invalid_Password')

def phone_number_validate(phone_number):
    PHONE_NUMBER_REGEX  = '\d{3}-\d{3,4}-\d{4}'

    if not re.match(PHONE_NUMBER_REGEX ,phone_number):
        raise ValidationError(message = 'Invalid_PhoneNumber')

def url_validate(value):
    URL_REGEX = '^https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_/=.?]*'

    if not re.match(URL_REGEX, value):
        raise ValidationError(message = 'Invalid_Url')