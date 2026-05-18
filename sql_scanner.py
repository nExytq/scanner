import requests
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
from config import SQL_PAYLOADS, SQL_ERRORS

class SQLScanner:
    def __init__(self, target_url):
        self.target_url = target_url if target_url.startswith('http') else f'http://{target_url}'
        self.payloads = SQL_PAYLOADS
        self.error_patterns = SQL_ERRORS
        self.vulnerabilities_found = 0

    def test_url_params(self):
        """Test GET parameters for SQL injection"""
        print(f"\n[*] Testing URL parameters for SQL injection on {self.target_url}...")
        parsed = urlparse(self.target_url)
        params = parse_qs(parsed.query)
        
        if not params:
            print("[-] No URL parameters found to test")
            return
        
        for param_name in params.keys():
            print(f"[*] Testing parameter: {param_name}")
            for payload in self.payloads:
                test_params = params.copy()
                test_params[param_name] = [payload]
                
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(test_params, doseq=True)}"
                
                try:
                    response = requests.get(test_url, timeout=10)
                    
                    # Check for SQL errors in response
                    for error in self.error_patterns:
                        if error.lower() in response.text.lower():
                            print(f"[+] POTENTIAL SQL INJECTION: {param_name} with payload: {payload}")
                            print(f"    Error found: {error}")
                            self.vulnerabilities_found += 1
                            break
                    
                    # Check for time-based injection
                    if response.elapsed.total_seconds() > 5 and 'SLEEP' in payload.upper():
                        print(f"[+] POTENTIAL TIME-BASED SQL INJECTION: {param_name} with payload: {payload}")
                        self.vulnerabilities_found += 1
                        
                except Exception as e:
                    print(f"[-] Error testing {param_name}: {e}")

    def test_forms(self):
        """Test form inputs for SQL injection"""
        print(f"\n[*] Testing forms for SQL injection on {self.target_url}...")
        try:
            response = requests.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            
            if not forms:
                print("[-] No forms found to test")
                return
            
            print(f"[*] Found {len(forms)} forms")
            
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
                        target = action if action.startswith('http') else urljoin(self.target_url, action)
                        
                        if method == 'post':
                            res = requests.post(target, data=data, timeout=10)
                        else:
                            res = requests.get(target, params=data, timeout=10)
                        
                        # Check for SQL errors
                        for error in self.error_patterns:
                            if error.lower() in res.text.lower():
                                print(f"[+] POTENTIAL SQL INJECTION in form #{i+1} with payload: {payload}")
                                print(f"    Error found: {error}")
                                self.vulnerabilities_found += 1
                                break
                                
                    except Exception as e:
                        print(f"[-] Error testing form: {e}")
                        
        except Exception as e:
            print(f"[!] Error fetching forms: {e}")

    def run(self):
        self.test_url_params()
        self.test_forms()
        return self.vulnerabilities_found
