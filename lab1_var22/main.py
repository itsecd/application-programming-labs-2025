#!/usr/bin/env python3
"""
Лабораторная 1, вариант 22.
Из файла с анкетами строит список "Фамилия: номер телефона" для корректных телефонов.
"""

from __future__ import annotations
import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class Person:
    last_name: str
    first_name: str
    gender: str
    birth_date: str
    contact: str
    city: str


def read_people(path: Path) -> List[Person]:
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    lines = [ln for ln in lines if ln != ""]
    people: List[Person] = []

    if len(lines) % 6 != 0:
        truncated = len(lines) - (len(lines) // 6) * 6
        print(f"[warn] Некратное 6 количество строк: игнорирую последние {truncated} строки")

    for i in range(0, len(lines) - len(lines) % 6, 6):
        chunk = lines[i:i + 6]
        people.append(Person(*chunk))

    return people


_PHONE_DIGITS_RE = re.compile(r"\D+")


def normalize_phone(raw: str) -> Optional[str]:
    digits = _PHONE_DIGITS_RE.sub("", raw)
    if len(digits) != 11:
        return None
    if digits[0] not in ("7", "8"):
        return None

    area = digits[1:4]
    bbb = digits[4:7]
    cc = digits[7:9]
    dd = digits[9:11]
    return f"+7 ({area}) {bbb}-{cc}-{dd}"


def select_lastname_and_phone(people: Iterable[Person]) -> List[str]:
    result: List[str] = []
    for p in people:
        phone = normalize_phone(p.contact)
        if phone:
            result.append(f"{p.last_name}: {phone}")
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Лаб.1 (вар.22): 'Фамилия: номер телефона' для корректных телефонов"
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=Path("data.txt"),
        help="Путь к входному файлу (по умолчанию data.txt)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("phones.txt"),
        help="Куда сохранить результат (по умолчанию phones.txt)"
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    people = read_people(args.input)
    pairs = select_lastname_and_phone(people)

    print(f"Найдено корректных телефонов: {len(pairs)}")
    for line in pairs[:10]:
        print(line)

    out_text = "\n".join(pairs) + ("\n" if pairs else "")
    args.output.write_text(out_text, encoding="utf-8")
    print(f"Сохранено в: {args.output.resolve()}")


if __name__ == "__main__":
    main()