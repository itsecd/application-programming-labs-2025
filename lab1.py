# ВЫПОЛНИЛ ДОЛЖИКОВ ДМИТРИЙ 6212-100503D
import functions


def main() -> None:
    """Main logic"""
    filename = functions.get_args()
    if filename is None:
        print("Usage: python lab1.py -f filename.txt")
        exit(3)
    lines = functions.read_file(filename)

    if lines is None:
        print("ERROR: No such file or directory")
        exit(1)

    age_statistics = functions.get_statistics(lines)

    if functions.save_result(age_statistics):
        print("Saved to 'result.txt'")
    else:
        print("ERROR: Unable to save the file Permisson Denied")
        exit(2)


if __name__ == "__main__":
    main()
