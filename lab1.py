import argparse
from validations import *
from functions import *


def main() -> None:
    """Main logic"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", type=str, help="Set userdata filepath (-f /path/to/file.txt)"
    )
    args = parser.parse_args()

    if args.file is not None:
        print("Usage: python lab1.py -f filename.txt")
    else:
        filename = "data.txt"
        try:
            with open(filename, "r", encoding="utf8") as file:
                lines = file.readlines()
        except:
            print("File Opening ERROR")
            exit(1)

        userdata = []
        age_statistics = {
            "Мужчины 0-17": 0,
            "Мужчины 18-64": 0,
            "Мужчины 65+": 0,
            "Женщины 0-17": 0,
            "Женщины 18-59": 0,
            "Женщины 60+": 0,
        }
        result_str = ""
        for line in lines:
            if line == "\n" or re.fullmatch(r"\d*[)]\n", line):
                continue
            line = line[line.find(":") + 2 : -1]
            if "г." in line:
                line = line[3:]
            userdata.append(line)
            if len(userdata) < 6:
                continue
            if is_valid_userdata(userdata):
                age = get_age(userdata[3])
                age_statistics[get_group_type(userdata[2][0].lower(), age)] += 1
            userdata.clear()
        try:
            for group, count in age_statistics.items():
                result_str += f"{group}: {count}\n"
            file = open("result.txt", "w", encoding="utf-8")
            file.write(result_str)
            file.close()
            print("Saved to 'result.txt'")
        except:
            print("Saving file result ERROR")
            exit(2)


if __name__ == "__main__":
    main()
