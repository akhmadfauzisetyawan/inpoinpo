import time, random, shutil, os
import json
import subprocess

def loading():
    mengetik('\033[32m')
    mengetik("╔══════════════════════════════════════════════════════════════════════╗")
    mengetik("║ Loading ..............                                               ║")
    mengetik("╚══════════════════════════════════════════════════════════════════════╝")
    time.sleep(1)
    os.system("cls")

def mengetik(s):
    terminal_width, _ = shutil.get_terminal_size()
    padding = (terminal_width - len(s)) // 2
    print(" " * padding + s)
    time.sleep(random.random() * 0.001)

def login():
    mengetik("╔══════════════════════════════════════════════════════════════════════╗")
    mengetik("║                                  Welcome                             ║")
    mengetik("╠══════════════════════════════════════════════════════════════════════╣")
    mengetik("║                           HR-AL BUKHARI NO 7152                      ║")
    mengetik("╚══════════════════════════════════════════════════════════════════════╝")
    username = input("Username: ")
    password = input("Password: ")

    loading()

    try:
        with open("cabang/cabang.json", mode="r") as file:
            cabang_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cabang_data = []  

    if username == "bos" and password == "bos":
        mengetik("Anda login sebagai bos")
        subprocess.run(["python",r"C:\Users\uer\Documents\AaaKu kuliah\SEMESTER 2\ALGO\toko_utama\inicoba.py", username])
        return "bos"  
    elif any(entry["username"] == username and entry["password"] == password for entry in cabang_data):
        mengetik(f"Selamat datang, cabang {username}!")
        subprocess.run(["python",r"C:\Users\uer\Documents\AaaKu kuliah\SEMESTER 2\ALGO\toko_utama\cabang.py", username])
        return "cabang"  
    else:
        mengetik("Login gagal. Cek username dan password Anda.")
        return None  


login()
