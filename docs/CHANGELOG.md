# Changelog

Все значимые изменения в проекте будут документированы в этом файле.

## [2.1.0] - 2026-05-18

### Добавлено
- ✨ Новый модуль SQL Injection Scanner
  - Тестирование GET параметров
  - Тестирование форм
  - Обнаружение SQL ошибок
  - Time-based injection detection
  - Поддержка множества СУБД

- 📝 Централизованный config.py
  - Все настройки в одном месте
  - Расширенные списки payloads
  - Новые паттерны для JS Analyzer
  - SQL injection payloads и error patterns

- 🔍 Улучшенный JS Analyzer
  - Поиск приватных ключей
  - Обнаружение email адресов
  - Поиск телефонных номеров
  - Больше паттернов для API ключей

- 🛡️ Расширенный Header Scanner
  - Дополнительные security headers
  - Больше чувствительных файлов
  - Улучшенная логика проверки

- ⚡ Улучшенный Parameter Fuzzer
  - Больше fuzz values
  - Path traversal payloads
  - NoSQL injection payloads
  - Template injection payloads

- 💉 Расширенный XSS Scanner
  - Новые bypass техники
  - Больше векторов атак
  - Улучшенная обработка форм

### Изменено
- 🔧 Рефакторинг всех модулей для использования config.py
- 📚 Обновлена документация
- 🎨 Улучшен интерактивный интерфейс
- 🐛 Исправлены ошибки импортов
- 🔨 Исправлены проблемы с отступами в коде

### Документация
- 📖 Добавлен подробный README.md
- 📝 Создан EXAMPLES.md с примерами использования
- 📋 Добавлен CHANGELOG.md

## [2.0.0] - Предыдущая версия

### Базовый функционал
- Header Scanner
- JS Analyzer
- XSS Scanner
- Parameter Fuzzer
- Интерактивный режим
- CLI режим

---

## Планы на будущее

### [2.2.0] - Планируется
- [ ] SSRF Scanner
- [ ] XXE Scanner
- [ ] CSRF Token Analyzer
- [ ] Subdomain Enumeration
- [ ] Directory Bruteforce
- [ ] SSL/TLS Analyzer
- [ ] Webhook Testing
- [ ] Rate Limiting Detection

### [2.3.0] - В разработке
- [ ] Reporting module (HTML/PDF отчеты)
- [ ] Database для сохранения результатов
- [ ] Web UI
- [ ] Интеграция с Burp Suite
- [ ] Proxy support
- [ ] Authentication handling
- [ ] Session management

### [3.0.0] - Долгосрочные планы
- [ ] Machine Learning для обнаружения аномалий
- [ ] Автоматическая эксплуатация найденных уязвимостей
- [ ] Distributed scanning
- [ ] Cloud integration
- [ ] API для интеграции с CI/CD
