import re
from typing import List, Tuple


def format_phone_number(phone_line: str, clean_pattern: str) -> str:
    """Форматирует номер телефона в стандартный вид: +7(XXX)XXX-XX-XX"""
    clean_phone = re.sub(clean_pattern, '', phone_line)
    if len(clean_phone) == 11:
        if clean_phone.startswith('8'):
            formatted_phone = f"+7({clean_phone[1:4]}){clean_phone[4:7]}-{clean_phone[7:9]}-{clean_phone[9:]}"
        else:
            formatted_phone = f"+7({clean_phone[1:4]}){clean_phone[4:7]}-{clean_phone[7:9]}-{clean_phone[9:]}"
    else:
        formatted_phone = phone_line
    return formatted_phone


def extract_phonebook_data(lines: List[str]) -> List[Tuple[str, str]]:
    """Извлекает фамилии и номера телефонов из списка строк"""
    surname_pattern = r'^Фамилия:\s*([А-ЯЁ][а-яё]*)$'
    phone_pattern = r'^(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
    clean_phone_pattern = r'[^\d]'
    
    result: List[Tuple[str, str]] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        surname_match = re.match(surname_pattern, line)

        if surname_match:
            surname = surname_match.group(1)
            print(f"Найдена фамилия: {surname}")

            j = i + 1
            phone_found = False
            while j < min(i + 10, len(lines)) and not phone_found:
                phone_line = lines[j].strip()

                if phone_line.startswith('Номер телефона или email:'):
                    phone_value = phone_line.split(':', 1)[1].strip()
                    print(f"Найден телефон: '{phone_value}'")

                    if re.match(phone_pattern, phone_value):
                        print("Телефон валиден!")
                        formatted_phone = format_phone_number(phone_value, clean_phone_pattern)
                        result.append((surname, formatted_phone))
                        phone_found = True
                    else:
                        print("Это не валидный телефон (возможно email)")
                    break
                j += 1
            i = j + 1 if phone_found else i + 1
        else:
            i += 1

    print(f"Всего найдено валидных записей: {len(result)}")
    return result
