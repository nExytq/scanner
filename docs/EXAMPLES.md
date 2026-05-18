# Примеры использования PEN-TEST MULTI-TOOL

## Базовые примеры

### 1. Сканирование заголовков безопасности
```bash
python main.py https://example.com -m headers
```

### 2. Анализ JavaScript файлов
```bash
python main.py https://example.com -m js
```

### 3. Поиск XSS уязвимостей
```bash
python main.py https://example.com/login -m xss
```

### 4. Тестирование SQL injection
```bash
python main.py https://example.com/search?q=test -m sql
```

### 5. Parameter Fuzzing для IDOR
```bash
python main.py https://api.example.com/user -m fuzz -p "{\"user_id\": 123, \"role\": \"user\"}"
```

### 6. Полное сканирование
```bash
python main.py https://example.com -m all
```

## Продвинутые примеры

### Тестирование API endpoint с JSON payload
```bash
python main.py https://api.example.com/v1/users -m fuzz -p "{\"id\": 1, \"admin\": false, \"account_id\": 12345}"
```

### Тестирование с массивом объектов
```bash
python main.py https://api.example.com/bulk -m fuzz -p "[{\"user_id\": 1, \"role\": \"user\"}]"
```

## Интерактивный режим

Просто запустите без параметров:
```bash
python main.py
```

Выберите нужный режим из меню:
```
1. Header & Config Scanner
2. JS File Analyzer
3. XSS Form Scanner
4. SQL Injection Scanner
5. Parameter Fuzzer
6. Run ALL Scans
0. Exit
```

## Типичные сценарии использования

### Сценарий 1: Первичная разведка
```bash
# Шаг 1: Проверка заголовков и конфигов
python main.py https://target.com -m headers

# Шаг 2: Анализ JS файлов на утечки
python main.py https://target.com -m js
```

### Сценарий 2: Тестирование форм
```bash
# XSS тестирование
python main.py https://target.com/contact -m xss

# SQL injection тестирование
python main.py https://target.com/login -m sql
```

### Сценарий 3: API тестирование
```bash
# Fuzzing параметров для IDOR
python main.py https://api.target.com/user/profile -m fuzz -p "{\"user_id\": 100}"
```

### Сценарий 4: Комплексное тестирование
```bash
# Запуск всех сканеров сразу
python main.py https://target.com -m all -p "{\"id\": 1}"
```

## Интерпретация результатов

### Header Scanner
- `[+]` - Заголовок найден
- `[-]` - Заголовок отсутствует (потенциальная проблема)
- `[!] WARNING` - Найдена небезопасная конфигурация
- `[+] FOUND` - Обнаружен чувствительный файл

### JS Analyzer
- `[+] Found` - Обнаружена потенциальная утечка данных

### XSS Scanner
- `[+] POTENTIAL XSS` - Payload отразился в ответе

### SQL Scanner
- `[+] POTENTIAL SQL INJECTION` - Обнаружена SQL ошибка
- `[+] POTENTIAL TIME-BASED SQL INJECTION` - Задержка в ответе

### Parameter Fuzzer
- `[+] POTENTIAL IDOR` - Успешный доступ с измененным параметром

## Советы по использованию

1. **Всегда получайте разрешение** перед тестированием
2. **Начинайте с пассивных сканеров** (headers, js)
3. **Используйте throttling** для избежания блокировки
4. **Документируйте находки** для отчетов
5. **Проверяйте false positives** вручную

## Troubleshooting

### Ошибка подключения
```bash
# Проверьте доступность цели
curl -I https://target.com
```

### Timeout ошибки
- Увеличьте timeout в коде сканеров
- Проверьте сетевое подключение

### Слишком много false positives
- Настройте payloads в config.py
- Используйте более специфичные паттерны
