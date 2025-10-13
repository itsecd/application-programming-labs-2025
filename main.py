import re
import sys
import os
from typing import Pattern, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


class Validators:
    #Класс с регулярными выражениями для валидации данных
    
    MOSCOW_PATTERN: Pattern = re.compile(r'^(г\.\s*)?Москва$', re.IGNORECASE)
    
    PERSON_PATTERN: Pattern = re.compile(
        r'Фамилия:\s*(.+)\s*'
        r'Имя:\s*(.+)\s*'
        r'Пол:\s*(.+)\s*'
        r'Дата рождения:\s*(.+)\s*'
        r'Номер телефона или email:\s*(.+)\s*'
        r'Город:\s*(.+)',
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    
    NAME_PATTERN: Pattern = re.compile(r'^[А-ЯЁA-Z][а-яёa-z]*$')

    GENDER_PATTERN: Pattern = re.compile(r'^(М|м|Мужской|мужской|Ж|ж|Женский|женский)$')
    
    DATE_PATTERN: Pattern = re.compile(
        r'^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$'
    )
    
    PHONE_PATTERN: Pattern = re.compile(
        r'^(8|\+7)[\s(-]*(\d{3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})$'
    )
    
    EMAIL_PATTERN: Pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$'
    )


@dataclass
class Person:
    #Класс для представления анкеты человека
    
    last_name: str
    first_name: str
    gender: str
    birth_date: str
    contact: str
    city: str
    is_valid: bool = True
    validation_errors: List[str] = None
    
    def __post_init__(self):
        #Проверка валидности данных после создания объекта
        if self.validation_errors is None:
            self.validation_errors = []
        self._validate_person()
    
    def _validate_person(self) -> None:
        #Проверяет валидность всех данных анкеты
        self.is_valid = True
        self.validation_errors = []
        
        if not Validators.NAME_PATTERN.match(self.last_name):
            self.is_valid = False
            self.validation_errors.append(f"Неверный формат фамилии: {self.last_name}")
        
        if not Validators.NAME_PATTERN.match(self.first_name):
            self.is_valid = False
            self.validation_errors.append(f"Неверный формат имени: {self.first_name}")
        
        if not Validators.GENDER_PATTERN.match(self.gender):
            self.is_valid = False
            self.validation_errors.append(f"Неверный формат пола: {self.gender}")
        
        if not self._validate_date(self.birth_date):
            self.is_valid = False
            self.validation_errors.append(f"Неверный формат даты рождения: {self.birth_date}")
        
        if not (Validators.PHONE_PATTERN.match(self.contact.replace(' ', '')) or 
                Validators.EMAIL_PATTERN.match(self.contact)):
            self.is_valid = False
            self.validation_errors.append(f"Неверный формат контакта: {self.contact}")
    
    def _validate_date(self, date_str: str) -> bool:
         #Проверяет валидность даты рождения
        match = Validators.DATE_PATTERN.match(date_str)
        if not match:
            return False
        
        day, month, year = map(int, match.groups())
        
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            return False
        
        if month < 1 or month > 12:
            return False
        
        days_in_month = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 
                         31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        return 1 <= day <= days_in_month[month - 1]
    
    @classmethod
    def from_string(cls, data: str) -> Optional['Person']:
        """
        Создает объект Person из строки с данными анкеты
        Args:
            data: Строка с данными анкеты
        Returns:  Объект Person или None если данные некорректны
        """
        # Убираем нумерацию вроде "1)", "2)" и т.д.
        cleaned_data = re.sub(r'^\d+\)\s*', '', data.strip(), flags=re.MULTILINE)
        
        match = Validators.PERSON_PATTERN.search(cleaned_data)
        if match:
            return cls(
                last_name=match.group(1).strip(),
                first_name=match.group(2).strip(),
                gender=match.group(3).strip(),
                birth_date=match.group(4).strip(),
                contact=match.group(5).strip(),
                city=match.group(6).strip()
            )
        return None
    
    def is_from_moscow(self) -> bool:
        """
        Проверяет, проживает ли человек в Москве
        Returns:  True если человек из Москвы, иначе False
        """
        return bool(Validators.MOSCOW_PATTERN.match(self.city))
    
    def to_string(self) -> str:
        """
        Преобразует объект Person в строку для сохранения
        Returns:  Строка с данными анкеты
        """
        return (f"{self.last_name}\n{self.first_name}\n{self.gender}\n"
                f"{self.birth_date}\n{self.contact}\n{self.city}\n")
    
    def __str__(self) -> str:
        #Строковое представление объекта
        status = "✓" if self.is_valid else "✗"
        return f"{status} {self.last_name} {self.first_name}, {self.city}"


class FileParser:
    #Класс для работы с файлами анкет
    
    @staticmethod
    def read_people_from_file(filename: str) -> Tuple[List[Person], List[Person]]:
        """
        Читает анкеты людей из файла
        Args:
            filename: Имя файла для чтения
        Returns: Кортеж (валидные_анкеты, невалидные_анкеты)
        Raises:
            FileNotFoundError: Если файл не существует
            IOError: При ошибках чтения файла
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден")
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Разделяем файл на отдельные анкеты
            profiles = content.strip().split('\n\n')
            
            valid_people = []
            invalid_people = []
            
            for profile in profiles:
                if profile.strip():  # Пропускаем пустые анкеты
                    person = Person.from_string(profile)
                    if person:
                        if person.is_valid:
                            valid_people.append(person)
                        else:
                            invalid_people.append(person)
                    else:
                        print(f"Предупреждение: не удалось распарсить анкету")
                    
            return valid_people, invalid_people
            
        except Exception as e:
            raise IOError(f"Ошибка при чтении файла {filename}: {str(e)}")
    
    @staticmethod
    def save_people_to_file(people: List[Person], filename: str) -> None:
        """
        Сохраняет список людей в файл
        Args:
            people: Список объектов Person для сохранения
            filename: Имя файла для сохранения
        Raises:
            IOError: При ошибках записи в файл
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for i, person in enumerate(people, 1):
                    file.write(f"{i})\n")
                    file.write(f"Фамилия: {person.last_name}\n")
                    file.write(f"Имя: {person.first_name}\n")
                    file.write(f"Пол: {person.gender}\n")
                    file.write(f"Дата рождения: {person.birth_date}\n")
                    file.write(f"Номер телефона или email: {person.contact}\n")
                    file.write(f"Город: {person.city}\n\n")
                    
        except Exception as e:
            raise IOError(f"Ошибка при записи в файл {filename}: {str(e)}")


def main() -> None:
    try:
        # Проверяем аргументы командной строки
        if len(sys.argv) < 1:
            print("Ошибка: не указано имя файла")
            print("Использование: python main.py <имя_файла>")
            return

        input_filename = "data.txt"
        output_filename = "moscow_people.txt"

        print(f"Чтение файла: {input_filename}")

        # Читаем анкеты из файла
        valid_people, invalid_people = FileParser.read_people_from_file(input_filename)
        
        print(f"Прочитано анкет: {len(valid_people) + len(invalid_people)}")
        print(f"Валидных анкет: {len(valid_people)}")
        print(f"Невалидных анкет: {len(invalid_people)}")
        
        if invalid_people:
            print("\nНевалидные анкеты:")
            for person in invalid_people:
                print(f"  - {person}")
                for error in person.validation_errors:
                    print(f"    Ошибка: {error}")
        
        # Находим людей из Москвы среди валидных анкет
        moscow_people: List[Person] = [
            person for person in valid_people 
            if person.is_from_moscow()
        ]
        
        # Выводим результаты
        print(f"\nНайдено людей из Москвы: {len(moscow_people)}")
        
        if moscow_people:
            print("\nСписок людей из Москвы:")
            for person in moscow_people:
                print(f"  - {person}")
            
            # Сохраняем в файл
            FileParser.save_people_to_file(moscow_people, output_filename)
            print(f"\nАнкеты сохранены в файл: {output_filename}")
        else:
            print("Людей из Москвы не найдено")
            
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == '__main__':
    main()