import function

def main():
    filepath = function.get_args()
    text = function.readfile(filepath)
    mens = text.split("\n")
    if mens[len(mens)-1] != "":
        mens.append("")
    file = open("correct_date.txt", "w")
    for i in range(0,len(mens),8):
        if not function.is_correct(mens[i+4][15:]):
            function.print_men(mens,i)
        else:
            function.to_file(file,i,mens)


if __name__ == "__main__":
    main()