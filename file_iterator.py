# file_iterator.py

class FileIterator:
    def __init__(self, file_path: str):
        try:
            self.filepath = file_path
            self.file = open(file_path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f'Файл {file_path} не найден')

    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()

        if not line:
            self.file.close()
            raise StopIteration

        return line