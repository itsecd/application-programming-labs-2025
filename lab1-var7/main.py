import re

def is_valid_phone(phone: str) -> bool:
    '''
    проверка валидности номера телефона с кодом 927
    +7 927 345 67 89
    8 (927) 345-67-89
    89273456789
    '''
    pattern = r'^(?:\+7|8)\s*\(?927\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
    match = re.search(pattern, phone)
    return bool(match)

if __name__ == "__main__":
    test_numbers = [
        "89273456789",
        "+7 927 345 67 89", 
        "8 (927) 345-67-89",
        "89373456789"
    ]
    for num in test_numbers:
        print(f"{num}: {is_valid_phone(num)}")
