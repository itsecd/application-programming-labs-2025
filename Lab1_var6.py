#Найти всех людей с фамилиями, оканчивающимися на "ов(а)". Выведите их количество на экран и сохраните анкеты в новый файл.
import re
import os
import subprocess
import platform
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Находит всех людей с фамилиями, оканчивающимися на 'ов' или 'ова', и сохраняет их анкеты."
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    return args.filename

def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла '{filename}': {e}")
    
    if not content.strip():
        raise ValueError(f"Файл '{filename}' пуст.")
    return content
    
def parse_entries(content: str) -> list[dict]:
    """Парсит содержимое файла и возвращает список анкет (словарей)."""
    lines = content.strip().split('\n')
    entries = []
    current_entry = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.match(r'^\d+\)', line):  # Начало новой анкеты "перехват 1),2) и т.д"
            if current_entry:
                entries.append(current_entry)
            current_entry = {}
        elif ':' in line:
            try:
                key, value = line.split(':', 1)
                current_entry[key.strip()] = value.strip()
            except ValueError:
                raise ValueError(f"Некорректный формат строки: '{line}'")
            
    if current_entry:
        entries.append(current_entry)
    
    return entries

def filter_by_surname(entries: list[dict], pattern: str = r'^.*ов(?:а)?$') -> list[dict]:
    """Фильтрует анкеты по фамилии, оканчивающейся на 'ов' или 'ова'."""
    def matches_surname(surname: str) -> bool:
        return bool(re.match(pattern, surname, re.IGNORECASE))

    filtered = []
    for entry in entries:
        if 'Фамилия' not in entry:
            raise KeyError("В анкете отсутствует поле 'Фамилия'")
        if matches_surname(entry['Фамилия']):
            filtered.append(entry)
    return filtered


def save_entries_to_file(entries: list[dict], output_filename: str = 'filtered_data.txt') -> None:
    """Сохраняет отфильтрованные анкеты в файл."""
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for i, entry in enumerate(entries, 1):
                f.write(f"{i})\n")
                for key, value in entry.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")
    except Exception as e:
        raise RuntimeError(f"Не удалось сохранить файл '{output_filename}': {e}")

def open_file(filepath: str) -> None:
    """Открывает файл в стандартном приложении ОС."""
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(filepath)
        elif system == "Darwin":  # macOS
            subprocess.call(('open', filepath))
        else:  # Linux и др.
            subprocess.call(('xdg-open', filepath))
    except Exception as e:
        raise RuntimeError(f"Не удалось открыть файл '{filepath}': {e}")

def main():
    
    filename=parse_args()
    
    try:
        content = read_file(filename)

        entries = parse_entries(content)

        filtered_entries = filter_by_surname(entries)
        
        count = len(filtered_entries)
        print("Однофамильцев:", count)

        output_file = 'filtered_data.txt'
        save_entries_to_file(filtered_entries, output_file)

        print(f"Анкеты сохранены в {output_file}.")
        open_file(output_file)

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
        
if __name__ == "__main__":
    import sys
    main()
   