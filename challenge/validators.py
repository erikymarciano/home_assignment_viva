import re

def only_letters(string):
    return string.isalpha()

def only_numbers(string):
    return string.isnumeric()

def valid_birth(date_birth):
    """ Verify if is a valid date 0000-00-00"""
    model = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    response = re.findall(model, date_birth)
    return response

def valid_gender(gender):
    """ Verify if is a valid gender M or F """
    if gender == "M" or gender == "F":
        return True
    return False
