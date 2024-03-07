import os
import argparse
import shutil


def main() -> None:
    parser = argparse.ArgumentParser(prog="ConsoleScript",
                                     description="Can create file, "
                                                 "delete file, "
                                                 "write file, "
                                                 "read file, "
                                                 "copy file from other directory, "
                                                 "rename file",
                                     epilog="You can use arguments: -c / --create; -d / --delete; "
                                            "-w / --write; -r / --read; with additional argument -d / --directory "
                                     )
    parser.add_argument("-c", "--create", type=str, help="enter file name to create")
    parser.add_argument("-d", "--delete", type=str, help="enter file name to delete")
    parser.add_argument("-w", "--write", type=str, help="enter file name to write")
    parser.add_argument("-r", "--read", type=str, help="enter file name to read")
    parser.add_argument("-dir", "--directory", type=str, default="C:\\",
                        help="enter directory")
    parser.add_argument("-t", "--transfer", nargs=3, help="enter 3 arguments to transfer file: "
                                                          "first: name file, "
                                                          "second: old directory, "
                                                          "third: new directory")
    parser.add_argument("-rn", "--rename", nargs=2, help="enter 2 arguments to raname file: "
                                                "first argument: name file, "
                                                "second argument: new name file")

    args = parser.parse_args()

    if args.create:
        os.chdir(args.directory)
        try:
            with open(args.create, "x") as file:
                pass
            print("The file was successfully created!")
        except FileExistsError:
            print("The file has already been created previously!")

    if args.delete:
        os.chdir(args.directory)
        if os.path.exists(args.delete):
            os.remove(args.delete)
            print("The file was successfully deletes!")
        else:
            search_trip = find_file(args.delete, args.directory)
            if search_trip == "Not found":
                print("The file is not found!")
            else:
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!")

    if args.write:
        os.chdir(args.directory)
        try:
            with open(args.write, "a") as file:
                text = input("Write your text here: ")
                file.write(text)
            print("The text is already write!")

        except PermissionError:
            search_trip = find_file(args.write, args.directory)
            if search_trip == "Not found":
                print("The file is not found!")
            else:
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!")

    if args.read:
        os.chdir(args.directory)
        try:
            with open(args.read, "r") as file:
                lines = file.readlines()
                for line in lines:
                    print(line.strip())

            print("\nThat is all!")

        except FileNotFoundError:
            search_trip = find_file(args.read, args.directory)
            if search_trip == "Not found":
                print("The file is not found!")
            else:
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!")

    if args.transfer:
        os.chdir(args.transfer[1])
        try:
            with open(args.transfer[0], "r") as file:
                pass
            shutil.copy(args.transfer[0], args.transfer[2])
            print("The file is copied to new directory!")

        except FileNotFoundError:
            search_trip = find_file(args.transfer[0], args.transfer[1])
            if search_trip == "Not found":
                print("The file is not found!")
            else:
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!")

    if args.rename:
        os.chdir(args.directory)
        try:
            with open(args.rename[0], "r") as file:
                pass
            os.rename(args.rename[0], args.rename[1])
            print("The file is rename!")
        except FileNotFoundError:
            search_trip = find_file(args.rename[0], args.directory)
            if search_trip == "Not found":
                print("The file is not found!")
            else:
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!")




# file_name = 'Test_lab1.txt'
# search = 'C:\\Users\\PCLe\\Desktop'

def find_file(file_name: str, search_path: str) -> str:
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)

    return "Not found"


if __name__ == "__main__":
    main()




# print(find_file(args.create, args.directory))
# print(find_file(file_name, search_path=search))

# print(args)
# print(args.create)

