import pandas as pd
from tabulate import tabulate
import time, random, shutil, os, csv, datetime, json
import matplotlib.pyplot as plt

def loading():
    mengetik('\033[32m')
    mengetik("╔══════════════════════════════════════════════════════════════════════╗")
    mengetik("║ Loading ..............                                               ║")
    mengetik("╚══════════════════════════════════════════════════════════════════════╝")
    time.sleep(1)
    os.system("cls")

def gabung_transaksipenjualan_cabang():
    all_trans = pd.DataFrame()
    cabang_files = [file for file in os.listdir() if file.endswith('_transaksi_penjualan.csv')]
    for file in cabang_files:
        cabang_name = file.split('_')[0] 
        df = pd.read_csv(file)
        df['Nama Cabang'] = cabang_name
        all_trans = pd.concat([all_trans, df], ignore_index=True)
    all_trans['Total Penjualan'] = all_trans['Jumlah Terjual'] * all_trans['Harga Barang']
    return all_trans

def visualisasi_total_penjualan(sorted_trans):
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_trans['Nama Cabang'], sorted_trans['Total Penjualan'], color='skyblue')
    plt.title("Total Penjualan Terbanyak per Cabang")
    plt.xlabel("Nama Cabang")
    plt.ylabel("Total Penjualan")
    plt.xticks(rotation=45, ha='right')
    for i in range(len(sorted_trans)):
        plt.text(i, sorted_trans['Total Penjualan'].iloc[i], str(sorted_trans['Total Penjualan'].iloc[i]), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def total_penjualan_cabang():
    all_trans = gabung_transaksipenjualan_cabang()
    if not all_trans.empty:
        grouped_trans = all_trans.groupby('Nama Cabang')
        total_penjualan = grouped_trans['Total Penjualan'].sum().reset_index()
        total_barang_terjual = grouped_trans['Jumlah Terjual'].sum().reset_index()

        total_penjualan = total_penjualan.merge(total_barang_terjual, on='Nama Cabang', suffixes=('_penjualan', '_barang'))
        
        trans_list = total_penjualan.values.tolist()
        n = len(trans_list)
        for i in range(n):
            for j in range(0, n-i-1):
                if trans_list[j][1] < trans_list[j+1][1]:
                    trans_list[j], trans_list[j+1] = trans_list[j+1], trans_list[j]

        sorted_trans = pd.DataFrame(trans_list, columns=["Nama Cabang", "Total Penjualan", "Jumlah Terjual"])
        print("Cabang dengan Total Penjualan Terbanyak:")
        print(tabulate(sorted_trans, headers='keys', tablefmt='grid'))  
        visualisasi_total_penjualan(sorted_trans)
    else:
        print("Belum ada data penjualan dari cabang.")

def mengetik(s):
    terminal_width, _ = shutil.get_terminal_size()
    padding = (terminal_width - len(s)) // 2
    print(" " * padding + s)
    time.sleep(random.random() * 0.001)
    
def Tambah_Barang():
    Info_cabang() 
    
    while True:
        nama_cabang = input("Masukkan nama cabang: ")
        file_path = f"{nama_cabang}_barang.csv"

        if not os.path.exists(file_path):
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Nama Barang", "Harga Barang", "Jumlah Barang", "Tanggal Kirim", "Jam Kirim"])

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=["Nama Barang", "Harga Barang", "Jumlah Barang", "Tanggal Kirim", "Jam Kirim"])

        while True:
            nama_barang = input("Masukan nama barang: ")
            if len(nama_barang) < 4:
                print("nama barang tidak valid")
                return
            elif len(nama_barang) >20:
                print("nama barang tidak valid")
                break

            existing_item = df[df['Nama Barang'] == nama_barang]

            if not existing_item.empty:
                harga = existing_item['Harga Barang'].iloc[0]
                print(f"Barang '{nama_barang}' ditemukan dengan harga {harga}.")
            else:
                while True:
                    try:
                        harga = int(input("Masukan harga barang : "))
                        if harga >= 1000:
                            break
                        else:
                            print("Harga harus di atas 1.000.")
                    except ValueError:
                        print("Masukan angka yang valid.")

            while True:
                try:
                    jumlah_barang = int(input("Masukan jumlah barang : "))
                    if jumlah_barang > 0:
                        break
                    else:
                        print("Jumlah barang tidak boleh 0.")
                except ValueError:
                    print("Masukan angka yang valid.")

            waktu_sekarang = datetime.datetime.now()
            tanggal = waktu_sekarang.strftime("%Y-%m-%d")
            jam_Kirim = waktu_sekarang.strftime("%H:%M:%S")

            mask = (df['Nama Barang'] == nama_barang) & (df['Harga Barang'] == harga)

            if not df[mask].empty:
                df.loc[mask, 'Jumlah Barang'] += jumlah_barang
            else:
                new_row = pd.DataFrame({
                    "Nama Barang": [nama_barang],
                    "Harga Barang": [harga],
                    "Jumlah Barang": [jumlah_barang],
                    "Tanggal Kirim": [tanggal],
                    "Jam Kirim": [jam_Kirim],
                })
                df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv(file_path, mode="w", index=False) 
            print("Data barang berhasil ditambahkan.")

            while True:
                pilihan = input("Apakah ingin kembali ke menu admin? (ya/tidak): ").lower()
                if pilihan == "ya":
                    loading()
                    return
                elif pilihan == "tidak":
                    loading()
                    break
                else:
                    print("Pilihan tidak valid. Silakan masukkan 'ya' atau 'tidak'.")

            print("Data barang berhasil ditambahkan.")

def Info_Barang():
    Info_cabang()
    nama_cabang = input("Masukkan nama cabang: ")
    file_path = f"{nama_cabang}_barang.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print("Data Barang untuk Cabang", nama_cabang + ":")
        headers = ["Nama Barang", "Harga Barang", "Jumlah Barang",
                   "Tanggal Kirim", "Jam Kirim"]
        table = []

        for _, row in df.iterrows():
            table.append([row['Nama Barang'], row['Harga Barang'], row['Jumlah Barang'],
                          row['Tanggal Kirim'], row['Jam Kirim']])
            
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("Cabang belum memiliki data barang.")

def edit_barang():
    Info_cabang()
    nama_cabang = input("Masukkan nama cabang: ")
    file_path = f"{nama_cabang}_barang.csv"
    if os.path.exists(file_path):
        Info_Barang(nama_cabang)
        try:
            barangnih = int(input("Masukan nomor barang yang ingin diubah: ")) - 1
            df = pd.read_csv(file_path)

            if 0 <= barangnih < len(df):
                while True:
                    nama_barang = input("Masukan nama barang: ")
                    if len(nama_barang) >= 4:
                        break
                    else:
                        print("Nama Barang harus minimal 4 karakter.")

                while True:
                    try:
                        harga = int(input("Masukan harga barang: "))
                        if harga >= 100000:
                            break
                        else:
                            print("Harga tidak valid. Harus minimal 100.000.")
                    except ValueError:
                        print("Masukan angka yang valid.")

                while True:
                    try:
                        jumlah_barang = int(input("Masukan jumlah barang: "))
                        if jumlah_barang != 0:
                            break
                        else:
                            print("Jumlah barang tidak boleh 0.")
                    except ValueError:
                        print("Masukan angka yang valid.")

                if 'Total' in df.columns:
                    df = df.drop(columns=['Total'])

                user_input = {
                    'Nama Barang': nama_barang,
                    'Harga Barang': harga,
                    'Jumlah Barang': jumlah_barang,
                    'Tanggal Kirim': input('Masukan tanggal Kirim: '),
                    'Jam Kirim': input('Masukan jam untuk diubah: '),
                }
                for field, value in user_input.items():
                    df.at[barangnih, field] = value

                df.at[barangnih, 'Total'] = df.at[barangnih, 'Harga Barang'] * df.at[barangnih, 'Jumlah Barang']

                df.to_csv(file_path, index=False)
                print("Barang berhasil diubah!")
            else:
                print("Error: Nomor barang tidak valid.")
        except ValueError:
            print("Error: Masukan nomor barang yang valid.")
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")

def data_cabang():
    try:
        with open("cabang/cabang.json", mode="r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("File cabang/cabang.json tidak ditemukan.")
        return []

def Tambah_Cabang():
    username = input("Masukkan username baru: ")

    existing_usernames = [entry["username"] for entry in data_cabang()]
    if username in existing_usernames:
        print("Username sudah ada. Tambahkan username yang berbeda.")
        return

    password = input("Masukkan password baru: ")

    try:
        with open("cabang/cabang.json", mode="r") as file:
            cabang_data = json.load(file)
    except json.decoder.JSONDecodeError:
        cabang_data = []

    cabang_data.append({"username": username, "password": password})

    with open("cabang/cabang.json", mode="w") as file:
        json.dump(cabang_data, file, indent=2)

    print("Data cabang berhasil ditambahkan.")

def edit_cabang():
    cabang_data = data_cabang()
    Info_cabang()
    cabangnih = int(input("Masukan indeks cabang yang akan diubah: "))

    if 0 <= cabangnih < len(cabang_data):
        username = input("Masukan username cabang: ")
        password = input("Masukan password cabang: ")

        if username:
            cabang_data[cabangnih]["username"] = username
        if password:
            cabang_data[cabangnih]["password"] = password

        with open("cabang/cabang.json", mode='w') as file:
            json.dump(cabang_data, file, indent=2)

        print("cabang berhasil diubah!")
    else:
        print("Error: Indeks cabang tidak valid.")

def hapus_cabang():
    cabang_data = data_cabang()
    Hapuscabang = int(input("Masukan indeks cabang yang akan dihapus: "))

    if 0 <= Hapuscabang < len(cabang_data):
        Hapuscabang2 = cabang_data.pop(Hapuscabang)
        with open("cabang/cabang.json", mode='w') as file:
            json.dump(cabang_data, file, indent=2)
        print(f"cabang {Hapuscabang2['username']} telah dihapus")
    else:
        print("Error: Indeks cabang tidak valid.")

def Info_cabang():
    cabang_data = data_cabang()
    if not cabang_data:
        print("Data cabang kosong.")
    else:
        print("Data cabang:")
        headers = ["Username"]
        table = [[entry.get("username", "N/A")] for entry in cabang_data]
        print(tabulate(table, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    while True:
        mengetik("╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗")
        mengetik("║                                     Aplikasi Manajemen Toko - Toko Cabang                            ║")
        mengetik("╠════════════════════════════════════════════════════════╦═════════════════════════════════════════════╣")
        mengetik("║                  1. Tambah Cabang                      ║                  6. Info Barang             ║")
        mengetik("║                  2. Info Cabang                        ║                  7. Edit Barang             ║")
        mengetik("║                  4. Hapus Cabang                       ║                  8. Penjualan Cabang        ║")
        mengetik("║                  3. Edit Cabang                        ║                  9. Keluar                  ║")
        mengetik("║                  5. Tambah Barang                      ║                                             ║")
        mengetik("╚════════════════════════════════════════════════════════╩═════════════════════════════════════════════╝")

        choice = input("Pilih opsi: ")
        loading()

        if choice == "1":
            Tambah_Cabang()
        elif choice == "2":
            Info_cabang()
        elif choice == "3":
            edit_cabang()
        elif choice == "4":
            hapus_cabang()
        elif choice == "5":
            Tambah_Barang()
        elif choice == "6":
            Info_Barang()
        elif choice == "7":
            edit_barang()
        elif choice == "8":
            total_penjualan_cabang()
        elif choice == "9":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih kembali.")
