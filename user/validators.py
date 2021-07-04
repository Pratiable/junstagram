import re

REGEX = {
    'email'        : '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'password'     : '[A-Za-z0-9@#$%^&+=]{8,}',
    'name'         : '''^([A-Z][a-z]+([ ]?[a-z]?['-]?[A-Z][a-z]+)*)$|^[가-힣]{2,}''', 
    'phone_number' : '^[0-9]{3}[-]+[0-9]{3,4}[-]+[0-9]{4}$'
}

def validate_email(email): 
    return re.search(REGEX['email'], email)

def validate_password(password):
    return re.search(REGEX['password'], password)

def validate_name(name):
    return re.search(REGEX['name'], name)

def validate_phone_number(phone_number):
    return re.search(REGEX['phone_number'], phone_number)