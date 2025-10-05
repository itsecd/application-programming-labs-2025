import func

def main():
    filename = func.get_args()
    content = func.read_file(filename)
    
    if (len(content) == 0) or (content is None):
        print("Error: file is empty or data is corrupted.")
        exit(1)

    filename_result = "result.txt"
    func.process_people(content, filename_result)
    print(f"Result was recorded to {filename_result}")


if __name__ == "__main__":
    main()
