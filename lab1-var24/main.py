import func

def main():
    filename, filename_result = func.get_args()
    content = func.read_file(filename)
    
    if not content:
        print("Error: file is empty or data is corrupted.")
        exit(1)

    func.process_people(content, filename_result)
    print(f"Result was recorded to {filename_result}")


if __name__ == "__main__":
    main()
