
import func


def main() -> None:
    filenames = func.get_args()
    text = func.intput_file(filenames[0])
    people = text.split("\n\n")
    new_file = open(filenames[1], "w")
    for human in people:
        if func.is_correct_name_or_surname(human)>0:
            human = func.data_change_surname_and_name(human)
        func.output_file(new_file, human)
    new_file.close()


if __name__ == "__main__":
    main()
