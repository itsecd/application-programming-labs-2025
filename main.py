import anketes
import argparse
import work_with_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='path to input file')
    parser.add_argument('output_file', type=str, help='path to output file')
    args = parser.parse_args()
    data = work_with_file.read_file(args.input_file)
    data_list = anketes.differentiate_by_anketes(data)
    res = anketes.find_goal_anketes(data_list)
    work_with_file.write_data(args.output_file, res)
    print(len(res))


if __name__ == "__main__":
    main()
