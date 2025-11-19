def extract_gender_entries(lines, target_gender='Мужской'):
    """
    Находит анкеты по полу и считает их,также сделаны
    валидные форматы для мужского пола: М, м, Мужской, мужской.
    """

    male_entries = []
    current_entry = []
    is_male = False
    entry_count = 0

    male_pattern = re.compile(r'^Пол:\s*(Мужской|мужской|М|м)\b')

    for line in lines:
        if not line:  
            if current_entry and is_male:
                male_entries.append('\n'.join(current_entry))
                entry_count += 1
            current_entry = []
            is_male = False
        else:
            current_entry.append(line)
            if male_pattern.search(line):
                is_male = True

    if current_entry and is_male:
        male_entries.append('\n'.join(current_entry))
        entry_count += 1

    return entry_count, male_entries
