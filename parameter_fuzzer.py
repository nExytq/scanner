import requests
import json
import uuid
from config import INTERESTING_KEYS, FUZZ_VALUES_INT, FUZZ_VALUES_STR

class ParameterFuzzer:
    def __init__(self, target_url, json_payload):
        self.target_url = target_url
        self.payload = json_payload
        self.interesting_keys = INTERESTING_KEYS
        self.fuzz_values_int = FUZZ_VALUES_INT
        self.fuzz_values_str = FUZZ_VALUES_STR
        self.vulnerabilities_found = 0

    def _get_fuzz_values(self, value):
        fuzz_list = []
        if isinstance(value, int):
            fuzz_list.extend(self.fuzz_values_int)
            fuzz_list.append(value + 1)
            fuzz_list.append(value - 1)
        elif isinstance(value, str):
            if value.isdigit():
                val_int = int(value)
                fuzz_list.append(str(val_int + 1))
                fuzz_list.append(str(val_int - 1))
            fuzz_list.extend(self.fuzz_values_str)
            fuzz_list.append(str(uuid.uuid4()))
        return fuzz_list

    def run(self):
        print(f"\n[*] Starting Parameter Fuzzing on {self.target_url}...")
        
        # Обработка случая, если payload — это список
        working_payload = self.payload
        if isinstance(self.payload, list):
            if len(self.payload) > 0 and isinstance(self.payload[0], dict):
                print("[*] Detected JSON list. Fuzzing the first object in the list...")
                working_payload = self.payload[0]
            else:
                print("[-] Error: The fuzzer requires a JSON object (dictionary) to find parameters.")
                return

        try:
            base_res = requests.post(self.target_url, json=self.payload, timeout=10)
            base_len = len(base_res.content)
            base_code = base_res.status_code
            print(f"[*] Base response: Code {base_code}, Length {base_len}")
        except Exception as e:
            print(f"[!] Error making base request: {e}")
            return

        for key, value in working_payload.items():
            if any(ik in key.lower() for ik in self.interesting_keys):
                print(f"[*] Found interesting parameter: {key} = {value}")
                
                fuzz_values = self._get_fuzz_values(value)
                for fuzz_val in fuzz_values:
                    test_payload = working_payload.copy()
                    test_payload[key] = fuzz_val
                    
                    # Если оригинальный payload был списком, оборачиваем измененный объект обратно в список
                    final_payload = [test_payload] if isinstance(self.payload, list) else test_payload
                    
                    try:
                        res = requests.post(self.target_url, json=final_payload, timeout=10)
                        res_len = len(res.content)
                        res_code = res.status_code

                        if res_code == 200 or res_len == base_len:
                            print(f"[+] POTENTIAL IDOR: {key} -> {fuzz_val} | Code: {res_code}, Len: {res_len}")
                            self.vulnerabilities_found += 1
                    except Exception as e:
                        print(f"[-] Error fuzzing {key} with {fuzz_val}: {e}")

    def start(self):
        self.run()
        return self.vulnerabilities_found
