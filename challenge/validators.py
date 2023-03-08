import re

def valid_country(string):
    model = '^[A-Za-z ]*$'
    response = re.findall(model, string)
    return response

def valid_idno(string):
    return string.isnumeric()

def valid_score(score):
    if 0 <= score <= 100:
        return True
    return False