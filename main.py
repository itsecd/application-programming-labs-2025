#Найдите все женские имена, начинающиеся с буквы А.
#Выведите их количество на экран и сохраните анкеты в новый файл.
import re 
import argparse

def is_name_correct(text: str)->bool:
    """Имя должно начинаться на заглавную А и состоять только из букв."""
    return re.fullmatch(r'А[а-яё]*', name) is not None

def is_female(text: str)->bool:
    """Пол женский"""
    return re.fullmatch(r'(Ж|ж|Женский|женский)', gender) is not None
