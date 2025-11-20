import re


def main() -> None:
    with open("data.txt", "r", encoding="utf-8") as f:
        content = f.read()

   
    pattern = r"(\d+)\)\s*\n(.*?)(?=\n\d+\)|\Z)"
    matches = re.findall(pattern, content, flags=re.DOTALL)

    moscow_people = []

    for num_str, body in matches:
        num = int(num_str)
        lines = [line.strip() for line in body.split("\n") if line.strip()]
        data = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

        city = data.get("Город", "")
        
        norm_city = city.strip()
        if norm_city.startswith("г."):
            norm_city = norm_city[2:].strip()

        if norm_city == "Москва":
            moscow_people.append((num, body))

    count = len(moscow_people)
    print(f"Количество жителей Москвы: {count}")

    with open("moscow_residents.txt", "w", encoding="utf-8") as f:
        for num, body in moscow_people:
            f.write(f"{num})\n{body}\n\n")

    print("😎👍 Анкеты сохранены в 'moscow_residents.txt'")


if __name__ == "__main__":
    main()