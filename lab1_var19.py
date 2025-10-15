import argparse
import re
from pathlib import Path
from typing import List, Pattern, Optional, Tuple


def build_email_regex(allowed_domains: List[str]) -> Pattern[str]:
    """Создаёт регулярное выражение для проверки корректности email."""
    dom_part = "|".join(re.escape(d) for d in allowed_domains)
    pattern = rf"^[A-Za-z0-9._%+\-]{{1,64}}@(?:{dom_part})$"
    return re.compile(pattern, re.IGNORECASE)


def arg_parse() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Найдите адреса почты с некорректным форматом."
    )
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", type=str, default="result.txt", help="Output file")
    parser.add_argument("--domains", nargs="+", default=["gmail.com", "mail.ru", "yandex.ru"])
    parser.add_argument("--encoding", default="utf-8")

    return parser.parse_args()


def read_file(path: Path, encoding: str) -> str:
    """Читает текст из файла. Возвращает содержимое в виде строки."""
    try:
        return path.read_text(encoding=encoding, errors="replace")
    except FileNotFoundError:
        raise SystemExit(f"[!] Файл не найден: {path} ")


def write_file(path: Path, records: List[str], encoding: str) -> None:
    """Записывает список анкет в файл."""
    text ="\n\n".join(records) + ("\n" if records else "")
    path.write_text(text, encoding=encoding)
    print(f"[+] Результат без некорректных email сохранён: {path}")


def split_records(text: str) -> List[str]:
    """Разделяет исходный текст на отдельные анкеты."""
    lines = text.splitlines()
    records, cur = [], []
    numbered_start = re.compile(r'^\s*\d+\)\s*$')

    for ln in lines:
        if numbered_start.match(ln):
            if cur:
                records.append("\n".join(cur).strip())
            cur = [ln]
        else:
            if ln.strip() == "" and cur:
                records.append("\n".join(cur).strip())
                cur = []
            else:
                cur.append(ln)
    
    if cur:
        records.append("\n".join(cur).strip())
    
    if not records:
        records = [blk.strip() for blk in re.split(r"\n\s*\n+", text) if blk.strip()]

    return records


def extract_contact(record_text: str) -> Optional[str]:
    """
    Извлечь значение поля 'Номер телефона или email: ...' из анкеты.
    Возвращает строку (телефон или email) либо None.
    """
    for line in record_text.splitlines():
        m = re.match(r'^\s*Номер телефона или email\s*:\s*(.+)$',
                     line, flags=re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def process_records(records: List[str], email_re: Pattern[str]) ->Tuple[List[str], List[Tuple[str, str]]]:
    """Обработка записей и классификация по действительным/недействительным email."""
    kept, invalid = [], []
    for rec in records:
        contact = extract_contact(rec)
        if contact is None:
            kept.append(rec)
            continue
        if "@" in contact:
            if email_re.fullmatch(contact):
                kept.append(rec)
            else:   
                invalid.append((contact, rec))
        else:
            kept.append(rec)
    return kept, invalid


def main()-> None:
    """Основная функция программы."""
    args = arg_parse()
    input_path = Path(args.input)
    text = read_file(Path(args.input), args.encoding)
    records = split_records(text)
    email_pattern = build_email_regex(args.domains)
    kept_records, invalid_records = process_records(records=records, email_re=email_pattern)

    print(f"Количество анкет с НЕКОРРЕКТНЫМИ email: {len(invalid_records)}\n")
    for i, (email, rec) in enumerate(invalid_records, start=1):
        print(f"--- Некорректный email #{i}: {email} ---")
        print(rec)
        print()

    write_file(Path(args.output), kept_records, args.encoding)


if __name__ == "__main__":
    main()
