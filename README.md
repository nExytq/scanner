# 🛡️ PEN-TEST MULTI-TOOL v2.1

Многофункциональный инструмент для тестирования безопасности веб-приложений.

## 🚀 Возможности

### 1. Header & Config Scanner
- Проверка наличия security headers (CSP, HSTS, X-Frame-Options и др.)
- Анализ CORS политик
- Поиск чувствительных файлов (.env, config.php, backup файлы и т.д.)
- Обнаружение открытых административных панелей

### 2. JS File Analyzer
- Поиск API endpoints в JavaScript файлах
- Обнаружение утечек ключей (Firebase, AWS, GitHub, Stripe и др.)
- Поиск JWT токенов
- Обнаружение внутренних IP адресов
- Поиск email адресов и телефонов

### 3. XSS Scanner
- Автоматическое обнаружение форм на странице
- Тестирование различных XSS payloads
- Проверка reflected XSS
- Поддержка различных bypass техник

### 4. SQL Injection Scanner
- Тестирование GET параметров
- Тестирование форм (POST/GET)
- Обнаружение SQL ошибок в ответах
- Time-based SQL injection detection
- Поддержка различных СУБД (MySQL, PostgreSQL, MSSQL, Oracle)

### 5. Parameter Fuzzer (IDOR/Mass Assignment)
- Автоматическое обнаружение интересных параметров (id, user_id, role и т.д.)
- Fuzzing с различными значениями
- Обнаружение IDOR уязвимостей
- Тестирование Mass Assignment
- Поддержка path traversal и injection payloads

## 📦 Установка

```bash
git clone <your-repo>
cd scanner
pip install -r requirements.txt
```

## 🎯 Использование

### Интерактивный режим
```bash
python main.py
```

### CLI режим

**Header Scanner:**
```bash
python main.py http://example.com -m headers
```

**JS Analyzer:**
```bash
python main.py http://example.com -m js
```

**XSS Scanner:**
```bash
python main.py http://example.com -m xss
```

**SQL Injection Scanner:**
```bash
python main.py http://example.com -m sql
```

**Parameter Fuzzer:**
```bash
python main.py http://example.com/api/user -m fuzz -p '{"user_id": 123, "role": "user"}'
```

**Запустить все сканеры:**
```bash
python main.py http://example.com -m all
```

## ⚙️ Конфигурация

Все настройки находятся в `config.py`:

- `SECURITY_HEADERS` - список проверяемых security headers
- `SENSITIVE_FILES` - список чувствительных файлов для поиска
- `JS_PATTERNS` - regex паттерны для поиска в JS файлах
- `INTERESTING_KEYS` - параметры для fuzzing
- `XSS_PAYLOADS` - XSS payloads для тестирования
- `SQL_PAYLOADS` - SQL injection payloads
- `SQL_ERRORS` - паттерны SQL ошибок

## 🔧 Расширение функционала

### Добавление новых payloads

Отредактируйте `config.py` и добавьте свои payloads в соответствующие списки:

```python
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "ваш_новый_payload",
]
```

### Добавление новых паттернов для JS Analyzer

```python
JS_PATTERNS = {
    'Your Pattern Name': r'your_regex_pattern',
}
```

## ⚠️ Важно

**ИСПОЛЬЗУЙТЕ ТОЛЬКО ДЛЯ ЛЕГАЛЬНОГО ТЕСТИРОВАНИЯ!**

- Получите письменное разрешение перед тестированием
- Не используйте на production системах без согласования
- Соблюдайте законы вашей страны
- Используйте только в образовательных целях или в рамках bug bounty программ

## 📝 Лицензия

Для образовательных целей и легального пентестинга.

## 🤝 Вклад

Приветствуются pull requests с новыми функциями и улучшениями!

## 📧 Контакты

Для вопросов и предложений создавайте issues в репозитории.
