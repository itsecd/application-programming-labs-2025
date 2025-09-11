import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str, help="Имя входного файла с анкетами")
args = parser.parse_args()

with open(args.filename, "r", encoding="utf-8") as file:
    lines = file.readlines()


def capitalize_name(name):
    return name.capitalize()


fixed_lines = []

for line in lines:
    if "Фамилия:" in line or "Имя:" in line:
        parts = line.rsplit(": ", 1)
        if len(parts) == 2:
            key = parts[0]
            value = parts[1].strip()
            fixed_value = capitalize_name(value)
            fixed_line = key + ": " + fixed_value + "\n"
        else:
            stripped = line.strip()
            fixed_line = capitalize_name(stripped) + "\n"
        fixed_lines.append(fixed_line)
    else:
        fixed_lines.append(line)

with open("fixed_data.txt", "w", encoding="utf-8") as outfile:
    outfile.writelines(fixed_lines)

print("Исправленные данные сохранены в fixed_data.txt")
