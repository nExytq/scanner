import requests
from bs4 import BeautifulSoup
from config import XSS_PAYLOADS

class XSSScanner:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith('http') else f'http://{target_url}'
        self.payloads = XSS_PAYLOADS
        self.vulnerabilities_found = 0

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
                    action = form.get('action', self.target_url)
                    target = action if action.startswith('http') else f"{self.target_url.rstrip('/')}/{action.lstrip('/')}"
                    
                    if method == 'post':
                        res = requests.post(target, data=data, timeout=10)
                    else:
                        res = requests.get(target, params=data, timeout=10)
                    
                    if payload in res.text:
                        print(f"[+] POTENTIAL XSS: Payload {payload} reflected in response!")
                        self.vulnerabilities_found += 1
                except Exception as e:
                    print(f"[-] Error sending payload: {e}")

    def run(self):
        self.scan()
        return self.vulnerabilities_found
