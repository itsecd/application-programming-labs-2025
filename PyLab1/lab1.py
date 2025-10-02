
import func


def main() -> None:
    filename = func.get_args()
    text = func.intput_file(filename)
    people = text.split("\n\n")
    new_file = open("new_data.txt", "w")
    for human in people:
        if not func.is_correct_name(human):
            human = func.data_change_name(human)
        if not func.is_correct_surname(human):
            human = func.data_change_surname(human)
        func.output_file(new_file, human)
    new_file.close()


if __name__ == "__main__":
    main()
