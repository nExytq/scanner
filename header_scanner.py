import requests

class HeaderScanner:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith('http') else f'http://{target_url}'
        self.security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection",
            "Referrer-Policy"
        ]
        self.sensitive_files = [
            ".env",
            ".git/config",
            "docker-compose.yml",
            "phpinfo.php",
            "config.php",
            "web.config",
            ".htaccess"
        ]

    def scan_headers(self):
        print(f"\n[*] Scanning headers for {self.target_url}...")
        try:
            response = requests.get(self.target_url, timeout=10)
            headers = response.headers

            print("\n--- Security Headers ---")
            for header in self.security_headers:
                if header in headers:
                    print(f"[+] {header}: Found")
                else:
                    print(f"[-] {header}: Missing")

            # CORS check
            cors = headers.get("Access-Control-Allow-Origin")
            if cors == "*":
                print(f"[!] WARNING: CORS policy is open (Access-Control-Allow-Origin: *)")
            elif cors:
                print(f"[*] CORS policy: {cors}")
            else:
                print("[-] CORS header not found")

        except Exception as e:
            print(f"[!] Header scan error: {e}")

    def scan_configs(self):
        print(f"\n[*] Searching for sensitive files on {self.target_url}...")
        for file in self.sensitive_files:
            url = f"{self.target_url.rstrip('/')}/{file}"
            try:
                response = requests.get(url, timeout=5, allow_redirects=False)
                if response.status_code == 200:
                    print(f"[+] FOUND: {url} (Status: 200)")
                else:
                    pass # Skip non-existent files
            except Exception as e:
                print(f"[-] Error checking {url}: {e}")

    def run(self):
        self.scan_headers()
        self.scan_configs()
