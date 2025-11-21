import argparse
from file_operations import read_file, write_processed_file
from processors import process_lines


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(description='Обработка данных пользователей')
    parser.add_argument('file', type=str, help='Путь к файлу с данными')
    args = parser.parse_args()
    
    
    lines = read_file(args.file)
    
    if not lines:
        print("Не удалось прочитать исходный файл")
        return
    
    processed_lines = process_lines(lines)
    
    
    write_processed_file(args.file, processed_lines)


if __name__ == '__main__':
    main()