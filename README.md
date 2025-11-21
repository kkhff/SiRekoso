# SiRekoso: Asisten Keuangan Kos Gen Z

SiRekoso (**Sistem Rekapitulasi Kos**) adalah asisten keuangan berbasis konsol (CLI) yang dirancang khusus untuk mengelola anggaran bulanan anak kos. Aplikasi ini membantu Anda mencatat pengeluaran harian, melacak sisa limit, dan memprediksi kapan anggaran akan habis.



## Fitur Utama

SiRekoso dirancang untuk menyediakan *insight* keuangan yang cepat dan praktis:

| Kategori | Fitur | Deskripsi |
| :--- | :--- | :--- |
| **Pencatatan** | **Tambah Pengeluaran** | Mencatat transaksi harian lengkap dengan tanggal dan deskripsi. |
| **Manajemen Anggaran** | **Siklus Bulanan Otomatis** | Mengelola anggaran dalam siklus **30 hari** penuh. |
| | **Limit Harian Dinamis** | Secara otomatis menghitung sisa limit harian Anda berdasarkan pengeluaran hari ini. |
| | **Limit Bulanan Derivasi** | Total limit bulanan dihitung otomatis dari Limit Harian yang Anda tetapkan. |
| **Kontrol** | **Mode Hemat** | Mengaktifkan mode hemat yang secara otomatis **mengurangi Limit Harian dan Bulanan** sebesar persentase yang telah ditentukan, membantu Anda mengerem pengeluaran saat kritis. |
| **Pelaporan** | **Laporan Harian & Bulanan** | Melihat detail pengeluaran pada hari atau bulan tertentu, termasuk total pengeluaran harian. |
| **Aksi Cepat** | **Edit & Hapus Pengeluaran** | Memungkinkan Anda memperbaiki atau menghapus catatan pengeluaran yang salah langsung dari laporan harian. |
| **Prediksi** | **"Kapan Dompet Nangis"** | Fitur prediksi untuk memperkirakan tanggal di mana sisa anggaran akan habis, berdasarkan rata-rata pengeluaran dan limit harian. |
| **Kustomisasi** | **Dukungan Dua Bahasa** | Tersedia mode bahasa **Indonesia** dan **Jawa** (Ngoko / Suroboyo). |
| | **Pengaturan Anggaran** | Mengatur ulang *default* Limit Harian, menambah anggaran di tengah siklus, dan mereset data. |



## Teknologi dan Instalasi

Proyek ini dibangun murni menggunakan **Python**.

### Persyaratan Sistem
* **Python Version:** **3.8 atau lebih baru** (Disarankan Python 3.10+)
* **Sistem Operasi:** Windows, macOS, atau Linux.

### Cara Menjalankan

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/kkhff/SiRekoso.git
    cd SiRekoso
    ```
2.  **Siapkan Struktur Folder:** Pastikan Anda memiliki struktur folder berikut. File data dan konfigurasi akan dibuat secara otomatis saat program dijalankan:
    ```
    .
    ├── main.py
    ├── core/
    ├── data/
    │   └── records.json  <-- Dibuat otomatis saat runtime
    └── config/
        └── settings.json <-- Dibuat otomatis saat runtime
    ```
3.  **Jalankan Aplikasi:**
    *Gunakan `python3` untuk menjamin penggunaan interpreter Python versi 3:*
    ```bash
    python3 main.py
    ```
    *(Jika perintah `python3` tidak ditemukan, coba gunakan `python main.py`)*

4.  **Inisialisasi Awal:** Saat pertama kali dijalankan, aplikasi akan meminta Anda mengatur **Anggaran Dasar** dan **Tanggal Awal Siklus Kos.** Anda dapat mengatur **Limit Harian** di Menu **Opsi [6] Atur Anggaran & Reset Data.**



## Struktur File Proyek

| File/Direktori | Deskripsi | Catatan Git |
| :--- | :--- | :--- |
| `main.py` | File utama yang menjalankan *loop* aplikasi dan menampilkan menu. | Komit/Push |
| `core/analysis.py` | Logika perhitungan keuangan, `get_financial_summary()`, dan Mode Hemat. | Komit/Push |
| `core/data_manager.py` | Bertanggung jawab untuk memuat dan menyimpan data dari file JSON. | Komit/Push |
| `core/expenses.py` | Fungsi untuk menambah, mengedit, menghapus, dan menampilkan laporan pengeluaran. | Komit/Push |
| `core/helpers.py` | Utilitas (format Rupiah, validasi input) dan **Lokalisasi Bahasa**. | Komit/Push |
| `config/settings.json` | Menyimpan konfigurasi pengguna (Anggaran, Limit Harian, Mode Bahasa, Mode Hemat). | **Dibuat Otomatis saat Program Dijalankan.** |
| `data/records.json` | Menyimpan semua riwayat transaksi/pengeluaran. | **Dibuat Otomatis saat Program Dijalankan.** |



## Kontribusi

Jika Anda menemukan *bug* atau memiliki ide fitur baru, silakan buka *issue* atau kirimkan *pull request* di repository ini. Kami menyambut kontribusi dari komunitas Gen Z yang ingin mengelola keuangan kos dengan lebih baik!