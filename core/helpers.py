import random
import datetime
import re
from core.data_manager import load_settings, save_settings 

# --- FORMATTING & UTILITY ---

def format_rupiah(angka):
    try:
        s = f"{int(angka):,}"
        s = s.replace(",", ".")
        return f"Rp {s}"
    except:
        return f"Rp {0}"

def validate_number(prompt):
    while True:
        try:
            value = input(prompt).replace('.', '').replace(',', '')
            if value == "":
                return None
            if not value.isdigit() :
                 print("Error: Masukkan hanya angka (tanpa titik atau koma).")
                 continue
            return int(value)
        except ValueError:
            print("Error: Masukkan hanya angka yang valid, Rek.")
        except KeyboardInterrupt:
            # Handle Ctrl+C
            return None

def get_current_date():
    return datetime.datetime.now().strftime("%d/%m/%Y")

# --- LOKALISASI (BAHASA) & PESAN ---

def get_localized_message(category):   
    # --- KOREKSI: DATA PESAN DIMASUKKAN KE SINI AGAR SELALU TERSEDIA ---
    PESAN_NOTIFIKASI = {
        "JAWA": {
            "OVER_LIMIT": [
                "Bahaya! Sirekoso wis kesel ngandani. Duwitmu wis nnangis tenan",
                "DUWIT ENTEK! Jupuken hape, telpon wong tuwomu, njaluk kiriman!",
                "Saldo Iki: Kosong. Selamat! Kowe wis sukses dadi wong mlarat tenan."
            ],
            "NANGIS": [
                "Dompet KO sadurunge gajian. Siap-siap urip ngirit banget nang tanggal-tanggal krusial.",
                "Le, SiRekoso nangis ndelok prediksimu. Mulai saiki, kudu ngirit tenanan!",
                "Bahaya! Dhuwitmu diprediksi entek pas tanggal-tanggal panas. Ndang mikir solusi!"
            ],
            "WASPADA": [
                "Warning! Kowe boros banget. Ndang eling-eling, jupuk catetanmu, cek maneh belanjamu.",
                "Awas! Kowe duwe potensi nangis sadurunge gajian. Wis, turu wae!",
                "Ati-ati! SiRekoso ngerti belanjamu boros. Fokus sing paling penting wae, Rek."
            ],
            "AMAN_SENTOSA": [
                "Santuy, Rek! Sangu-mu jek on track, iso jajan sitik. Good job!",
                "Lanjut turu/mabar, duwitmu aman. Pertahankan!",
                "Status: Ijo Royo-royo! SiRekoso ngijini, awamu isih oleh jajan sithik-sithik."
            ]
        },
        "INDONESIA": {
            "OVER_LIMIT": [
                "Sisa Saldo: Nihil. Selamat! Anda sukses menjadi kaum mendang-mending.",
                "SALDO HABIS! Segera hubungi orangtua, atau siap-siap makan nasi + garam.",
                "Darurat Kritis! SiRekoso melambaikan tangan. Anggaran bulan ini sudah mencapai batas akhir"
            ],
            "NANGIS": [
                "Dompet K.O. sebelum waktunya. Persiapkan diri untuk hidup tanpa sisa anggaran di tanggal krusial.",
                "Wahai Anak Kos, SiRekoso sedih melihat prediksimu. Fokus hidup hemat mulai detik ini!",
                "Bahaya! Saldo terancam habis di tengah bulan. Segera buat rencana darurat!"
            ],
            "WASPADA": [
                "Peringatan! Pengeluaranmu di atas rata-rata. Perbaiki jalur pengeluaran sebelum terlambat.",
                "Perhatian serius! Anda berpotensi overlimit sebelum akhir periode. Hati-hati memilih menu makan.",
                "Stop! SiRekoso memintamu segera aktifkan Mode Hemat. Fokus pada kebutuhan yang PENTING saja."
            ],
            "AMAN_SENTOSA": [
                "Santai! Saldo masih aman, kamu bisa jajan sedikit.",
                "Pengeluaranmu terkontrol. Pertahankan pola hematmu!",
                "Status: Hijau ! SiRekoso izin, kamu masih bisa jajan kopi sesekali."
            ]
        }
    }

    settings = load_settings()
    mode = settings.get("MODE_BAHASA", "INDONESIA")
    
    pesan_list = PESAN_NOTIFIKASI.get(mode, {}).get(category, [])
    
    if pesan_list:
        return random.choice(pesan_list)
    else:
        return "Notifikasi darurat: Hubungi developer. Data pesan rusak!"

def get_text(key_id):

    texts = {
        "JAWA": {
            "menu_utama": "--- MENU UTAMA ---",
            "sisa_limit_daily": "Limit dino iki sisa: ",
            "sisa_limit_monthly": "Limit Wulan iki sisa",
            "opsi_1": "1. Tambah Pengeluaran Anyar",
            "opsi_2": "2. Laporan Pengeluaran",
            "opsi_3": "3. Prediksi Kapan Dompet Nangis",
            "opsi_4": "4. Ganti Mode Boso",
            "opsi_5": "5. Mode Ngirit",
            "opsi_6": "6. Atur Anggaran & Reset Data",
            "opsi_7": "7. Metu",
            "pilih_menu": "Pilih menune, Rek: ",
            "expense_judul": "       --- TAMBAH PENGELUARAN ANYAR ---",
            "expense_saved" : "wis dicatet, Rek!",
            "Default_tanggal": "Enter gawe default",
            "input_tanggal": "Tanggal (DD/MM/YYYY - default dino iki",
            "err_input_tanggal": "Error: Format tanggal kudu DD/MM/YYYY (contoh: 05/11/2025).",
            "enter_batal": "Enter gawe batal",
            "deskripsi": "Keterangan (misal: Sego Goreng Cak Ji): ",
            "err_deskripsi": "Error: Deskripsi gak oleh kosong. Pembatalan input.",
            "enter_menu": "Enter gawe balik nang Menu Utama...",
            "harga": "Rego (Ongko tok): ",
            "err_harga": "Error: harga gak valid. Pembatalan input.",
            "laporan_judul": "        --- LAPORAN PENGELUARAN  ---",
            "laporan_opsi1": "[1] Dino iki",
            "laporan_opsi2": "[2] wulan iki",
            "laporan_opsi3": "[3] Balik Nang Menu",
            "pilih_laporan": "Pilih jenis laporan: ",
            "pilihan_invalid": "Pilihan gak valid rek, tolong pilih seng onok ae",
            "total_bulanan":  "Total Pengeluaran wulan Iki:    ",
            "sisa_saldo":  "Sisa Saldo:                     ",
            "avg_pengeluaran": "Rata-rata Pengeluaran Bendino:  ",
            "no_expense": "Durung ono pengeluaran seng dicatet. Santai, Rek!",
            "enter_laporan": "Enter gawe balik nang sub-menu laporan...",
            "daily_expense_judul": "     --- DETAIL PENGELUARAN DINO IKI ---",
            "total_harian": "TOTAL PENGELUARAN DINO IKI: ",
            "aksi_msg": "1 = Edit, 2 = Hapus, (Enter gawe balik)",
            "hapus_msg": "Yakin ta ngehapus pengeluaran?",
            "hapus_input": "'Y' gawe lanjut, Enter gawe batal: ",
            "err_daily": "[ERROR] onok masalah pas memproses aksi: ",
            "monthly_expense_judul": "    --- DETAIL PENGELUARAN WULAN IKI ---",
            "edit_msg": "Jarno kosong nek gak pingin di ganti",
            "edit_sukses": "Sukses ngedit pengeluaran",
            "hapus_sukses": "Sukses menghapus pengeluaran",
            "id_not_found": "Id gak ketemu rek",
            "new_deskripsi": "Keterangan anyar (lawas: ",
            "new_harga": "Rego anyar (lawas: " ,
            "enter_laporan_daily": "Enter gawe balik nang laporan dino iki...",
            "cancel_edit": "Edit pengeluaran dibatalno",
            "prediksi_judul": "       --- PREDIKSI DOMPET NANGIS ---",
            "sisa_hari_siklus" : "Sisa Dino Siklus:               ",
            "limit_daily_aktif":       "Limit dinoan seng aktif:        ",
            "limit_monthly_aktif":     "Limit Wulanan seng aktif:       ",
            "prediksi_over_limit": "Duwitmu wes entek!",
            "prediksi_aman": "Duwitmu bertahan sampek akhir wulan atau",
            "prediksi_kritis": "SiRekoso ngiro-ngiro, dhuwitmu kari separuh, cukup sampek tanggal",
            "prediksi_nangis": "Miturut ramalan, sisa dhuwitmu bakal entek pas tanggal",
            "bahasa_judul": "           --- GANTI MODE BOSO ---",
            "bahasa_sekarang": "Mode Boso saiki: ",
            "b_indo": "Mode Boso: INDONESIA wis diaktifno.",
            "b_jawa": "Mode Boso: JAWA wis diaktifno.",
            "mode_hemat_judul": "             --- MODE NGIRIT ---",
            "hemat_off": "Mode hemat off. Balik nang limit normalmu.",
            "limit_off": "Limit dinoan bali dadi",
            "hemat_on": "Ojok kakean polah! Limit di-rem, Rek. Sukses hemat!",
            "limit_on": "Limit dinoan saiki dadi",
            "atur_anggaran_judul": "      --- ATUR ANGGARAN & PENGATURAN ---",
            "anggaran_opsi1": "[1] Tambah Anggaran (Wulan Iki : ",
            "anggaran_opsi2": "[2] Limit Dinoan :     ",
            "anggaran_opsi3": "[3] Mulai Siklus Anggaran anyar (Wajib Bulanan!)",
            "anggaran_opsi4": "[4] Reset Data Pengeluaran (Hapus Kabeh Riwayat Pengeluaran)",
            "anggaran_opsi5": "[5] Balik Nang Menu",
            "pilih_anggaran": "Pilih setting sing pengen diganti (1-5): ",
            "add_anggaran_judul": "          --- TAMBAH ANGGARAN ---",
            "tambah_budget_prompt": "Masukno Jumlah    ",
            "add_anggaran": "Anggaran berhasil ditambahkan!",
            "total_add_anggaran": "Total Anyar:  ",
            "minimum_spend": "Gak logis blas!",
            "anggaran_sukses": "Anggaran Wulanan sukses diganti.",
            "limit_judul": "            --- ATUR LIMIT ---",
            "limit_sukses": "Limit Dinoan sukses diganti.",
            "err_angka": "Error: Kudu ongko tok.",
            "warn_reset": "PERINGATAN! Aksi iki bakal ngehapus KABEH riwayat pengeluaranmu",
            "konfirmasi_reset": "Ketik 'LANJUT' gawe ngelanjutno reset (Enter gawe batal): ",
            "enter_anggaran": "Tekan Enter gawe balik...",
            "atur_limit_harian": "Masukno Limit Dinoan anyar (saiki",
            "siklus_baru_judul": "      --- SIKLUS ANGGARAN ANYAR ---",
            "warn_siklus_baru": "Aksi iki nimpa anggaran wulan iki lan ngereset periode siklus. Riwayat lawas TETEP KESIMPAN.",
            "prompt_konfirmasi_siklus": "Ketik 'YA' gawe mulai siklus anyar: ",
            "siklus_batal": "Operasi dibatalno",
            "input_anggaran_dasar": "Masukno ANGGARAN DASAR total wulan iki:",
            "siklus_sukses": "Siklus anggaran anyar sukses dianyari",
            "anggaran_dasar_baru": "Anggaran Dasar Anyar",
            "tanggal_siklus_baru": "Tanggal Mulai Siklus",
            "input_tanggal_siklus": "Masukno Tanggal Awal Siklus (DD/MM/YYYY)",
            "err_tanggal_siklus": "Error: Format tanggal kudu DD/MM/YYYY.",
            "atur_budget_bulanan": "Masukno Anggaran Wulanan anyar (saiki",
            "reset_success": "Data pengeluaran wis resik! SiRekoso siap demo teko nol." ,
            "gagal_reset": "Gagal ngehapus data.",
            "reset_batal": "reset data dibatalno.",
            "keluar": "Maturnuwun, Rek! Ojok lali cek saldo terus. SiRekoso pamit. :D",

        },
        "INDONESIA": {
            "menu_utama": "--- MENU UTAMA ---",
            "sisa_limit_daily": "Limit hari ini sisa: ",
            "sisa_limit_monthly": "Limit Bulan ini sisa",
            "opsi_1": "1. Tambah Pengeluaran Baru",
            "opsi_2": "2. Laporan Pengeluaran",
            "opsi_3": "3. Prediksi Kapan Dompet Nangis",
            "opsi_4": "4. Ganti Mode Bahasa",
            "opsi_5": "5. Mode Hemat",
            "opsi_6": "6. Atur Anggaran & Reset Data",
            "opsi_7": "7. Keluar",            
            "pilih_menu": "Pilih menu: ",
            "expense_judul": "       --- TAMBAH PENGELUARAN BARU ---",
            "expense_saved" : "Telah dicatat!",
            "Default_tanggal": "Enter untuk default",
            "input_tanggal": "Tanggal (DD/MM/YYYY - default hari ini",
            "err_input_tanggal": "Error: Format tanggal kudu DD/MM/YYYY (contoh: 05/11/2025).",
            "enter_batal": "Enter untuk batal",
            "deskripsi": "Keterangan (misal: Nasi Goreng Pak Ji): ",
            "err_deskripsi": "Error: Deskripsi tidak boleh kosong. Pembatalan input.",
            "enter_menu": "Enter untuk kembali ke Menu Utama...",
            "harga": "Harga (Angka saja): ",
            "err_harga": "Error: harga tidak valid. Pembatalan input.",
            "laporan_judul": "        --- LAPORAN PENGELUARAN  ---",
            "laporan_opsi1": "[1] Hari ini",
            "laporan_opsi2": "[2] Bulan ini",
            "laporan_opsi3": "[3] Kembali Ke Menu",
            "pilih_laporan": "Pilih jenis laporan: ",
            "pilihan_invalid": "Pilihan tidak valid, tolong pilih yang ada saja",
            "total_bulanan": "Total Pengeluaran Bulan Ini:  ",
            "sisa_saldo": "Sisa Saldo Tersedia:          ",
            "avg_pengeluaran": "Rata-rata Pengeluaran Harian: ",
            "no_expense": "Belum ada pengeluaran yang dicatat",
            "enter_laporan": "Enter untuk kembali ke sub-menu laporan...",
            "daily_expense_judul": "--- DETAIL PENGELUARAN HARI INI ---",
            "total_harian": "TOTAL PENGELUARAN HARI INI: ",
            "aksi_msg": "1 = Edit, 2 = Hapus, (Enter untuk kembali)",
            "hapus_msg": "Apakah anda yakin menghapus pengeluaran?",
            "hapus_input": "'Y' untuk lanjut, Enter untuk batal: ",
            "err_daily": "[ERROR] Terjadi masalah saat memproses aksi: ",
            "monthly_expense_judul": "    --- DETAIL PENGELUARAN BULAN INI ---",
            "edit_sukses": "Sukses edit pengeluaran",
            "hapus_sukses": "Sukses menghapus pengeluaran",
            "id_not_found": "Id tidak ditemukan",
            "edit_msg": "Biarkan kosong untuk tidak mengubah",
            "new_deskripsi": "Keterangan baru (lama: ",
            "new_harga": "Harga baru (lama: " ,
            "enter_laporan_daily": "Enter untuk kembali ke laporan hari ini...",
            "cancel_edit": "Edit pengeluaran dibatalkan",
            "prediksi_judul": "       --- PREDIKSI DOMPET NANGIS ---",
            "sisa_hari_siklus" : "Sisa Hari Siklus:             ",
            "limit_daily_aktif":       "Limit harian yang aktif:      ",
            "limit_monthly_aktif":     "Limit Bulanan Yang aktif:     ",
            "prediksi_over_limit": "Uangmu sudah habis!",
            "prediksi_aman": "Uangmu bertahan sampai akhir bulan atau",
            "prediksi_kritis": "Prediksi SiRekoso, uangmu tinggal setengah, hanya cukup sampai tanggal",
            "prediksi_nangis": "Sesuai prediksi, sisa anggaranmu akan habis total pada tanggal",
            "bahasa_judul": "         --- GANTI MODE BAHASA ---",
            "bahasa_sekarang": "Mode Bahasa sekarang: ",
            "b_indo": "Mode Bahasa: INDONESIA telah diaktifkan.",
            "b_jawa": "Mode Bahasa: JAWA telah diaktifkan.",
            "mode_hemat_judul": "             --- MODE HEMAT ---",
            "hemat_off": "Mode hemat off. Kembali ke limit normalmu",
            "limit_off": "Limit harianmu kembali jadi",
            "hemat_on": "Limit harian dibatasi, tetap hemat!",
            "limit_on": "Limit harianmu sekarang jadi",
            "atur_anggaran_judul": "      --- ATUR ANGGARAN & PENGATURAN ---",
            "anggaran_opsi1": "[1] Tambah Anggaran (Bulan Ini : ",
            "anggaran_opsi2": "[2] Limit Harian :     ",
            "anggaran_opsi3": "[3] Mulai Siklus Anggaran Baru (Wajib Bulanan!)",
            "anggaran_opsi4": "[4] Reset Data Pengeluaran (Hapus Semua Riwayat Pengeluaran)",
            "anggaran_opsi5": "[5] Kembali Ke Menu",
            "pilih_anggaran": "Pilih setting yang ingin diganti (1-5): ",
            "add_anggaran_judul": "          --- TAMBAH ANGGARAN ---",
            "tambah_budget_prompt": "Masukkan Jumlah    ",
            "add_anggaran": "Anggaran berhasil ditambahkan!",
            "total_add_anggaran": "Total Baru:   ",
            "minimum_spend": "Tidak masuk akal!",
            "anggaran_sukses": "Anggaran Bulanan sukses diubah.",
            "err_angka": "Error: hanya angka saja.",
            "limit_judul": "            --- ATUR LIMIT ---",
            "limit_sukses": "Limit Harian sukses diubah.",
            "warn_reset": "PERINGATAN! Aksi ini akan menghapus SEMUA riwayat pengeluaranmu",
            "konfirmasi_reset": "Ketik 'LANJUT' untuk melanjutkan reset (Enter untuk batal): ",
            "enter_anggaran": "Tekan Enter untuk kembali...",
            "siklus_baru_judul": "      --- SIKLUS ANGGARAN BARU ---",
            "warn_siklus_baru": "Aksi ini akan menimpa anggaran bulan ini dan mereset periode siklus. Riwayat lama TETAP TERSIMPAN.",
            "prompt_konfirmasi_siklus": "Ketik 'YA' untuk memulai siklus baru: ",
            "siklus_batal": "Operasi dibatalkan",
            "input_anggaran_dasar": "Masukkan ANGGARAN DASAR total bulan ini:",
            "siklus_sukses": "Siklus anggaran baru sukses diperbarui",
            "anggaran_dasar_baru": "Anggaran Dasar Baru",
            "tanggal_siklus_baru": "Tanggal Mulai Siklus",
            "input_tanggal_siklus": "Masukkan Tanggal Awal Siklus (DD/MM/YYYY)",
            "err_tanggal_siklus": "Error: Format tanggal harus DD/MM/YYYY.",
            "atur_budget_bulanan": "Masukkan Anggaran Bulanan Baru (sekarang",
            "atur_limit_harian": "Masukkan Limit Harian Baru (sekarang",
            "reset_success": "Data pengeluaran sudah bersih! SiRekoso siap demo dari nol." ,
            "gagal_reset": "Gagal menghapus data.",
            "reset_batal": "reset data dibatalkan.",
            "keluar": "Terimakasih, jangan lupa cek saldo terus, SiRekoso pamit. :D",
        }
    }
    
    settings = load_settings()
    mode = settings.get("MODE_BAHASA", "INDONESIA")
    
    return texts.get(mode, {}).get(key_id, f"[{key_id} NOT FOUND]")


def change_language(new_mode):
    settings = load_settings()
    settings["MODE_BAHASA"] = new_mode
    save_settings(settings)
    
    
# --- FUNGSI RESET DATA ---

def reset_all_data():
    
    from core.data_manager import save_records
    save_records([])
    
  
    settings = load_settings()
    settings["MODE_HEMAT_AKTIF"] = False
    save_settings(settings)
    
    return get_text("reset_success")