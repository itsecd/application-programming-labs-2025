import re
import argparse
from typing import List, Dict, Tuple


def read_file(filename: str) -> List[str]:
    """
    Читает файл и возвращает список строк.
    
    Args:
        filename (str): Имя файла для чтения
        
    Returns:
        List[str]: Список строк файла
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Файл {filename} не найден") from exc
    except IOError as exc:
        raise IOError(f"Ошибка чтения файла {filename}") from exc


def extract_emails_from_file(filename: str) -> List[str]:
    """
    Извлекает валидные email адреса из файла с анкетами.
    
    Args:
        filename (str): Имя файла для анализа
        
    Returns:
        List[str]: Список найденных email адресов
    """
    lines = read_file(filename)
    emails = []
    
    # Строгое регулярное выражение по ТЗ
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
    """
    Извлекает домены из списка email адресов.
    
    Args:
        emails (List[str]): Список email адресов
        
    Returns:
        List[str]: Список доменов
    """
    domains = []
    for email in emails:
        if '@' in email:
            domain = email.split('@')[1].strip().lower()
            domains.append(domain)
    return domains


def count_domains(domains: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество каждого домена.
    
    Args:
        domains (List[str]): Список доменов
        
    Returns:
        Dict[str, int]: Словарь с количеством каждого домена
    """
    domain_count = {}
    for domain in domains:
        if domain in domain_count:
            domain_count[domain] += 1
        else:
            domain_count[domain] = 1
    return domain_count


def sort_domains_by_count(domain_count: Dict[str, int]) -> List[Tuple[str, int]]:
    """
    Сортирует домены по количеству в убывающем порядке.
    
    Args:
        domain_count (Dict[str, int]): Словарь с количеством доменов
        
    Returns:
        List[Tuple[str, int]]: Отсортированный список кортежей
    """
    return sorted(domain_count.items(), key=lambda x: x[1], reverse=True)


def save_domain_statistics(sorted_domains: List[Tuple[str, int]], 
                          output_filename: str = 'domain_stats.txt') -> None:
    """
    Сохраняет статистику по доменам в файл.
    
    Args:
        sorted_domains (List[Tuple[str, int]]): Отсортированный список доменов
        output_filename (str): Имя выходного файла
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("Домен: количество\n")
            for domain, count in sorted_domains:
                file.write(f"{domain}: {count}\n")
        print(f"Статистика сохранена в файл: {output_filename}")
    except IOError as exc:
        raise IOError(f"Ошибка при сохранении файла {output_filename}") from exc


def print_domain_statistics(sorted_domains: List[Tuple[str, int]]) -> None:
    """
    Выводит статистику по доменам на экран.
    
    Args:
        sorted_domains (List[Tuple[str, int]]): Отсортированный список доменов
    """
    if not sorted_domains:
        print("Валидные email адреса не найдены")
        return
        
    print("\nСтатистика по доменам:")
    for domain, count in sorted_domains:
        print(f"{domain}: {count}")


def main() -> None:
    """
    Основная функция программы.
    """
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(description='Анализ доменов email в файле данных')
    parser.add_argument('filename', type=str, help='Имя входного файла с данными')
    
    try:
        # Парсинг аргументов
        args = parser.parse_args()
        
        print(f"Анализ файла: {args.filename}")
        
        # Извлекаем email адреса
        emails = extract_emails_from_file(args.filename)
        print(f"Найдено валидных email адресов: {len(emails)}")
        
        if not emails:
            print("В файле не найдено валидных email адресов")
            return
        
        # Извлекаем домены
        domains = extract_domains(emails)
        
        # Считаем статистику
        domain_count = count_domains(domains)
        sorted_domains = sort_domains_by_count(domain_count)
        
        # Выводим результаты
        print_domain_statistics(sorted_domains)
        
        # Сохраняем в файл
        save_domain_statistics(sorted_domains)
        
    except Exception as exc:
        print(f"Произошла ошибка: {exc}")


if __name__ == "__main__":
    main()
