def strength_checker(password: str):
    import string


    strength = 0

    length_criteria = len(password) >= 8
    upper_criteria = lower_criteria = digit_criteria = special_criteria = False

    for ch in password:
        if ch.isupper():
            upper_criteria = True
        if ch.islower():
            lower_criteria = True
        if ch.isdigit():
            digit_criteria = True
        if ch in string.punctuation:
            special_criteria = True

    if length_criteria:
        strength += 1
    if upper_criteria:
        strength += 1
    if lower_criteria:
        strength += 1
    if digit_criteria:
        strength += 1
    if special_criteria:
        strength += 1

 
    if strength == 5:
        return "Strong password"
    elif 3 <= strength < 5:
        return "Moderate password"
    else:
        return "Weak password"


def generate_password(length=8):
    import random
    import string

    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(random.choice(characters) for _ in range(length))

        if strength_checker(password) == "Strong password":
           
            return password


