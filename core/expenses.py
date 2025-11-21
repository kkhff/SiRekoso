import datetime
import time
from core.analysis import generate_report
from core.data_manager import load_records, save_records
from core.helpers import validate_number, get_current_date, format_rupiah, get_text, get_localized_message

def add_new_expense():
    print("\n \n \n==============================================")
    print(get_text('expense_judul'))
    print("==============================================")
    
    # 1. Input Tanggal
    today = get_current_date()
    while True:
        print(get_text('Default_tanggal'))
        input_tanggal = input(f"{get_text('input_tanggal')} {today}): ")
        if not input_tanggal:
            tanggal = today
            break
        if len(input_tanggal) == 10 and input_tanggal[2] == '/' and input_tanggal[5] == '/':
            tanggal = input_tanggal
            break
        else:
            print(get_text('err_input_tanggal'))

    print(get_text('enter_batal'))
    # 2. Input Deskripsi
    deskripsi = input(get_text('deskripsi'))
    if not deskripsi.strip():
        print(get_text('err_deskripsi'))
        input(f"\n{get_text('enter_menu')}")
        return 

    # 3. Input harga (Menggunakan helper untuk validasi angka)
    harga = validate_number(get_text('harga'))
    
    if harga is None or harga <= 100:
        print(get_text('err_harga'))
        input(f"\n{get_text('enter_menu')}")
        return

    # 4. Buat ID Unik
    expense_id = "e" + str(int(time.time())) 

    # 5. Buat Objek Transaksi Baru
    new_record = {
        "id": expense_id,
        "tanggal": tanggal,
        "deskripsi": deskripsi,
        "harga": harga
    }

    # 6. Load data lama, tambahkan data baru, dan simpan
    records = load_records()
    records.append(new_record)
    save_records(records)
    
    # 7. Konfirmasi ke User
    konfirmasi_teks = f"\nPengeluaran '{deskripsi}' senilai {format_rupiah(harga)} {get_text('expense_saved')}"
    print(konfirmasi_teks)
    input(f"\n{get_text('enter_menu')}")

def delete_expense(expense_id):
    records = load_records()
    
    # Filter records, hapus yang ID-nya cocok
    new_records = [r for r in records if r['id'] != expense_id]
    
    if len(new_records) < len(records):
        save_records(new_records)
        print(f"\n{get_text('hapus_sukses')}")
        input(f"\n{get_text('enter_laporan_daily')}")
        return True
    else:
        print(f"\n{get_text('id_not_found')}")
        input(f"\n{get_text('enter_laporan_daily')}")
        return False

def edit_expense(expense_id, old_record):
    print(f"\n--- EDIT TRANSAKSI: {old_record['deskripsi']} ---")
    print(f"\n{get_text('edit_msg')}")
    
    new_deskripsi = input(f"{get_text('new_deskripsi')}{old_record['deskripsi']}): ")
    new_harga = validate_number(f"{get_text('new_harga')}{format_rupiah(old_record['harga'])}): ")
    if not new_deskripsi and new_harga is None:
        print(get_text('cancel_edit'))
        input(f"\n{get_text('enter_laporan_daily')}")
        return
    if not new_deskripsi.strip() :
        new_deskripsi = old_record['deskripsi']
    if new_harga is None :
        new_harga = old_record['harga']
    if new_harga <= 100:
        print(get_text('minimum_spend'))
        return  
    


    records = load_records()
    found = False
    
    # Cari dan update record
    for i, record in enumerate(records):
        if record['id'] == expense_id:
            records[i]['deskripsi'] = new_deskripsi
            records[i]['harga'] = new_harga
            found = True
            break
            
    if found:
        save_records(records)
        print(f"\n{get_text('edit_sukses')}")
        input(f"\n{get_text('enter_laporan_daily')}")
    else:
        print(f"\n{get_text('id_not_found')}")
        input(f"\n{get_text('enter_laporan_daily')}")

def view_daily_expenses(target_date):
    while True:
        records = load_records()
        daily_records = [r for r in records if r['tanggal'] == target_date]
        if not daily_records:
            print("\n \n==============================================")
            print(get_text("daily_expense_judul"))
            print("==============================================")
            print(f"\nTanggal {target_date}: {get_text('no_expense')}")
            input(get_text('enter_laporan'))
            return 0

        total_harian = 0
    
        print("\n \n==============================================")
        print(get_text("daily_expense_judul"))
        print("==============================================")

        for i, record in enumerate(daily_records):
            harga_transaksi = record.get('harga')

            if harga_transaksi is None:
                harga_transaksi = 0

            print(f"[{i+1}] {record['deskripsi']:<30} | {format_rupiah(harga_transaksi):>15}")
            total_harian += harga_transaksi

        print("-" * 50)
        print(f"{get_text('total_harian')}{format_rupiah(total_harian):>18}")
        print("-" * 50)
    
        try:
            # Ambil input aksi
            print(get_text('aksi_msg'))
            action = input(f"\nPilih aksi: ") 

            if not action.strip() :
                break # Kembali ke sub-menu laporan

            elif action in ['1', '2']:
                
                idx_input = input("input nomor pengeluaran: ")
                idx = int(idx_input) - 1 # Konversi ke index list (0-based)
                
                if 0 <= idx < len(daily_records):
                    selected_record = daily_records[idx]
                    expense_id = selected_record['id']

                    if action == '1':
                        edit_expense(expense_id, selected_record)
                        continue
                        
                    elif action == '2':
                        print(get_text('hapus_msg'))
                        confirm_input = input(get_text('hapus_input'))
                        if confirm_input.upper() != "Y":
                            continue
                        if delete_expense(expense_id):
                            # Jika sukses hapus, kita keluar dan reload menu
                            continue
                            
                else:
                    print(get_text('pilihan_invalid'))
                    
            else:
                print(get_text('pilihan_invalid'))

        except ValueError:
            print(get_text('pilihan_invalid'))
            
        except Exception as e:
            print(f"{get_text('err_daily')}{e}")
            

    return total_harian

def view_monthly_details():
    records = load_records()

    DATE_FORMAT = "%d/%m/%Y"

    try:
        today_dt = datetime.datetime.strptime(get_current_date(), DATE_FORMAT)
    except ValueError:
        today_dt = datetime.datetime.now()
        

    start_date = today_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    next_month = today_dt.replace(day=28) + datetime.timedelta(days=4)
    end_date = next_month.replace(day=1) - datetime.timedelta(seconds=1)

    
    # --- 2. Filter Records ---
    filtered_records = []
    for r in records:
        try:
            record_date = datetime.datetime.strptime(r['tanggal'], DATE_FORMAT)
            if start_date <= record_date <= end_date:
                filtered_records.append(r)
        except ValueError:
            continue
    
    if not filtered_records:
        print("\n==============================================")
        print(get_text("monthly_expense_judul"))
        print("==============================================")
        print(get_text('no_expense'))
        input(f"\n{get_text('enter_laporan')}")
        return
    
    sorted_records = sorted(
        filtered_records, 
        key=lambda r: datetime.datetime.strptime(r['tanggal'], "%d/%m/%Y"), 
        reverse=True # Tampilkan tanggal terbaru dulu
    )
    
    total_bulan_ini = sum(r['harga'] for r in filtered_records)
    
    print("\n==============================================")
    print(get_text("monthly_expense_judul"))
    print("==============================================")
    print(f"{get_text('total_bulanan')}{format_rupiah(total_bulan_ini)}")
    print("-" * 50)
    
    current_date = ""
    for record in sorted_records:
        if record['tanggal'] != current_date:
            current_date = record['tanggal']
            print(f"\n--- TANGGAL: {current_date} ---")
            
        # Tampilkan detail transaksi
        print(f"  > {record['deskripsi']:<35} {format_rupiah(record['harga']):>15}")

    print("-" * 50)
    input(f"\n{get_text('enter_laporan')}")


def handle_report_menu(today):
    while True:
        print("\n==============================================")
        print(get_text('laporan_judul'))
        print("==============================================")
        generate_report()
        print(get_text('laporan_opsi1'))
        print(get_text('laporan_opsi2'))
        print(get_text('laporan_opsi3'))

        pilihan = input(get_text('pilih_laporan'))

        if pilihan == '1':
            view_daily_expenses(today) 
        elif pilihan == '2':
            view_monthly_details() 
        elif pilihan == '3':
            return
        else:
            print(get_text('pilihan_invalid'))

