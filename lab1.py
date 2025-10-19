import re
import argparse
from typing import List, Dict, Tuple


def read_file(filename: str) -> List[str]:
    """Читает файл и возвращает список строк."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Файл {filename} не найден") from exc
    except IOError as exc:
        raise IOError(f"Ошибка чтения файла {filename}") from exc


def extract_emails_from_file(filename: str) -> List[str]:
    """Извлекает валидные email адреса из файла."""
    lines = read_file(filename)
    emails = []
    
    email_pattern = r'[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)'
    
    for line in lines:
        line = line.strip()
        if line.startswith('Номер телефона или email:'):
            contact_info = line.split(':', 1)[1].strip()
            email_match = re.search(email_pattern, contact_info)
            if email_match:
                emails.append(email_match.group())
    
    return emails


def extract_domains(emails: List[str]) -> List[str]:
    """Извлекает домены из email адресов."""
    domains = []
    for email in emails:
        if '@' in email:
            domain = email.split('@')[1].strip().lower()
            domains.append(domain)
    return domains


def count_domains(domains: List[str]) -> Dict[str, int]:
    """Подсчитывает количество каждого домена."""
    domain_count = {}
    for domain in domains:
        if domain in domain_count:
            domain_count[domain] += 1
        else:
            domain_count[domain] = 1
    return domain_count


def sort_domains_by_count(domain_count: Dict[str, int]) -> List[Tuple[str, int]]:
    """Сортирует домены по количеству."""
    return sorted(domain_count.items(), key=lambda x: x[1], reverse=True)


def save_domain_statistics(sorted_domains: List[Tuple[str, int]], 
                          output_filename: str = 'domain_stats.txt') -> None:
    """Сохраняет статистику по доменам в файл."""
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("Домен: количество\n")
            for domain, count in sorted_domains:
                file.write(f"{domain}: {count}\n")
        print(f"Статистика сохранена в файл: {output_filename}")
    except IOError as exc:
        raise IOError(f"Ошибка при сохранении файла {output_filename}") from exc


def print_domain_statistics(sorted_domains: List[Tuple[str, int]]) -> None:
    """Выводит статистику по доменам на экран."""
    if not sorted_domains:
        print("Валидные email адреса не найдены")
        return
        
    print("\nСтатистика по доменам:")
    for domain, count in sorted_domains:
        print(f"{domain}: {count}")


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(description='Анализ доменов email в файле данных')
    parser.add_argument('filename', type=str, help='Имя входного файла с данными')
    
    try:
        args = parser.parse_args()
        
        print(f"Анализ файла: {args.filename}")
        
        emails = extract_emails_from_file(args.filename)
        print(f"Найдено валидных email адресов: {len(emails)}")
        
        if not emails:
            print("В файле не найдено валидных email адресов")
            return
        
        domains = extract_domains(emails)
        domain_count = count_domains(domains)
        sorted_domains = sort_domains_by_count(domain_count)
        
        print_domain_statistics(sorted_domains)
        save_domain_statistics(sorted_domains)
        
    except Exception as exc:
        print(f"Произошла ошибка: {exc}")


if __name__ == "__main__":
    main()
