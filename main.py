import argparse
import work_with_file
import anketes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='name of scanning file')
    args = parser.parse_args()
    data = work_with_file.read_file(args.filename)
    data_list = anketes.differentiate_by_anketes(data)
    res = anketes.find_goal_anketes(data_list)
    work_with_file.write_data(res)
    print(len(res))


if __name__ == "__main__":
    main()
