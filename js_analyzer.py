import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class JSAnalyzer:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith('http') else f'http://{target_url}'
        # Регулярные выражения для путей API и ключей
        self.patterns = {
            'API Endpoint': r'\/api\/v[0-9]\/[\w\/-]+',
            'Firebase Key': r'AIza[0-9A-Za-z-_]{35}',
            'AWS Access Key': r'AKIA[0-9A-Z]{16}',
            'Generic Secret': r'(?i)(secret|key|token|auth|password)\s*[:=]\s*["\']([a-zA-Z0-9_\-]{16,})["\']'
        }

    def analyze(self):
        print(f"\n[*] Analyzing JS files for {self.target_url}...")
        try:
            response = requests.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', src=True)
            
            js_files = [urljoin(self.target_url, s['src']) for s in scripts]
            print(f"[*] Found {len(js_files)} JS files.")

            for js_url in js_files:
                try:
                    js_res = requests.get(js_url, timeout=10)
                    content = js_res.text
                    
                    for name, pattern in self.patterns.items():
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # match может быть кортежем если есть группы в regex
                            val = match[1] if isinstance(match, tuple) else match
                            print(f"[+] Found {name} in {js_url}: {val}")
                except Exception as e:
                    print(f"[-] Could not read {js_url}: {e}")

        except Exception as e:
            print(f"[!] Error in JS analysis: {e}")

    def run(self):
        self.analyze()
