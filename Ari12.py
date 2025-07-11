import csv
import os

class Node:
    def __init__(self, waktu, kegiatan):
        self.waktu = waktu
        self.kegiatan = kegiatan
        self.next = None

class JadwalLinkedList:
    def __init__(self):
        self.head = None
        self.undo_stack = []

    def tambah_kegiatan(self, waktu, kegiatan):
        new_node = Node(waktu, kegiatan)
        new_node.next = self.head
        self.head = new_node
        self.undo_stack.append(("hapus", waktu, kegiatan))
        self.simpan_ke_csv()

    def hapus_kegiatan(self, waktu):
        prev = None
        current = self.head
        while current:
            if current.waktu == waktu:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self.undo_stack.append(("tambah", current.waktu, current.kegiatan))
                self.simpan_ke_csv()
                return True
            prev = current
            current = current.next
        return False

    def undo(self):
        if not self.undo_stack:
            print("Tidak ada aksi yang bisa di-undo.")
            return
        aksi, waktu, kegiatan = self.undo_stack.pop()
        if aksi == "hapus":
            self.hapus_kegiatan(waktu)
        elif aksi == "tambah":
            self.tambah_kegiatan(waktu, kegiatan)

    def tampilkan(self):
        current = self.head
        if not current:
            print("Jadwal masih kosong.")
            return
        print("Jadwal Belajar Mahasiswa:")
        while current:
            print(f"{current.waktu} - {current.kegiatan}")
            current = current.next

    def simpan_ke_csv(self):
        with open('jadwal.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            current = self.head
            while current:
                writer.writerow([current.waktu, current.kegiatan])
                current = current.next

    def muat_dari_csv(self):
        try:
            with open('jadwal.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reversed(list(reader)):
                    self.tambah_kegiatan(row[0], row[1])
        except FileNotFoundError:
            pass

kegiatan_default = [
    ("06:00", "Bangun dan persiapan kuliah"),
    ("07:30", "Kuliah Pagi"),
    ("10:00", "Review materi kuliah"),
    ("12:00", "Istirahat dan makan siang"),
    ("13:00", "Belajar mandiri / perpustakaan"),
    ("15:00", "Mengerjakan tugas"),
    ("17:00", "Organisasi / olahraga"),
    ("19:00", "Makan malam"),
    ("20:00", "Mengulang pelajaran / baca buku"),
    ("22:00", "Istirahat malam"),
]

jadwal = JadwalLinkedList()

if not os.path.exists('jadwal.csv') or os.path.getsize('jadwal.csv') == 0:
    for waktu, kegiatan in reversed(kegiatan_default):
        jadwal.tambah_kegiatan(waktu, kegiatan)
else:
    jadwal.muat_dari_csv()

def menu():
    while True:
        print("\n=== MENU JADWAL BELAJAR ===")
        print("1. Tampilkan Jadwal")
        print("2. Tambah Kegiatan")
        print("3. Hapus Kegiatan")
        print("4. Undo Aksi Terakhir")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            jadwal.tampilkan()
        elif pilihan == "2":
            waktu = input("Masukkan waktu (HH:MM): ")
            kegiatan = input("Masukkan kegiatan: ")
            jadwal.tambah_kegiatan(waktu, kegiatan)
            print("Kegiatan ditambahkan.")
        elif pilihan == "3":
            waktu = input("Masukkan waktu kegiatan yang ingin dihapus: ")
            if jadwal.hapus_kegiatan(waktu):
                print("Kegiatan berhasil dihapus.")
            else:
                print("Kegiatan tidak ditemukan.")
        elif pilihan == "4":
            jadwal.undo()
            print("Undo berhasil dilakukan.")
        elif pilihan == "5":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih antara 1-5.")

if __name__ == "__main__":
    menu()