import re
import sys

def is_valid_surname(surname):
    # Только кириллица, первая — заглавная, остальные — строчные
    return bool(re.fullmatch(r'[А-ЯЁ][а-яё]*', surname))

def normalize_phone(raw):
    # Удаляем всё кроме цифр
    digits = re.sub(r'\D', '', raw)
    
    # Должно быть 11 цифр, начинаться с 8 или 7
    if len(digits) == 11 and (digits.startswith('8') or digits.startswith('7')):
        if digits.startswith('7'):
            digits = '8' + digits[1:]
        return f"8 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return None

def is_email(contact):
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@(?:gmail\.com|mail\.ru|yandex\.ru)$')
    return bool(email_pattern.match(contact.strip()))

def main():
    if len(sys.argv) != 2:
        print("Использование: python3 lab.py <файл_с_анкетами>")
        return

    input_file = sys.argv[1]
    output_file = "result.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
        return

    # Удаляем номера вроде "1)", "2)" и пустые строки
    content = re.sub(r'^\s*\d+\)\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n\s*\n', '\n\n', content)  # нормализуем пустые строки

    # Ищем все блоки, содержащие "Фамилия:"
    blocks = re.findall(r'Фамилия:.*?(?=\n\s*Фамилия:|\Z)', content, re.DOTALL)

    print(f"Найдено блоков: {len(blocks)}")  # Отладка

    results = []

    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        data = {}
        for line in lines:
            if ':' in line:
                key, val = line.split(':', 1)
                data[key.strip()] = val.strip()

        surname = data.get("Фамилия", "")
        contact = data.get("Номер телефона или email", "")

        if not re.fullmatch(r'[А-ЯЁ][а-яё]*', surname):
            continue

        if is_email(contact):
            continue

        normalized = normalize_phone(contact)
        if normalized:
            results.append(f"{surname}: {normalized}")

    # ... остальное без изменений

    # Сохраняем и выводим
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')

    if results:
        for line in results:
            print(line)
    else:
        print("Нет валидных записей.")

if __name__ == "__main__":
    main()
