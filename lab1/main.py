import re

import function


def main():
    filepath = function.get_args()
    text = function.read_file(filepath)
    mens = text.split("\n\n")
    file = open("correct_date.txt", "w")
    for men in mens:
        if not function.is_correct(re.search(r'\d+[./\t-]\d+[./\t-]\d+', men).group()):
            print(men)
        else:
            function.to_file(file, men)
    file.close()


if __name__ == "__main__":
    main()