import sys
from core.data_manager import load_settings
from core.expenses import add_new_expense, handle_report_menu
from core.analysis import get_financial_summary, predict_spending, generate_report, toggle_hemat_mode, manage_settings
from core.helpers import get_current_date, format_rupiah, get_text, change_language

def display_menu(summary):
    
    menu_utama_text = get_text('menu_utama')
    pilih_menu_text = get_text('pilih_menu')
    
    
    print("\n \n \n" + "=" * 35)
    print(" SIREKOSO: Asisten Kos Gen Z")
    print("=" * 35)
    print(get_text('sisa_limit_monthly'),format_rupiah(summary['remaining_monthly_limit']))
    print(f"{get_text('sisa_limit_daily')}{format_rupiah(summary['remaining_daily_limit'])}")
    print("-" * 35)

    print(menu_utama_text)
    print(get_text('opsi_1'))
    print(get_text('opsi_2'))
    print(get_text('opsi_3'))
    print(get_text('opsi_4'))
    print(get_text('opsi_5'))
    print(get_text('opsi_6'))
    print(get_text('opsi_7'))
    print("-" * 35)
    
    choice = input(pilih_menu_text)
    return choice

def handle_choice(choice, today):
    settings = load_settings()
    
    if choice == '1':
        add_new_expense()
    
    elif choice == '2':
        handle_report_menu(today)

        
    elif choice == '3':
        predict_spending()

    elif choice == '4':
        print("\n \n \n==============================================")
        print(get_text("bahasa_judul"))
        print("==============================================")
        current_mode = settings.get("MODE_BAHASA")
        print(f"{get_text('bahasa_sekarang')} {current_mode}")
        
        print("[1] Indonesia (Standard)")
        print("[2] Jawa (Ngoko / Suroboyo)")
        
        mode_choice = input("Masukkan pilihan (1/2): ")
        
        if mode_choice == '1':
            change_language("INDONESIA")
            print(get_text('b_indo'))
            input(f"\n{get_text('enter_menu')}")

        elif mode_choice == '2':
            change_language("JAWA")
            print(get_text('b_jawa'))
            input(f"\n{get_text('enter_menu')}")

        else:
            print(get_text('pilihan_invalid'))
            input(f"\n{get_text('enter_menu')}")

    elif choice == '5':
        toggle_hemat_mode()

    elif choice == '6':
        manage_settings()
        
    elif choice == '7':
        print(f"\n{get_text('keluar')}")
        sys.exit()
        
    else:
        print(f"\n{get_text('pilihan_invalid')}")

def main():
    
    # Main Loop aplikasi
    while True:
        try:
            # Dapatkan summary keuangan terbaru untuk ditampilkan di banner
            summary = get_financial_summary()
            
            # Tampilkan menu dan ambil pilihan
            choice = display_menu(summary)
            
            # Tangani pilihan user
            handle_choice(choice, get_current_date())
            
        except Exception as e:
            # Penanganan error utama
            print(f"\n[CRITICAL ERROR] Terjadi kesalahan fatal: {e}")
            print("Aplikasi terpaksa dihentikan.")
            sys.exit(1)

if __name__ == "__main__":
    main()