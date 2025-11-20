import argparse


import data_frame_operations

def parsing() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="Enter file path")
    args = parser.parse_args()
    return args.file_path


def main():
    file_path = parsing()
    data_frame = data_frame_operations.create_DataFrame(file_path)
    print(data_frame)
    data_frame_operations.area_distrib(data_frame)


if __name__ == "__main__":
    main()