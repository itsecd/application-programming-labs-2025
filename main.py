import anketes
import argparse
import work_with_file


def argument_parsing() -> list[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='path to input file')
    parser.add_argument('output_file', type=str, help='path to output file')
    args = parser.parse_args()
    return [args.input_file, args.output_file]


def data_process(data: str) -> list[str]:
    data_list = anketes.differentiate_by_anketes(data)
    return anketes.find_goal_anketes(data_list)


def main():
    input_file, output_file = argument_parsing()
    data = work_with_file.read_file(input_file)
    result = data_process(data)
    work_with_file.write_data(output_file, result)
    print('Найдено подходящих анкет:', len(result))


if __name__ == "__main__":
    main()
