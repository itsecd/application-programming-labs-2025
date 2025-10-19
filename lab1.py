import re
pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
valid_lines = []
for line in lines:
    if re.search(pattern, line):
        valid_lines.append(line)
print(len(valid_lines))
with open('result.txt', 'w', encoding='utf-8') as f:
    f.writelines(valid_lines)
