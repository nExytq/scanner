# 🚀 Быстрый старт

## Установка

```bash
cd E:\projects\scanner
pip install -r requirements.txt
```

## Использование

### Интерактивный режим (рекомендуется для начинающих)
```bash
python main.py
```

### CLI режим

**Проверка заголовков безопасности:**
```bash
python main.py https://example.com -m headers
```

**Анализ JavaScript файлов:**
```bash
python main.py https://example.com -m js
```

**Поиск XSS:**
```bash
python main.py https://example.com -m xss
```

**Тестирование SQL injection:**
```bash
python main.py https://example.com -m sql
```

**Parameter Fuzzing:**
```bash
python main.py https://api.example.com/user -m fuzz -p "{\"user_id\": 123}"
```

**Запустить все сканеры:**
```bash
python main.py https://example.com -m all
```

## Структура проекта

```
scanner/
├── main.py                 # Главный файл
├── config.py              # Конфигурация (payloads, patterns)
├── header_scanner.py      # Сканер заголовков
├── js_analyzer.py         # Анализатор JS
├── xss_scanner.py         # XSS сканер
├── sql_scanner.py         # SQL injection сканер
├── parameter_fuzzer.py    # Fuzzer параметров
├── requirements.txt       # Зависимости
├── README.md             # Документация
├── EXAMPLES.md           # Примеры
├── SECURITY_GUIDE.md     # Руководство по безопасности
├── CHANGELOG.md          # История изменений
└── UPDATE_SUMMARY.md     # Сводка обновлений
```

## Настройка

Все настройки находятся в `config.py`:

- `SECURITY_HEADERS` - проверяемые заголовки
- `SENSITIVE_FILES` - файлы для поиска
- `JS_PATTERNS` - паттерны для JS анализа
- `XSS_PAYLOADS` - XSS payloads
- `SQL_PAYLOADS` - SQL injection payloads
- `INTERESTING_KEYS` - параметры для fuzzing

## Тестирование

**Легальные площадки для практики:**
- DVWA (Damn Vulnerable Web Application)
- WebGoat (OWASP)
- HackTheBox
- TryHackMe

## ⚠️ Важно

**ИСПОЛЬЗУЙТЕ ТОЛЬКО С РАЗРЕШЕНИЕМ!**

Перед использованием прочитайте `SECURITY_GUIDE.md`

## Помощь

```bash
python main.py --help
```

## Версия

Текущая версия: **2.1.0**

Дата обновления: **2026-05-18**
