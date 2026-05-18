import requests
import logging
from config import SECURITY_HEADERS, SENSITIVE_FILES

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HeaderScanner:
    def __init__(self, target_url):
        self.target_url = self._ensure_http_prefix(target_url)
        self.security_headers = SECURITY_HEADERS
        self.sensitive_files = SENSITIVE_FILES

    def _ensure_http_prefix(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            return f'http://{url}'
        return url
    
    def scan_headers(self):
        logging.info(f"[*] Scanning headers for {self.target_url}...")
        try:
            response = requests.get(self.target_url, timeout=10)
            headers = response.headers

            logging.info("\n--- Security Headers ---")
            for header in self.security_headers:
                if header in headers:
                    header_value = headers[header]
                    logging.info(f"[+] {header}: Found - {header_value}")
                    # Basic analysis for some headers
                    if header == "Strict-Transport-Security" and "max-age=0" in header_value:
                        logging.warning(f"[!] WARNING: HSTS max-age is 0, effectively disabling it.")
                    if header == "X-Frame-Options" and header_value.lower() not in ["deny", "sameorigin"]:
                        logging.warning(f"[!] WARNING: X-Frame-Options is '{header_value}', consider 'DENY' or 'SAMEORIGIN'.")
                    if header == "Content-Security-Policy" or header == "Content-Security-Policy-Report-Only":
                        if "unsafe-inline" in header_value or "unsafe-eval" in header_value or "'*'" in header_value:
                            logging.warning(f"[!] WARNING: CSP contains potentially insecure directives like 'unsafe-inline', 'unsafe-eval', or wildcard '*'.")
                else:
                    logging.warning(f"[-] {header}: Missing")

            # CORS check
            cors = headers.get("Access-Control-Allow-Origin")
            if cors == "*":
                logging.warning(f"[!] WARNING: CORS policy is open (Access-Control-Allow-Origin: *)")
            elif cors:
                logging.info(f"[*] CORS policy: {cors}")
            else:
                logging.warning("[-] CORS header not found")

        except requests.exceptions.RequestException as e:
            logging.error(f"[!] Header scan error for {self.target_url}: {e}")
        except Exception as e:
            logging.error(f"[!] An unexpected error occurred during header scan: {e}")

    def scan_configs(self):
        logging.info(f"[*] Searching for sensitive files on {self.target_url}...")
        for file in self.sensitive_files:
            url = f"{self.target_url.rstrip('/')}/{file}"
            try:
                response = requests.get(url, timeout=5, allow_redirects=False)
                if response.status_code == 200:
                    logging.info(f"[+] FOUND: {url} (Status: {response.status_code})")
                elif response.status_code in [401, 403]:
                    logging.warning(f"[!] POSSIBLY FOUND (Restricted): {url} (Status: {response.status_code})")
                elif 300 <= response.status_code < 400:
                    logging.info(f"[*] Redirect for {url} (Status: {response.status_code}) -> {response.headers.get('Location', 'N/A')}")
            except requests.exceptions.RequestException as e:
                logging.error(f"[-] Error checking {url}: {e}")
            except Exception as e:
                logging.error(f"[-] An unexpected error occurred checking {url}: {e}")

    def run(self):
        self.scan_headers()
        self.scan_configs()
