with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
valid_lines = []
for line in lines:
    if '@' in line and '.' in line:
        valid_lines.append(line)
print(len(valid_lines))
with open('result.txt', 'w', encoding='utf-8') as f:
    f.writelines(valid_lines
