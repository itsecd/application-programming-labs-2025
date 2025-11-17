import re   
import sys
from typing import List, Dict, Any, Optional, Set


def read_data_file(file_path: str) -> List[str]:

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def extract_email(text: str) -> Optional[str]:

    email_pattern = r'[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)'
    match = re.search(email_pattern, text)
    if match:
        return match.group().lower()
    return None


def parse_profiles(lines: List[str]) -> List[Dict[str, Any]]:

    profiles: List[Dict[str, Any]] = []
    current_profile: Dict[str, Any] = {}

    for line in lines:
        line = line.strip()

        if not line:
            if current_profile:
                profiles.append(current_profile)
                current_profile = {}
            continue

        email = extract_email(line)
        if email:
            current_profile['email'] = email

        current_profile['raw_data'] = current_profile.get('raw_data', []) + [line]

    if current_profile:
        profiles.append(current_profile)

    return profiles


def find_duplicate_emails(profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    email_count: Dict[str, int] = {}
    duplicate_emails: Set[str] = set()

    for profile in profiles:
        if 'email' in profile:
            email = profile['email']
            email_count[email] = email_count.get(email, 0) + 1
            if email_count[email] > 1:
                duplicate_emails.add(email)

    duplicate_profiles: List[Dict[str, Any]] = []
    for profile in profiles:
        if 'email' in profile and profile['email'] in duplicate_emails:
            duplicate_profiles.append(profile)

    return duplicate_profiles


def print_results(duplicate_profiles: List[Dict[str, Any]]) -> None:

    if not duplicate_profiles:
        print("\nДублирующихся email не найдено - все email уникальны!")
        return

    print("\nНайдены анкеты с дублирующимися email:")


    email_groups: Dict[str, List[Dict[str, Any]]] = {}
    for profile in duplicate_profiles:
        email = profile['email']
        if email not in email_groups:
            email_groups[email] = []
        email_groups[email].append(profile)

    for email, profiles_list in email_groups.items():
        print(f"\nEmail: {email}")
        print(f"Количество дубликатов: {len(profiles_list)}")


        for i, profile in enumerate(profiles_list, 1):
            print(f"Дубликат {i}:")
            for line in profile['raw_data']:
                print(f"  {line}")
            print()


def main() -> None:

    if len(sys.argv) != 2:
        print("Использование: python lab1.py <путь_к_файлу>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        lines = read_data_file(file_path)
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    profiles = parse_profiles(lines)

    if not profiles:
        print("В файле не найдено анкет")
        return

    print(f"Всего найдено анкет: {len(profiles)}")

    duplicate_profiles = find_duplicate_emails(profiles)

    print_results(duplicate_profiles)


if __name__ == "__main__":
    main()
