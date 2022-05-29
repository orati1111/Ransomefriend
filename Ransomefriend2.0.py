
#Moduls to import
import argparse
import sys
from cryptography.fernet import Fernet
import os
import glob
import cryptography

#Declaration
opening = """

______                                      __      _                _ 
| ___ \                                    / _|    (_)              | |
| |_/ /__ _ _ __  ___  ___  _ __ ___   ___| |_ _ __ _  ___ _ __   __| |
|    // _` | '_ \/ __|/ _ \| '_ ` _ \ / _ |  _| '__| |/ _ | '_ \ / _` |
| |\ | (_| | | | \__ | (_) | | | | | |  __| | | |  | |  __| | | | (_| |
\_| \_\__,_|_| |_|___/\___/|_| |_| |_|\___|_| |_|  |_|\___|_| |_|\__,_|
                                                                       
                                                                       
-h -> use for help
"""

#Defs

def encrypt(path):
    # FILE
    if(os.path.isfile(path)):
        print(f"Path ----> {path}")
        with open("key.key","rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)

        with open(path,"rb") as file:
            original_content = file.read()

        encrypted_content = fernet.encrypt(original_content)

        with open(path,"wb") as file:
            file.write(encrypted_content)

        print("Done!")

    # DIR
    elif(os.path.isdir(path)):
        print(f"Path ----> {path}")

        with open("key.key","rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)

        glob_path = glob.glob(f'{path}/**', recursive=True)
        print("Encrypting:")
        for i in range(len(glob_path)):
            file_path = glob_path[i]
            if(os.path.isdir(file_path)):
                continue
            else:
                try:
                    print(file_path)
                    with open(file_path,"rb") as file:
                        original_content = file.read()

                    encrypted_content = fernet.encrypt(original_content)
                    
                    with open(file_path,"wb") as file:
                        file.write(encrypted_content)
                except PermissionError:
                    continue
            
        print("Done!")
    
    else:
        print("Couldnt find the directory/file.")


def decrypt(path):
    # FILE
        if(os.path.isfile(path)):
            print(f"Path ----> {path}")
            with open("key.key","rb") as key_file:
                key = key_file.read()
            fernet = Fernet(key)

            with open(path,"rb") as file:
                encrypted_content = file.read()

            original = fernet.decrypt(encrypted_content)

            with open(path,"wb") as file:
                file.write(original)

            print("Done!")

    # DIR
        if(os.path.isdir(path)):
            print(f"Path ----> {path}")
            with open("key.key","rb") as key_file:
                key = key_file.read()
            fernet = Fernet(key)

            glob_path = glob.glob(f'{path}/**', recursive=True)
            print("Decrypting:")
            for i in range(len(glob_path)):
                file_path = glob_path[i]
                if(os.path.isdir(file_path)):
                    continue
                else:
                    try:
                        print(file_path)
                        with open(file_path,"rb") as file:
                            encrypted_content = file.read()

                        decrypted_content = fernet.decrypt(encrypted_content)

                        with open(file_path,"wb") as file:
                            file.write(decrypted_content)
                    except (cryptography.fernet.InvalidToken, TypeError):
                        continue
            
            print("Done!")


os.system('color 0a')
os.system("cls")
print(opening)
parser = argparse.ArgumentParser(description="Security tool to encrypt and decrypt files.")
parser.add_argument("-e" ,"--encrypt" , action='store_true', help="Encrypts the files.")
parser.add_argument("-d" ,"--decrypt" , action='store_true',help="Decrypts the files.")
parser.add_argument("-p" ,"--path" , type=str, help="Select a path of files.")
parser.add_argument("-gen" ,"--generate" ,nargs="?",const=os.getcwd(), type=str, help="Generates a key and stores it.[Optional] -> add a path to store a key in a selected directory otherwise it will be stored in the current directory.")
args = parser.parse_args()

if args.generate != None:
    if(not os.path.exists("key.key")):
        key = Fernet.generate_key()
        with open("key.key","wb") as key_file:
            key_file.write(key)
            print("Generated a key at" , os.path.abspath("key.key"))

    elif (os.path.exists("key.key")):
        print("A KEY WAS ALREADY GENERATED DO YOU WANT TO OVERWRITE IT?(Y/N)")
        answer = input()
        if(answer == "y" or answer == "Y"):
            key = Fernet.generate_key()
            with open("key.key","wb") as key_file:
                key_file.write(key)
            print("Overwritten.")
        elif(answer == "n" or answer == "N"):
            exit()
        else:
            print("invalid input")
        

if args.encrypt:
    if(os.path.exists("key.key")):
        if args.path is None:
            raise KeyError("You didnt input any path.")
        else:
            encrypt(args.path)
    else:
        print("You didnt generate a key. you need to use -gen first.")
    
if args.decrypt:
        if(os.path.exists("key.key")):
            if args.path is None:
                raise KeyError("You didnt input any path.")
            else:
                decrypt(args.path)
        else:
            print("Couldnt find a key.")


