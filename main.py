import argparse
import json
import os
from header_scanner import HeaderScanner
from parameter_fuzzer import ParameterFuzzer
from xss_scanner import XSSScanner
from js_analyzer import JSAnalyzer
from sql_scanner import SQLScanner

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
    ==================================================
    🛡️  PEN-TEST MULTI-TOOL v2.2 (Interactive Mode)
    ==================================================
    1. 🔍 Header & Config Scanner
    2. 📜 JS File Analyzer (API & Keys)
    3. 💉 XSS Form Scanner
    4. 💊 SQL Injection Scanner
    5. ⚡ Parameter Fuzzer (IDOR/Mass Assignment)
    6. 🚀 Run ALL Scans
    0. ❌ Exit
    ==================================================
    """)

def print_summary(results):
    print("\n" + "="*50)
    print("📊 SCAN SUMMARY")
    print("="*50)
    
    if 'headers' in results:
        status = "✅" if results['headers'] == 0 else "❎"
        print(f"{status} Header & Config Scanner: {results['headers']} issues found")
    
    if 'js' in results:
        status = "✅" if results['js'] == 0 else "❎"
        print(f"{status} JS File Analyzer: {results['js']} findings")
    
    if 'xss' in results:
        status = "✅" if results['xss'] == 0 else "❎"
        print(f"{status} XSS Scanner: {results['xss']} vulnerabilities found")
    
    if 'sql' in results:
        status = "✅" if results['sql'] == 0 else "❎"
        print(f"{status} SQL Injection Scanner: {results['sql']} vulnerabilities found")
    
    if 'fuzz' in results:
        status = "✅" if results['fuzz'] == 0 else "❎"
        print(f"{status} Parameter Fuzzer: {results['fuzz']} potential issues found")
    
    print("="*50)
    
    total_issues = sum(results.values())
    if total_issues == 0:
        print("✅ No issues detected!")
    else:
        print(f"⚠️  Total issues detected: {total_issues}")
    print("="*50)

def run_scanner(mode, url, payload=None):
    print(f"\n[!] Target: {url}")
    print(f"[!] Mode: {mode}")
    print("--------------------------------------------------")
    
    results = {}

    if mode in ['headers', 'all']:
        result = HeaderScanner(url).run()
        results['headers'] = result

    if mode in ['js', 'all']:
        result = JSAnalyzer(url).run()
        results['js'] = result

    if mode in ['xss', 'all']:
        result = XSSScanner(url).run()
        results['xss'] = result
    
    if mode in ['sql', 'all']:
        result = SQLScanner(url).run()
        results['sql'] = result

    if mode in ['fuzz', 'all']:
        if payload:
            try:
                payload_dict = json.loads(payload)
                result = ParameterFuzzer(url, payload_dict).start()
                results['fuzz'] = result
            except json.JSONDecodeError:
                print("[!] Error: Invalid JSON provided in payload")
        else:
            print("\n[-] Skipping Parameter Fuzzer: No JSON payload provided.")

    print("\n--------------------------------------------------")
    
    # Показываем сводку только если был запущен массовый скан или несколько сканеров
    if mode == 'all' or len(results) > 1:
        print_summary(results)
    
    print("[!] Operation completed.")

def main():
    parser = argparse.ArgumentParser(description="Multi-Tool for Legal Penetration Testing")
    parser.add_argument("url", nargs='?', help="Target URL")
    parser.add_argument("-m", "--mode", choices=['headers', 'fuzz', 'xss', 'js', 'sql', 'all'], help="Scan mode")
    parser.add_argument("-p", "--payload", help="JSON payload for fuzzer")

    args = parser.parse_args()

    # Если аргументы переданы, работаем в режиме CLI
    if args.url and args.mode:
        run_scanner(args.mode, args.url, args.payload)
        return

    # Иначе — запускаем Интерактивное Меню
    while True:
        clear_screen()
        print_banner()
        
        choice = input("👉 Select an option: ").strip()

        if choice == '0':
            print("Goodbye! 👋")
            break
        
        if choice not in ['1', '2', '3', '4', '5', '6']:
            input("❌ Invalid option! Press Enter to try again...")
            continue

        # Маппинг выбора в режимы
        mode_map = {
            '1': 'headers',
            '2': 'js',
            '3': 'xss',
            '4': 'sql',
            '5': 'fuzz',
            '6': 'all'
        }
        selected_mode = mode_map[choice]

        # Запрашиваем URL
        target_url = input("🌐 Enter target URL (e.g., http://example.com): ").strip()
        if not target_url:
            input("❌ URL cannot be empty! Press Enter to try again...")
            continue

        # Если выбран фаззинг, запрашиваем JSON
        payload = None
        if selected_mode == 'fuzz' or selected_mode == 'all':
            print("\n[?] Payload is required for Fuzzing. If you don't have one, just press Enter.")
            payload = input("📦 Enter JSON payload: ").strip()

        run_scanner(selected_mode, target_url, payload)
        
        input("\n✅ Done! Press Enter to return to the main menu...")

if __name__ == '__main__':
    main()
