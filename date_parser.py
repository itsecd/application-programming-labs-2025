from typing import List, Tuple


def parse_date_ranges(date_args: str) -> List[Tuple[str, str]]:
    """Разбирает строку диапазонов на начальные и конечные даты"""
    ranges: List[Tuple[str, str]] = []
    range_strings = date_args.split(',')
    
    for range_str in range_strings:
        parts = range_str.split('-')
        if len(parts) != 6:
            raise ValueError(
                f"Неверный формат даты в диапазоне '{range_str}'. "
                f"Используйте: ГГГГ-ММ-ДД-ГГГГ-ММ-ДД"
            )
        
        start_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        end_date = f"{parts[3]}-{parts[4]}-{parts[5]}"
        ranges.append((start_date, end_date))
    
    return ranges