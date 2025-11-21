import datetime
import math
from core.data_manager import load_settings, save_settings, load_records, reset_records
from core.helpers import format_rupiah, get_current_date, get_localized_message, get_text

# --- HELPER UTAMA: MENGHITUNG SEMUA SUMBER DAYA ---

def get_financial_summary():

    settings = load_settings()
    records = load_records()
    
    # 1. Kalkulasi Tanggal
    DATE_FORMAT = "%d/%m/%Y"
    try:
        today = datetime.datetime.strptime(get_current_date(), DATE_FORMAT)
        start_date = datetime.datetime.strptime(settings['TANGGAL_AWAL_KOS'], DATE_FORMAT)
        end_date = start_date + datetime.timedelta(days=29)  
              
        if today < start_date:
            days_passed = 0
        elif today > end_date:
            days_passed = 30 # Siklus selesai, hitung 30 hari penuh
        else:
            days_passed = (today - start_date).days + 1
        
        days_remaining = (end_date - today).days 
        if days_remaining < 0: days_remaining = 0

        total_period_days = 30
            
    except ValueError:
        days_passed = 1
        days_remaining = 30
        total_period_days = 30
    
    current_cycle_records = []
    for r in records:
        try:
            record_date = datetime.datetime.strptime(r['tanggal'], DATE_FORMAT)
            if start_date <= record_date <= end_date:
                current_cycle_records.append(r)
        except:
            continue

    total_spent = sum(
        r.get('harga', 0) for r in current_cycle_records 
        if isinstance(r.get('harga', 0), (int, float))
    )
    initial_budget = settings['ANGGARAN_BULANAN']
    remaining_balance = initial_budget - total_spent
    
    # 3. Kalkulasi Limit Harian Efektif

    today_date_str = get_current_date()

    daily_limit = settings['LIMIT_HARIAN_DEFAULT']
    
    if settings['MODE_HEMAT_AKTIF']:
        reduction_percent = settings['PERSEN_PENGURANGAN_HEMAT']
        daily_limit = daily_limit * (1 - reduction_percent)
    today_spent = sum(
        r.get('harga', 0) for r in current_cycle_records
        if r['tanggal'] == today_date_str and isinstance(r.get('harga', 0), (int, float))
    )
    remaining_daily_limit = daily_limit - today_spent
    if remaining_daily_limit < 0:
        remaining_daily_limit = 0


    monthly_limit = daily_limit * total_period_days
    
    remaining_monthly_limit =  monthly_limit - total_spent
    


    # 4. Kalkulasi Rata-rata
    avg_spent = total_spent / days_passed if days_passed > 0 else 0
    
    return {
        'total_spent': total_spent,
        'remaining_balance': remaining_balance,
        'days_passed': days_passed,
        'remaining_monthly_limit': remaining_monthly_limit,
        'days_remaining': days_remaining,
        'total_period_days': total_period_days,
        'daily_limit': daily_limit,
        'monthly_limit': monthly_limit,
        'avg_spent': avg_spent,
        'today': today,
        'today_spent': today_spent, 
        'remaining_daily_limit': remaining_daily_limit
    }


# --- FUNGSI MENU [6]: MODE HEMAT ---

def toggle_hemat_mode():
    settings = load_settings()
    is_active = settings['MODE_HEMAT_AKTIF']
    
    summary = get_financial_summary()
    daily_limit_normal = settings['LIMIT_HARIAN_DEFAULT']
    reduction_percent = settings['PERSEN_PENGURANGAN_HEMAT']
    
    
    if is_active:
        settings['MODE_HEMAT_AKTIF'] = False
        save_settings(settings)
        
        new_limit = daily_limit_normal

        
        print("\n \n \n==============================================")
        print(get_text("mode_hemat_judul"))
        print("==============================================")
        print("MODE HEMAT: MATI.")
        print(get_text('hemat_off'))
        print(f"{get_text('limit_off')} **{format_rupiah(new_limit)}**.")
        input(get_text('enter_menu'))

    else:
        # Aktifkan Mode Hemat
        settings['MODE_HEMAT_AKTIF'] = True
        save_settings(settings)
        
        new_limit = daily_limit_normal * (1 - reduction_percent)

        
        print("\n \n \n==============================================")
        print(get_text("mode_hemat_judul"))
        print("==============================================")
        print("MODE HEMAT: AKTIF.")
        print(get_text('hemat_on'))
        print(f"{get_text('limit_on')} **{format_rupiah(new_limit)}** ({reduction_percent*100:.0f}%).")
        input(get_text('enter_menu'))


# --- FUNGSI MENU [4]: PREDIKSI DOMPET NANGIS ---

def predict_spending():
    summary = get_financial_summary()
    
    total_spent = summary['total_spent']
    remaining_balance = summary['remaining_balance']
    daily_limit = summary['daily_limit']
    avg_spent = summary['avg_spent']
    days_remaining = summary['days_remaining']
    monthly_limit = summary['monthly_limit']
    

    
    print("\n \n \n==============================================")
    print(get_text("prediksi_judul"))
    print("==============================================")
    print(f"{get_text('sisa_hari_siklus')}{summary['days_remaining']} Hari")
    print(f"{get_text('limit_monthly_aktif')}{format_rupiah(monthly_limit)}")
    print(f"{get_text('limit_daily_aktif')}{format_rupiah(daily_limit)}")
    print(f"{get_text('sisa_saldo')}{format_rupiah(remaining_balance)}")
    print(f"{get_text('avg_pengeluaran')}{format_rupiah(avg_spent)}")

    if remaining_balance <= 0:
        print("\nSTATUSMU: OVER LIMIT")
        print(f"[!] NOTIF: {get_localized_message('OVER_LIMIT')}")
        print(f"PREDIKSI OVERLIMIT: {get_text('prediksi_OVER_LIMIT')}")
        input(f"\n{get_text('enter_menu')}")
        return

    predicted_days_left = remaining_balance / avg_spent if avg_spent > 0 else 999
    
    predicted_date = summary['today'] + datetime.timedelta(days=predicted_days_left)
    predicted_date_str = predicted_date.strftime("%d/%m/%Y")
    
    
    # Tentukan Status
    if predicted_days_left >= days_remaining:

        print("\nSTATUSMU: AMAN SENTOSA")
        print(f"[!] NOTIF: {get_localized_message('AMAN_SENTOSA')}")
        print(f"PREDIKSI: Aman! {get_text('prediksi_aman')} {predicted_date_str}.")
        input(f"\n{get_text('enter_menu')}")

    elif predicted_days_left <= (days_remaining / 2): 
        print("\nSTATUSMU: WASPADA") 
        print(f"[!] NOTIF: {get_localized_message('WASPADA')}") # Panggil kunci WASPADAI
        print(f"PREDIKSI KRITIS: {get_text('prediksi_kritis')} {predicted_date_str}!")
        input(f"\n{get_text('enter_menu')}")

    else:
        print("\nSTATUSMU: NANGIS")
        print(f"[!] NOTIF: {get_localized_message('NANGIS')}")
        print(f"PREDIKSI NANGIS: {get_text('prediksi_nangis')} {predicted_date_str}!")
        input(f"\n{get_text('enter_menu')}")


def generate_report(timeframe='monthly'):

    summary = get_financial_summary()
    records = load_records()
    
    daily_spending = {}
    for record in records:
        date_str = record.get('tanggal')
        amount = record.get('harga')
        if amount is None or not isinstance(amount, (int, float)):
            amount = 0
        daily_spending[date_str] = daily_spending.get(date_str, 0) + amount

    print(f"{get_text('total_bulanan')}{format_rupiah(summary['total_spent'])}")
    print(f"{get_text('sisa_saldo')}{format_rupiah(summary['remaining_balance'])}")
    print(f"{get_text('avg_pengeluaran')}{format_rupiah(summary['avg_spent'])}")
    print("-" * 50)




# --- FUNGSI MENU [7]: ATUR ANGGARAN KOS ---

def manage_settings():
    settings = load_settings()

    while True:
        print("\n\n==============================================")
        print(get_text("atur_anggaran_judul"))
        print("==============================================")
        
        # --- TAMPILAN MENU FINAL ---
        print(f"{get_text('anggaran_opsi1')}{format_rupiah(settings['ANGGARAN_BULANAN'])})")
        print(f"{get_text('anggaran_opsi2')}{format_rupiah(settings['LIMIT_HARIAN_DEFAULT'])}")
        print(get_text('anggaran_opsi3')) 
        print(get_text('anggaran_opsi4')) 
        print(get_text('anggaran_opsi5')) 
        
        pilihan = input(f"\n{get_text('pilih_anggaran')}")
        
        if pilihan == '1':
            print("\n==============================================")
            print(get_text('add_anggaran_judul'))
            print("==============================================")
            # --- OPSI 1: TAMBAH ANGGARAN MID-CYCLE --- 
            new_budget_input = input(f"\n{get_text('tambah_budget_prompt')} (Anggaran Sekarang: {format_rupiah(settings['ANGGARAN_BULANAN'])}): ")
            
            try:
                added_amount = int(new_budget_input)
                
                if added_amount <= 0:
                    print(get_text("minimum_spend"))
                    input(get_text('enter_anggaran'))
                    continue
                
                # Logika Penjumlahan
                old_budget = settings['ANGGARAN_BULANAN']
                settings['ANGGARAN_BULANAN'] += added_amount

                save_settings(settings)
                
                print(get_text('add_anggaran'))
                print(f"Anggaran Awal: {format_rupiah(old_budget)}")
                print(f"Ditambah:      {format_rupiah(added_amount)}")
                print(get_text('total_add_anggaran'),format_rupiah(settings['ANGGARAN_BULANAN']))
                input(get_text('enter_anggaran'))
                
            except ValueError:
                print(get_text('err_angka'))
                input(get_text('enter_anggaran'))
                
        elif pilihan == '2':
            # --- OPSI 2: ATUR LIMIT HARIAN ---
            print("\n==============================================")
            print(get_text('limit_judul'))
            print("==============================================")
            new_limit = input(f"\n{get_text('atur_limit_harian')},{format_rupiah(settings['LIMIT_HARIAN_DEFAULT'])}): ")
            try:
                settings['LIMIT_HARIAN_DEFAULT'] = int(new_limit)
                if settings['LIMIT_HARIAN_DEFAULT'] <= 100:
                    print(get_text("minimum_spend"))
                    input(get_text('enter_anggaran'))
                    continue 
                save_settings(settings)
                print(get_text('limit_sukses'))
                input(get_text('enter_anggaran'))
            except ValueError:
                print(get_text('err_angka'))
                input(get_text('enter_anggaran'))


        elif pilihan == '3':
            DATE_FORMAT = "%d/%m/%Y"
            # --- OPSI 3: MULAI SIKLUS ANGGARAN BARU (LOGIKA DARI OPSI 5 LAMA) ---
            print("\n==============================================")
            print(get_text('siklus_baru_judul'))
            print("==============================================")
            
            # Konfirmasi Aksi
            print(f"\n{get_text('warn_siklus_baru')}")
            konfirmasi_siklus = input(f"\n{get_text('prompt_konfirmasi_siklus')}")
            
            if konfirmasi_siklus.upper() != 'YA':
                print(get_text('siklus_batal'))
                input(get_text('enter_anggaran'))
                continue

            new_start_date = None
            while True:
                # Gunakan kunci teks baru untuk prompt tanggal
                tanggal_prompt = f"{get_text('input_tanggal_siklus')} (Enter=Hari Ini): "
                tanggal_input = input(tanggal_prompt)
                
                if not tanggal_input:
                    # Default: Gunakan tanggal hari ini
                    new_start_date = get_current_date()
                    break
                
                try:
                    # Validasi format tanggal manual
                    datetime.datetime.strptime(tanggal_input, DATE_FORMAT)
                    new_start_date = tanggal_input
                    break
                except ValueError:
                    # Gunakan kunci teks error baru
                    print(get_text('err_tanggal_siklus'))
                    continue

            # Input Anggaran Dasar
            new_budget_base_input = input(get_text('input_anggaran_dasar'))
            
            try:
                new_budget_base = int(new_budget_base_input)
                
                if new_budget_base <= 100:
                    print(get_text("minimum_spend"))
                    input(get_text('enter_anggaran'))
                    continue

                # 1. Reset Anggaran Bulanan ke nilai Dasar (Menimpa)
                settings['ANGGARAN_BULANAN'] = new_budget_base 
                
                # 2. Reset Tanggal Awal Kos ke hari ini
                settings['TANGGAL_AWAL_KOS'] = new_start_date 
                
                save_settings(settings)
                
                print(f"\n{get_text('siklus_sukses')}")
                print(f"{get_text('anggaran_dasar_baru')}: {format_rupiah(new_budget_base)}")
                print(f"{get_text('tanggal_siklus_baru')}: {settings['TANGGAL_AWAL_KOS']}")
                input(get_text('enter_anggaran'))

            except ValueError:
                print(get_text('err_angka'))
                input(get_text('enter_anggaran'))

        elif pilihan == '4':
            # --- OPSI 4: RESET DATA PENGELUARAN (LOGIKA DARI OPSI 3 LAMA) ---
            print(f"\n {get_text('warn_reset')}")
            konfirmasi = input(get_text('konfirmasi_reset'))
            
            if konfirmasi.upper() == 'LANJUT':
                if reset_records(): 
                    print(f"\n{get_text('reset_success')}")
                    input(get_text('enter_anggaran'))
                else:
                    print(f"\n{get_text('gagal_reset')}")
                    input(get_text('enter_anggaran'))
            else:
                print(get_text('reset_batal'))
                input(get_text('enter_anggaran'))

        elif pilihan == '5':
            # --- OPSI 5: KEMBALI ---
            break
            
        else:
            print(get_text('pilihan_invalid'))
            input(get_text('enter_anggaran'))