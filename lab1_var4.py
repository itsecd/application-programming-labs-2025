def read_profiles():
    """Считывание анкеток"""
    profiles = []

    try:
        with open('data.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        """Рзделяет на блоки по двойному переносу"""
        profile_blocks = content.split('\n\n')

        for block in profile_blocks:
            lines = block.strip().split('\n') 
            """Разделяет на блоки по переносу строки"""
            if len(lines) >= 6:
                profile = {
                    'surname': lines[1].strip().split(": ")[-1],
                    'name': lines[2].strip().split(": ")[-1],
                    'gender': lines[3].strip().split(": ")[-1],
                    'birth_date': lines[4].strip().split(": ")[-1],
                    'contact': lines[5].strip().split(": ")[-1],
                    'city': lines[6].strip().split(": ")[-1]
                }
                """Сохраняет это в profiles как строку, split'ом выделяем только данные человека"""
                profiles.append(profile)

    except FileNotFoundError:
        print("Ошибка")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

    return profiles


def extract_year(birth_date_str):
    """Извлекает год из даты рождения (простая версия)"""
    import re
    year_match = re.search(r'\b(\d{4})\b', birth_date_str)
    if year_match:
        return int(year_match.group(1))
    return None


def find_oldest_and_youngest(profiles):
    """Находит самого старого и самого молодого человека по году рождения"""
    if not profiles:
        return None, None
    valid_profiles = []
    for profile in profiles:
        year = extract_year(profile['birth_date'])
        if year and 1900 <= year <= 2025:  # Простая проверка года
            valid_profiles.append(profile)

    if not valid_profiles:
        return None, None

    """Сортировка только по дате"""
    sorted_profiles = sorted(valid_profiles, key=lambda x: extract_year(x['birth_date']))

    oldest = sorted_profiles[0]  # Самый маленький год = самый старый
    youngest = sorted_profiles[-1]  # Самый большой год = самый молодой

    return oldest, youngest


def print_profile(profile, label):
    """Вывод анкет"""
    print(f"\n{label}:")
    print(f"Фамилия: {profile['surname']}")
    print(f"Имя: {profile['name']}")
    print(f"Пол: {profile['gender']}")
    print(f"Дата рождения: {profile['birth_date']}")
    print(f"Контакт: {profile['contact']}")
    print(f"Город: {profile['city']}")

    """Вычисляем возраст"""
    year = extract_year(profile['birth_date'])
    if year:
        age = 2025 - year
        print(f"Примерный возраст: {age} лет")


def main():
    # Читаем анкеты из файла
    profiles = read_profiles()

    if not profiles:
        print("Не удалось прочитать анкеты из файла data.txt")
        return

    print(f"Всего прочитано анкет: {len(profiles)}")

    # Находим самого старого и самого молодого
    oldest, youngest = find_oldest_and_youngest(profiles)

    if oldest is None or youngest is None:
        print("Не найдено анкет с валидной датой рождения")
        return

    # Выводим результаты
    print("\n" + "=" * 50)
    print_profile(oldest, "САМЫЙ СТАРЫЙ ЧЕЛОВЕК")
    print_profile(youngest, "САМЫЙ МОЛОДОЙ ЧЕЛОВЕК")

    # Сохраняем результаты в файл
    with open('result_variant4.txt', 'w', encoding='utf-8') as f:
        f.write("РЕЗУЛЬТАТЫ ПОИСКА САМОГО СТАРОГО И САМОГО МОЛОДОГО ЧЕЛОВЕКА\n")
        f.write("=" * 60 + "\n\n")

        f.write("САМЫЙ СТАРЫЙ ЧЕЛОВЕК:\n")
        f.write(f"Фамилия: {oldest['surname']}\n")
        f.write(f"Имя: {oldest['name']}\n")
        f.write(f"Пол: {oldest['gender']}\n")
        f.write(f"Дата рождения: {oldest['birth_date']}\n")
        f.write(f"Контакт: {oldest['contact']}\n")
        f.write(f"Город: {oldest['city']}\n\n")

        f.write("САМЫЙ МОЛОДОЙ ЧЕЛОВЕК:\n")
        f.write(f"Фамилия: {youngest['surname']}\n")
        f.write(f"Имя: {youngest['name']}\n")
        f.write(f"Пол: {youngest['gender']}\n")
        f.write(f"Дата рождения: {youngest['birth_date']}\n")
        f.write(f"Контакт: {youngest['contact']}\n")
        f.write(f"Город: {youngest['city']}\n")


if __name__ == "__main__":
    main()
