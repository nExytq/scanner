import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import JS_PATTERNS

class JSAnalyzer:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith('http') else f'http://{target_url}'
        self.patterns = JS_PATTERNS

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
