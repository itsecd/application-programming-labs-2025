def read_file(filename: str) -> str:
    """
    Операция чтения данных из файла в строку
    """
    try:
        with open(filename, encoding="utf-8") as file:
            text = file.read()
        return text
    except ValueError as exc:
        print(f"Data Error: {exc}")


def write_data(data: list[str]) -> None:
    with open("result.txt", "+w", encoding="utf-8") as f:
        for i in range(len(data)):
            f.write(f"{i+1})\n")
            f.write(data[i])