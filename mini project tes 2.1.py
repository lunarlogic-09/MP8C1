import csv

NAMA_FILE_DEFAULT = "dataset_pizza_35_baris_analisis_bahan_harga.csv"

AKUN = {"pizza": "8C"}
MAKS_PERCOBAAN = 3

def input_pilihan(teks, pilihan_valid):
    while True:
        jawaban = input(teks).strip().upper()
        if jawaban in pilihan_valid:
            return jawaban
        print("Input tidak valid. Pilihan yang tersedia:", ", ".join(pilihan_valid))


def tampil_sampul():
    lebar = 65

    anggota = [
        ("Briantara Abimanyu Putra Arigisha", "2610932014"),
        ("Cahaya Latifa Aquastya Sakti", "2610932030"),
        ("Fachri Akeza Maulana", "2610933036"),
        ("Imam Maulana", "2610933040"),
    ]

    print("=" * lebar)
    print("MINI PROJECT".center(lebar))
    print("PEMROGRAMAN KOMPUTER".center(lebar))
    print("(Analisis Perbandingan Rata-Rata Harga Jual Pizza Berdasarkan".center(lebar))
    print("Tingkat Kelengkapan Bahan Baku Menggunakan Python)".center(lebar))
    print()
    print("Oleh:".center(lebar))
    print("Kelompok 8C".center(lebar))
    print()
    print("Anggota:".center(lebar))

    for nama, nim in anggota:
        print(f"{nama:<36}({nim})".center(lebar))

    print()
    print("Asisten Pembimbing:".center(lebar))
    print("Jihan Fitri Sakinah dan Hafzi Rizal".center(lebar))
    print()
    print("Dosen Pengampu:".center(lebar))
    print("Dr. Asmuliardi Muluk, S.T., M.T.".center(lebar))
    print()
    print("LABORATORIUM SISTEM INFORMASI DAN KEPUTUSAN".center(lebar))
    print("DEPARTEMEN TEKNIK INDUSTRI".center(lebar))
    print("FAKULTAS TEKNIK".center(lebar))
    print("UNIVERSITAS ANDALAS".center(lebar))
    print("2026".center(lebar))
    print("=" * lebar)
    print()


def login():

    percobaan = 1

    while percobaan <= MAKS_PERCOBAAN:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in AKUN and AKUN[username] == password:
            print(f"\nLogin berhasil. Selamat datang, {username}!")
            return username

        sisa = MAKS_PERCOBAAN - percobaan
        print(f"Username atau password salah. Sisa percobaan: {sisa}\n")
        percobaan += 1

    return None


def input_nama_file():
    print("\nMasukkan nama file CSV (tekan Enter untuk memakai file default)")
    print("Default:", NAMA_FILE_DEFAULT)
    nama = input("Nama file: ").strip()

    if nama == "":
        return NAMA_FILE_DEFAULT
    return nama


def input_ukuran():
    jawaban = input_pilihan("Pilih ukuran (S/M/L/SEMUA): ",
                            ["S", "M", "L", "SEMUA"])
    if jawaban == "SEMUA":
        return ["S", "M", "L"]
    return [jawaban]


def input_nomor_pizza(daftar_nama):
    print("\nDAFTAR NAMA PIZZA")
    print("-" * 45)

    nomor = 1
    for nama in daftar_nama:
        print(f"{nomor:<5}. {nama}")
        nomor += 1

    print("-" * 45)

    while True:
        jawaban = input(f"Pilih nomor pizza (1-{len(daftar_nama)}): ").strip()

        if jawaban.isdigit():
            angka = int(jawaban)
            if 1 <= angka <= len(daftar_nama):
                return daftar_nama[angka - 1]

        print(f"Input tidak valid. Masukkan angka 1 sampai {len(daftar_nama)}.")


def tekan_enter():
    input("\nTekan Enter untuk kembali ke menu...")

def baca_data(nama_file):
    try:
        with open(nama_file, "r", encoding="utf-8-sig") as file:

            pembaca = csv.DictReader(file, delimiter=";")

            kolom = ["pizza_name", "pizza_size",
                     "pizza_ingredients", "unit_price", "quantity"]

            lengkap = True

            if pembaca.fieldnames is None:
                lengkap = False
            else:
                pembaca.fieldnames = [nama.strip() for nama in pembaca.fieldnames]

                for nama in kolom:
                    if nama not in pembaca.fieldnames:
                        lengkap = False

            if lengkap == False:
                print("Kolom CSV tidak lengkap.")
                return []

            data = []

            for baris in pembaca:
                data.append(baris)

            return data

    except FileNotFoundError:
        print("File CSV tidak ditemukan.")
        return []


def validasi_data(baris):
    nama = baris["pizza_name"].strip()
    ukuran = baris["pizza_size"].strip().upper()
    bahan = baris["pizza_ingredients"].strip()

    harga = float(baris["unit_price"].replace(",", "."))
    jumlah = int(baris["quantity"])

    if nama != "" and ukuran in ["S", "M", "L"]:
        if bahan != "" and harga > 0 and jumlah > 0:
            return True

    return False

def hitung_kategori(data):
    for baris in data:
        bahan = baris["pizza_ingredients"].split(",")
        jumlah = len(bahan)

        baris["ingredient_count"] = jumlah

        if jumlah <= 3:
            kategori = "Sederhana"
        elif jumlah <= 5:
            kategori = "Sedang"
        elif jumlah <= 7:
            kategori = "Lengkap"
        else:
            kategori = "Sangat Lengkap"

        baris["ingredient_category"] = kategori

    return data


def menu_unik(data):
    hasil = []
    sudah_ada = []

    for baris in data:
        identitas = baris["pizza_name"] + "|" + baris["pizza_size"]

        if identitas not in sudah_ada:
            sudah_ada.append(identitas)
            hasil.append(baris)

    return hasil


def filter_ukuran(data, daftar_ukuran):
    hasil = []
    for baris in data:
        if baris["pizza_size"].strip().upper() in daftar_ukuran:
            hasil.append(baris)
    return hasil


def daftar_nama_pizza(data):
    hasil = []
    for baris in data:
        if baris["pizza_name"] not in hasil:
            hasil.append(baris["pizza_name"])
    return hasil


def cari_pizza(data, nama_pizza):
    hasil = []
    for baris in data:
        if baris["pizza_name"] == nama_pizza:
            hasil.append(baris)
    return hasil


def hitung_frekuensi(data):
    frekuensi = {}

    for baris in data:
        bahan = baris["pizza_ingredients"].split(",")
        jumlah = int(baris["quantity"])

        for nama_bahan in bahan:
            nama_bahan = nama_bahan.strip()

            if nama_bahan != "":
                if nama_bahan in frekuensi:
                    frekuensi[nama_bahan] += jumlah
                else:
                    frekuensi[nama_bahan] = jumlah

    return frekuensi


def urut_frekuensi(frekuensi):
    hasil = []

    for bahan in frekuensi:
        hasil.append([bahan, frekuensi[bahan]])

    for i in range(len(hasil)):
        for j in range(i + 1, len(hasil)):
            if hasil[j][1] > hasil[i][1]:
                sementara = hasil[i]
                hasil[i] = hasil[j]
                hasil[j] = sementara

    return hasil

def tampil_info(data, data_valid, data_tidak_valid, menu, frekuensi):
    print("\nINFORMASI DATA")
    print("-" * 40)
    print("Total Data Transaksi :", len(data))
    print("Data Valid           :", len(data_valid))
    print("Data Tidak Valid     :", len(data_tidak_valid))
    print("Jumlah Menu Unik     :", len(menu))
    print("Jumlah Bahan Baku    :", len(frekuensi))
    print("-" * 40)


def tampil_menu(data):
    print("\nDAFTAR MENU PIZZA")
    print("=" * 100)
    print(f"{'No':<5}| {'Nama Pizza':<30}| {'Ukuran':<10}| {'Jumlah Bahan':<15}| {'Kategori'}")
    print("-" * 100)

    if len(data) == 0:
        print("Data tidak ditemukan.")

    nomor = 1

    for baris in data:
        print(f"{nomor:<5}| {baris['pizza_name']:<30}| "
              f"{baris['pizza_size']:<10}| "
              f"{baris['ingredient_count']:<15}| "
              f"{baris['ingredient_category']}")
        nomor += 1

    print("=" * 100)


def analisis_harga(data, ukuran):
    kategori = ["Sederhana", "Sedang", "Lengkap", "Sangat Lengkap"]

    print("\nANALISIS RATA-RATA HARGA PIZZA")
    print("=" * 100)
    print(f"{'Ukuran':<10}| {'Kategori':<20}| {'Jumlah Menu':<15}| {'Rata-rata Harga'}")
    print("-" * 100)

    for u in ukuran:
        for k in kategori:
            total = 0
            jumlah = 0

            for baris in data:
                if baris["pizza_size"] == u:
                    if baris["ingredient_category"] == k:
                        total += float(baris["unit_price"].replace(",", "."))
                        jumlah += 1

            if jumlah > 0:
                rata = total / jumlah

                print(f"{u:<10}| {k:<20}| {jumlah:<15}| Rp{rata:.2f}")

    print("=" * 100)


def tampil_frekuensi(frekuensi, batas):
    hasil = urut_frekuensi(frekuensi)

    if batas > 0:
        hasil = hasil[:batas]

    print("\nFREKUENSI PENGGUNAAN BAHAN BAKU")
    print("=" * 75)
    print(f"{'No':<5}| {'Nama Bahan':<35}| {'Frekuensi'}")
    print("-" * 75)

    nomor = 1

    for baris in hasil:
        print(f"{nomor:<5}| {baris[0]:<35}| {baris[1]}")
        nomor += 1

    print("=" * 75)


def analisis_prioritas(frekuensi):
    total = 0

    for bahan in frekuensi:
        total += frekuensi[bahan]

    rata = total / len(frekuensi)

    tinggi = 0
    sedang = 0
    rendah = 0

    hasil = []

    for bahan in frekuensi:
        nilai = frekuensi[bahan]

        if nilai >= rata:
            status = "Tinggi"
            tinggi += 1
        elif nilai >= rata * 0.5:
            status = "Sedang"
            sedang += 1
        else:
            status = "Rendah"
            rendah += 1

        hasil.append([bahan, nilai, status])

    for i in range(len(hasil)):
        for j in range(i + 1, len(hasil)):
            if hasil[j][1] > hasil[i][1]:
                sementara = hasil[i]
                hasil[i] = hasil[j]
                hasil[j] = sementara

    print("\nSTATUS PRIORITAS PERSEDIAAN")
    print("=" * 85)
    print(f"{'No':<5}| {'Nama Bahan':<35}| {'Frekuensi':<15}| {'Prioritas'}")
    print("-" * 85)

    nomor = 1

    for baris in hasil:
        print(f"{nomor:<5}| {baris[0]:<35}| "
              f"{baris[1]:<15}| {baris[2]}")
        nomor += 1

    print("=" * 85)

    print("\nRINGKASAN PRIORITAS")
    print("=" * 50)
    print(f"{'Prioritas Tinggi':<25}: {tinggi} bahan")
    print(f"{'Prioritas Sedang':<25}: {sedang} bahan")
    print(f"{'Prioritas Rendah':<25}: {rendah} bahan")
    print("=" * 50)


def tampil_tidak_valid(data_tidak_valid):
    print("\nDATA TIDAK VALID")
    print("-" * 40)

    if len(data_tidak_valid) > 0:
        for nama in data_tidak_valid:
            print(nama)
    else:
        print("Tidak ada data tidak valid.")

    print("-" * 40)


def tampil_menu_utama():
    print("\n" + "=" * 65)
    print("               MINI PROJECT ANALISIS PIZZA")
    print("=" * 65)
    print("1. Informasi data")
    print("2. Daftar menu pizza (filter ukuran)")
    print("3. Analisis rata-rata harga (pilih ukuran)")
    print("4. Frekuensi penggunaan bahan baku")
    print("5. Status prioritas persediaan")
    print("6. Cari menu berdasarkan nama pizza (pilih nomor)")
    print("7. Data tidak valid")
    print("0. Keluar")
    print("=" * 65)

def main():
    tampil_sampul()
    user = login()

    if user is None:
        print("Login gagal. Program dihentikan.")
        return

    nama_file = input_nama_file()
    data = baca_data(nama_file)

    if len(data) == 0:
        print("Data tidak tersedia.")
        return

    data_valid = []
    data_tidak_valid = []

    for baris in data:
        try:
            if validasi_data(baris):
                data_valid.append(baris)
            else:
                data_tidak_valid.append(baris["pizza_name"])

        except (ValueError, TypeError, AttributeError):
            data_tidak_valid.append(baris["pizza_name"])

    if len(data_valid) == 0:
        print("Tidak ada data valid.")
        return

    data_valid = hitung_kategori(data_valid)
    menu = menu_unik(data_valid)
    frekuensi = hitung_frekuensi(data_valid)

    while True:
        tampil_menu_utama()
        pilihan = input_pilihan("Pilih menu (0-7): ",
                                ["0", "1", "2", "3", "4", "5", "6", "7"])

        if pilihan == "0":
            print("\nTerima kasih. Program selesai.")
            break

        elif pilihan == "1":
            tampil_info(data, data_valid, data_tidak_valid, menu, frekuensi)

        elif pilihan == "2":
            ukuran = input_ukuran()
            tampil_menu(filter_ukuran(menu, ukuran))

        elif pilihan == "3":
            ukuran = input_ukuran()
            analisis_harga(menu, ukuran)

        elif pilihan == "4":
            batas = input("Tampilkan berapa bahan teratas? "
                          "(Enter / 0 = semua): ").strip()
            if batas.isdigit():
                tampil_frekuensi(frekuensi, int(batas))
            else:
                tampil_frekuensi(frekuensi, 0)

        elif pilihan == "5":
            analisis_prioritas(frekuensi)

        elif pilihan == "6":
            nama = input_nomor_pizza(daftar_nama_pizza(menu))
            tampil_menu(cari_pizza(menu, nama))

        elif pilihan == "7":
            tampil_tidak_valid(data_tidak_valid)

        tekan_enter()


main()