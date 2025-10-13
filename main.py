import re, argparse, os, parser as my_parser



def write_to_file(output_filename, data):

    """
    function for adding a record to a file
    """
    try:
        with open(output_filename, "a") as file:
            file.write(data + "\n") 


    except FileNotFoundError:
        print("file not exists")



def main(data_filename, output_filename):

    """
    reads data from file and send to parser.py
    """

    try:
        with open(data_filename, "r") as file:
            count = 0
            while True:
                data = ""
                for num_line in range(7):
                    line = file.readline()
                    if not line{
                        break
                    }
                    data += line

                if not data.strip(): 
                    break

                # parse data to user
                user = my_parser.Parse_data(data)
                if (my_parser.Parse_user(user)):
                    pattern = r"\d+[)]"
                    write_to_file(output_filename, re.sub(pattern, str(count + 1) + ")", data, count=0))
                    count += 1
                file.readline()
        return True, count
        



    except FileNotFoundError:
        print("file not exists")
        return False, 0





def cli_get_args():

    """
    receives arguments from the command line
    """
    # create and conf parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-fn", "--filename", type=str, help="your filename")
    parser.add_argument("-o", "--output", type=str, help="output filename")
    args = parser.parse_args()

    data_filename = "data.txt"
    output_filename = "output.txt"
    if (args.filename):
        data_filename = os.path.basename(args.filename)
    if (args.output):
        output_filename =  os.path.basename(args.output)

    return data_filename, output_filename
    
    



if __name__ == "__main__":

    """
    main func
    """
    # get args from cli    
    data_filename, output_filename = cli_get_args()

    try:
        with open(output_filename, "w") as file:
            file.write("")
    
    except FileNotFoundError:
        print("file not exists")

    success, count = main(data_filename, output_filename)
    
    if (success):
        print(f"count user with email: {count}")
        print("the program has finished")
        exit(0)
    print("somthing error :(")
    exit(1)