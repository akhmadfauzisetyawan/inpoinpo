from tabulate import tabulate
import time, random, shutil, os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime 
import csv

def mengetik(s):
    terminal_width, _ = shutil.get_terminal_size()
    padding = (terminal_width - len(s)) // 2
    print(" " * padding + s)
    time.sleep(random.random() * 0.001)
    
def sambut_pengguna(username, cabang):
    print(f"Selamat datang, {username} di Cabang {cabang}!")    

def loading():
    mengetik('\033[32m')
    mengetik("╔══════════════════════════════════════════════════════════════════════╗")
    mengetik("║ Loading ..............                                               ║")
    mengetik("╚══════════════════════════════════════════════════════════════════════╝")
    time.sleep(1)
    os.system("cls")

def sembako_barang(nama_cabang):
    file_path = f"{nama_cabang}_barang.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        sembako_items = df["Nama Barang"].unique().tolist()
        
        print("Daftar Barang Sembako yang Tersedia:")
        for i, item in enumerate(sembako_items, start=1):
            print(f"{i}. {item}")
        
        bobot = df["Jumlah Barang"].tolist()
        nilai = df["Harga Barang"].tolist()
        
        while True:
            try:
                total_nilai = float(input("Masukkan jumlah uang yang akan digunakan untuk membeli sembako: "))
                if total_nilai <= 0:
                    print("Masukkan jumlah uang yang valid (lebih besar dari 0).")
                else:
                    break
            except ValueError:
                print("Masukkan angka yang valid untuk jumlah uang.")
        
        hasil = []
        total_bobot = 0
        total_nilai_terpilih = 0
        
        while total_nilai_terpilih < total_nilai:
            idx = random.randint(0, len(bobot) - 1)
            if total_bobot + bobot[idx] <= total_nilai:
                hasil.append(df.iloc[idx])
                total_bobot += bobot[idx]
                total_nilai_terpilih += nilai[idx]
                
        hasil_df = pd.DataFrame(hasil)
        print(f"Sembako Barang untuk Cabang {nama_cabang} (Total Harga: Rp{total_nilai_terpilih}):")
        print(tabulate(hasil_df, headers='keys', tablefmt='grid'))
        tambah_histori(nama_cabang, "Tambah", hasil_df)
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")

def hapus_barang(nama_cabang):
    file_path = f"{nama_cabang}_barang.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print("Data Barang:")
        print(tabulate(df, headers='keys', tablefmt='grid'))
        try:
            barangnih = int(input("Masukkan nomor barang yang ingin dihapus: ")) - 1
            if 0 <= barangnih < len(df):
                df = df.drop(barangnih).reset_index(drop=True)
                df.to_csv(file_path, index=False)
                print("Barang berhasil dihapus!")
            else:
                print("Nomor barang tidak valid.")
        except ValueError:
            print("Error: Masukkan nomor barang yang valid.")
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")

def penjualan_barang(nama_cabang):
    file_path = f"{nama_cabang}_barang.csv"
    transaksi_path = f"{nama_cabang}_transaksi_penjualan.csv"

    if not os.path.exists(transaksi_path):
        with open(transaksi_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama Barang", "Harga Barang", "Jumlah Terjual", "Tanggal Penjualan", "Jam Penjualan"])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        while True:
            print("Data Barang:")
            print(tabulate(df.reset_index(drop=True), headers='keys', tablefmt='grid')) 
            try:
                barangnih_input = input("Masukkan nomor barang yang terjual (atau 'n' untuk keluar): ")
                if barangnih_input.lower() == 'n':
                    print("Selesai mencatat penjualan.")
                    break
                barangnih = int(barangnih_input)  

                if 0 <= barangnih < len(df):
                    jumlah_terjual_input = input("Masukkan jumlah barang yang terjual: ")
                    jumlah_terjual = int(jumlah_terjual_input)
                    if jumlah_terjual <= df.at[barangnih, 'Jumlah Barang']:
                        df.at[barangnih, 'Jumlah Barang'] -= jumlah_terjual
                        nama_barang = df.at[barangnih, 'Nama Barang']
                        harga_barang = df.at[barangnih, 'Harga Barang']

                        if df.at[barangnih, 'Jumlah Barang'] == 0:
                            df = df.drop(barangnih).reset_index(drop=True)

                        df.to_csv(file_path, index=False)
                        
                        waktu_sekarang = datetime.datetime.now()
                        tanggal_penjualan = waktu_sekarang.strftime("%Y-%m-%d")
                        jam_penjualan = waktu_sekarang.strftime("%H:%M:%S")
                        
                        with open(transaksi_path, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow([nama_barang, harga_barang, jumlah_terjual, tanggal_penjualan, jam_penjualan])

                        print("Penjualan berhasil dicatat dan transaksi disimpan!")
                    else:
                        print("Jumlah terjual melebihi stok yang ada.")
                else:
                    print("Nomor barang tidak valid.")
            except ValueError:
                print("Error: Masukkan nomor dan jumlah barang yang valid.")
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")

def lihat_barang(nama_cabang):
    file_path = f"{nama_cabang}_barang.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(f"Data Barang untuk Cabang {nama_cabang}:")
        print(tabulate(df, headers='keys', tablefmt='grid'))
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")
def bubble_sort(items):
    n = len(items)
    for i in range(n):
        for j in range(0, n-i-1):
            if items[j][1] < items[j+1][1]:
                items[j], items[j+1] = items[j+1], items[j]

def barang_terlaris(nama_cabang):
    file_path = f"{nama_cabang}_transaksi_penjualan.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        barang_items = df.groupby('Nama Barang')['Jumlah Barang'].sum().items()
        barang_list = list(barang_items)
        
        bubble_sort(barang_list)

        print(f"Barang Terlaris untuk Cabang {nama_cabang}:")
        print(tabulate(barang_list, headers=['Nama Barang', 'Jumlah Terjual'], tablefmt='grid'))
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")


def cari_barang(nama_cabang):
    file_path = f"{nama_cabang}_barang.csv"
    if os.path.exists(file_path):
        nama_barang = input("Masukkan nama barang yang ingin dicari: ")
        df = pd.read_csv(file_path)

        df = df.sort_values(by='Nama Barang', key=lambda col: col.str.lower()).reset_index(drop=True)

        batas_bawah = 0
        batas_atas = len(df) - 1
        hasil_cari = []

        while batas_bawah <= batas_atas:
            tengah = (batas_bawah + batas_atas) // 2
            nama_tengah = df.iloc[tengah]["Nama Barang"].lower()

            if nama_tengah.startswith(nama_barang.lower()):
                hasil_cari.append(df.iloc[tengah])
                i = tengah - 1
                while i >= 0 and df.iloc[i]["Nama Barang"].lower().startswith(nama_barang.lower()):
                    hasil_cari.append(df.iloc[i])
                    i -= 1
                i = tengah + 1
                while i < len(df) and df.iloc[i]["Nama Barang"].lower().startswith(nama_barang.lower()):
                    hasil_cari.append(df.iloc[i])
                    i += 1
                break
            elif nama_tengah < nama_barang.lower():
                batas_bawah = tengah + 1
            else:
                batas_atas = tengah - 1

        if hasil_cari:
            hasil_cari_df = pd.DataFrame(hasil_cari)
            print(f"Hasil Pencarian untuk '{nama_barang}':")
            print(tabulate(hasil_cari_df, headers='keys', tablefmt='grid'))
        else:
            print(f"Barang dengan nama yang dimulai dengan '{nama_barang}' tidak ditemukan.")
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")

def tambah_histori(nama_cabang, operasi, barang=None):
    file_path = f"{nama_cabang}_histori.txt"
    with open(file_path, "a") as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if operasi == "Tambah":
            file.write(f"{timestamp} - Tambah barang: {barang}\n")
        elif operasi == "Hapus":
            file.write(f"{timestamp} - Hapus barang: {barang}\n")
        elif operasi == "Penjualan":
            file.write(f"{timestamp} - Penjualan barang: {barang}\n")
        elif operasi == "Update":
            file.write(f"{timestamp} - Update barang: {barang}\n")
        else:
            file.write(f"{timestamp} - Operasi tidak diketahui\n")
    
def graf_barang(nama_cabang):
    file_path = f"{nama_cabang}_transaksi_penjualan.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        barang_items = df.groupby('Nama Barang')['Jumlah Barang'].sum().items()
        barang_list = list(barang_items)
        
        bubble_sort(barang_list)

        # Extract top 10 items
        top_items = barang_list[:10]
        top_items_df = pd.DataFrame(top_items, columns=['Nama Barang', 'Jumlah Terjual'])

        # Plot the bar graph
        plt.figure(figsize=(10, 6))
        bars = plt.bar(top_items_df['Nama Barang'], top_items_df['Jumlah Terjual'], color='skyblue')
        plt.title(f"Top 10 Barang Terlaris di Cabang {nama_cabang}")
        plt.xlabel("Nama Barang")
        plt.ylabel("Jumlah Terjual")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')

        plt.show()
    else:
        print(f"File barang untuk cabang '{nama_cabang}' tidak ditemukan.")

def main():
    if len(sys.argv) > 1:
        nama_cabang = sys.argv[1]
    else:
        print("Error: Nama cabang tidak diberikan.")
        return
    while True:
        mengetik("╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗")
        mengetik("║            Aplikasi Manajemen Toko - Toko Cabang                                 # Options           ║")
        mengetik("╠════════════════════════════════════════════════════════╦═════════════════════════════════════════════╣")
        mengetik("║                  1. Sembako                            ║                  5. Lihat Barang            ║")
        mengetik("║                  2. Hapus Stok                         ║                  6. Barang Terlaris         ║")
        mengetik("║                  3. Penjualan                          ║                  7. Cari Barang             ║")
        mengetik("║                  4. Graf Penjualan                     ║                  8. Keluar                  ║")
        mengetik("╚════════════════════════════════════════════════════════╩═════════════════════════════════════════════╝")
        pilihan = input("Masukan pilihan Anda: ")
        loading()
        
        if pilihan == '1':
            sembako_barang(nama_cabang)
            tambah_histori(nama_cabang, "Tambah")
        elif pilihan == '2':
            hapus_barang(nama_cabang) 
            tambah_histori(nama_cabang, "Hapus")
        elif pilihan == '3':
            penjualan_barang(nama_cabang)
            tambah_histori(nama_cabang, "Penjualan")
        elif pilihan == '4':
            graf_barang(nama_cabang)
            tambah_histori(nama_cabang, "Graf")
        elif pilihan == '5':
            lihat_barang(nama_cabang)
            tambah_histori(nama_cabang, "Lihat")
        elif pilihan == '6':
            barang_terlaris(nama_cabang)
            tambah_histori(nama_cabang, "Terlaris")
        elif pilihan == '7':
            cari_barang(nama_cabang)
            tambah_histori(nama_cabang, "Cari")
        elif pilihan == '8':
            break
        else:
            print("Pilihan tidak valid. Silakan pilih kembali.")


if __name__ == "__main__":
    main()
