import re
from collections import Counter

with open('data.txt', 'r', encoding='utf-8') as file:
    content = file.read()

codes = re.findall(r'[+78][\s\(]*(\d{3})', content)

if codes:
    code_counter = Counter(codes)
    code, count = code_counter.most_common(1)[0]
    print(f"Самый частый код оператора: {code}")
    print(f"Повторений: {count}")

else:
    print("Коды операторов не найдены")