import os
import argparse
import shutil
import winreg


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

    parser.add_argument("-crk", "--create_key", type=str, help="enter your key to create")
    parser.add_argument("-dk", "--delete_key", type=str, help="enter your key to delete")
    parser.add_argument("-wnk", "--write_keyvalue", nargs=4, help="enter 4 arguments to write value in key: "
                                                                "first: name key; "
                                                                "second: value type; "
                                                                "third: value name; "
                                                                "fourth: new value data")

    parser.add_argument("-bch", "--bush_key", type=str, default="CU", choices=['CU', 'CR', 'LM', 'U', 'CC'],
                        help="enter 1 of argument to needed bush (hotkey):"
                             "CU = HKEY_CURRENT_USER; "
                             "CR = HKEY_CLASSES_ROOT; "
                             "LM = HKEY_LOCAL_MACHINE; "
                             "U = HKEY_USERS; "
                             "CC = HKEY_CURRENT_CONFIG " )

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
                answer = input()
                if answer == "Y" or answer == 'y':
                    os.chdir(out_directory(search_trip))
                    os.remove(args.delete)
                    print("The file was successfully deletes!")

                elif answer == "N" or answer == "n":
                    print(f'The file is not found in {args.directory}')

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
                answer = input()
                if answer == "Y" or answer == 'y':
                    os.chdir(out_directory(search_trip))
                    with open(args.write, "a") as file:
                        text = input("Write your text here: ")
                        file.write(text)
                    print("The text is already write!")

                elif answer == "N" or answer == "n":
                    print(f'The file is not found in {args.directory}')

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
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!(Y/N)")
                answer = input()
                if answer == "Y" or answer == 'y':
                    os.chdir(out_directory(search_trip))
                    with open(args.read, "r") as file:
                        lines = file.readlines()
                        for line in lines:
                            print(line.strip())
                    print("\nThat is all!")
                elif answer == "N" or answer == "n":
                    print(f'The file is not found in {args.directory}')

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
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!(Y/N)")
                answer = input()
                if answer == "Y" or answer == 'y':
                    os.chdir(out_directory(search_trip))
                    shutil.copy(args.transfer[0], args.transfer[2])
                    print("The file is copied to new directory!")
                elif answer == "N" or answer == "n":
                    print(f'The file is not found in {args.transfer[1]}')

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
                print(f"File is found in a subdirectory {search_trip}, try with new arguments!(Y/N)")
                answer = input()
                if answer == "Y" or answer == 'y':
                    os.chdir(out_directory(search_trip))
                    os.rename(args.rename[0], args.rename[1])
                    print("The file is rename!")
                elif answer == "N" or answer == "n":
                    print(f'The file is not found in {args.directory}')

    if args.create_key or args.delete_key or args.write_keyvalue:
        try:
            if args.bush_key == "CU":
                hkey = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            elif args.bush_key == "CR":
                input("press 'enter' to continue, HKEY_CLASSES_ROOT:")
                hkey = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
            elif args.bush_key == "LM":
                input("press 'enter' to continue, HKEY_LOCAL_MACHINE:")
                hkey = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            elif args.bush_key == "U":
                input("press 'enter' to continue, HKEY_USERS:")
                hkey = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
            elif args.bush_key == "CC":
                input("press 'enter' to continue, HKEY_CURRENT_CONFIG:")
                hkey = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_CONFIG)
            else:
                print("ERROR not correct -bch / --bush_key argument!")

            if args.create_key:
                winreg.CreateKey(hkey, args.create_key)
                print("Key is successful create!")

            if args.delete_key:
                winreg.DeleteKey(hkey, args.delete_key)
                print("Key is successful delete!")

            if args.write_keyvalue:
                type_data = ["REG_BINARY", "REG_DWORD", "REG_EXPAND_SZ", "REG_MULTI_SZ", "REG_SZ", "REG_RESOURCE_LIST",
                             "REG_RESOURCE_REQUIREMENTS_LIST", "REG_FULL_RESOURCE_DESCRIPTOR", "REG_NONE", "REG_LINK",
                             "REG_QWORD"]
                if args.write_keyvalue[1] not in type_data:
                    print("Incorrect second argument!")

                else:
                    value_type = ret_value_type(args.write_keyvalue[1])
                    with winreg.OpenKey(hkey, args.write_keyvalue[0], 0, winreg.KEY_SET_VALUE) as key:
                        winreg.SetValueEx(key, args.write_keyvalue[2], 0, value_type, args.write_keyvalue[3])
                    print("Value key successful change!")

        except PermissionError:
            print(f"Not permission to create or delete or change value key in {args.bush_key} ")

        finally:
            winreg.CloseKey(hkey)


def ret_value_type(value_name):
    if value_name == "REG_BINARY":
        return winreg.REG_BINARY
    elif value_name == "REG_DWORD":
        return winreg.REG_DWORD
    elif value_name == "REG_EXPAND_SZ":
        return winreg.REG_EXPAND_SZ
    elif value_name == "REG_MULTI_SZ":
        return winreg.REG_MULTI_SZ
    elif value_name == "REG_SZ":
        return winreg.REG_SZ
    elif value_name == "REG_RESOURCE_LIST":
        return winreg.REG_RESOURCE_LIST
    elif value_name == "REG_RESOURCE_REQUIREMENTS_LIST":
        return winreg.REG_RESOURCE_REQUIREMENTS_LIST
    elif value_name == "REG_FULL_RESOURCE_DESCRIPTOR":
        return winreg.REG_FULL_RESOURCE_DESCRIPTOR
    elif value_name == "REG_NONE":
        return winreg.REG_NONE
    elif value_name == "REG_LINK":
        return winreg.REG_LINK
    elif value_name == "REG_QWORD":
        return winreg.REG_QWORD


def out_directory(text: str) -> str:
    text = text.replace('\\', '/').split("/")
    text.pop()
    text = "/".join(text)
    return text


def find_file(file_name: str, search_path: str) -> str:
    for root, dirs, files in os.walk(search_path):
        if file_name in files:
            return os.path.join(root, file_name)

    return "Not found"


if __name__ == "__main__":
    main()



