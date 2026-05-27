# 🚀 Telegram TODO/Shopping Bot

**Статус**: 📋 Разработка  
**Версия**: 1.0  
**Последнее обновление**: 2026-05-27  

---

## 📚 ДОКУМЕНТАЦИЯ

Все документы находятся в папке `docs/`:

| Документ | Назначение |
|----------|-----------|
| **docs/00_README_FIRST.md** | 📍 Начните отсюда! |
| **docs/01_QUICK_START.md** | 🚀 Быстрый старт (5 минут) |
| **docs/02_COMPREHENSIVE_PLAN.md** | 🎯 Главная документация |
| **docs/03_SECURITY_GUIDELINES.md** | 🔒 Безопасность |
| **docs/04_BEST_PRACTICES.md** | 💻 Best practices |
| **docs/05_INDEX.md** | 📚 Полная навигация |

---

## ⚡ БЫСТРЫЙ СТАРТ

```bash
# 1. Установить Python 3.8+
python --version

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Получить BOT_TOKEN от @BotFather в Telegram

# 5. Создать .env файл
cp .env.example .env
# И добавить BOT_TOKEN в .env

# 6. Запустить бота
python main.py

# 7. Тестировать в Telegram
/start
/todo add Первая задача
/todo list
```

---

## 📁 СТРУКТУРА ПРОЕКТА

```
telegram_todo_bot/
├── docs/                      # 📚 Документация (95KB)
│   ├── 00_README_FIRST.md
│   ├── 01_QUICK_START.md
│   ├── 02_COMPREHENSIVE_PLAN.md
│   ├── 03_SECURITY_GUIDELINES.md
│   ├── 04_BEST_PRACTICES.md
│   └── 05_INDEX.md
│
├── app/                       # 🤖 Основное приложение
│   ├── __init__.py
│   ├── bot.py                 # Инициализация бота
│   └── validators.py          # Валидаторы данных
│
├── handlers/                  # 🔧 Обработчики команд
│   ├── __init__.py
│   ├── common.py              # /start, /help, /cancel
│   ├── todo.py                # TODO команды
│   ├── shopping.py            # Shopping команды
│   ├── callbacks.py           # Callback кнопки
│   └── errors.py              # Обработка ошибок
│
├── database/                  # 💾 Хранилище данных
│   ├── __init__.py
│   └── storage.py             # JSON CRUD + кеширование
│
├── keyboards/                 # 🔘 Кнопки
│   ├── __init__.py
│   └── inline.py              # Inline кнопки
│
├── utils/                     # 🔨 Утилиты
│   ├── __init__.py
│   ├── formatters.py          # Форматирование сообщений
│   ├── logger.py              # Логирование
│   └── constants.py           # Константы
│
├── data/                      # 📊 Данные приложения
│   ├── data.json              # JSON база данных
│   └── backups/               # Резервные копии
│
├── logs/                      # 📋 Логи
│
├── tests/                     # 🧪 Тесты
│   ├── test_storage.py
│   └── test_handlers.py
│
├── main.py                    # 🔴 ГЛАВНЫЙ ФАЙЛ - запуск бота
├── config.py                  # ⚙️ Конфигурация
├── requirements.txt           # 📦 Зависимости
├── .env.example               # 🔐 Пример переменных окружения
├── .gitignore                 # Git игнорирует эти файлы
├── Procfile                   # 🚀 Для Heroku deployment
├── Dockerfile                 # 🐳 Для Docker
└── README.md                  # 📖 Этот файл
```

---

## 🎯 ТРЕБОВАНИЯ

- **Python**: 3.8+
- **pip**: инструмент управления пакетами
- **Telegram аккаунт**: для создания бота
- **Интернет**: для работы с Telegram API

---

## 📦 УСТАНОВКА

### 1. Клонировать или скачать репозиторий

```bash
git clone <url>
cd telegram_todo_bot
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
```

### 3. Активировать окружение

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

### 5. Получить BOT_TOKEN

1. Откройте Telegram
2. Найдите @BotFather
3. Отправьте `/newbot`
4. Следуйте инструкциям
5. Копируйте токен

### 6. Создать .env файл

```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте токен:
```env
BOT_TOKEN=ваш_токен_здесь
LOG_LEVEL=INFO
POLLING_TIMEOUT=30
```

### 7. Запустить бота

```bash
python main.py
```

Вы должны увидеть:
```
2026-05-27 12:00:00 - root - INFO - Bot started successfully
2026-05-27 12:00:00 - root - INFO - Polling started
```

---

## 🧪 ТЕСТИРОВАНИЕ

### Локально в Telegram

1. Найдите вашего бота по имени
2. Нажмите **START**
3. Тестируйте команды:

```
/start              # Информация о боте
/help               # Справка по командам
/todo add Тест      # Добавить задачу
/todo list          # Показать задачи
/shop add Молоко    # Добавить товар
/shop list          # Показать товары
```

### Автоматизированные тесты

```bash
# Запустить все тесты
pytest tests/ -v

# Только storage тесты
pytest tests/test_storage.py -v

# С coverage
pytest tests/ --cov
```

---

## 🚀 DEPLOYMENT

### На Railway (рекомендуется)

```bash
# 1. Установить Railway CLI
npm i -g @railway/cli

# 2. Логиниться
railway login

# 3. Инициализировать проект
railway init

# 4. Добавить переменные
railway variable set BOT_TOKEN="ваш_токен"

# 5. Развернуть
railway up
```

### На Heroku

```bash
# 1. Установить Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Логиниться
heroku login

# 3. Создать приложение
heroku create telegram-todo-bot

# 4. Добавить токен
heroku config:set BOT_TOKEN="ваш_токен"

# 5. Развернуть
git push heroku main

# 6. Включить worker
heroku ps:scale worker=1
```

### В Docker

```bash
# Построить образ
docker build -t telegram-todo-bot .

# Запустить контейнер
docker run -e BOT_TOKEN="ваш_токен" telegram-todo-bot
```

---

## 📖 ДОКУМЕНТАЦИЯ

Полная документация находится в папке `docs/`:

- 📍 **00_README_FIRST.md** - начните отсюда
- 🚀 **01_QUICK_START.md** - быстрый старт (5 минут)
- 🎯 **02_COMPREHENSIVE_PLAN.md** - полная техническая документация
- 🔒 **03_SECURITY_GUIDELINES.md** - безопасность приложения
- 💻 **04_BEST_PRACTICES.md** - best practices программирования
- 📚 **05_INDEX.md** - полная навигация

---

## 🔒 БЕЗОПАСНОСТЬ

- ✅ Используются переменные окружения для секретов
- ✅ Input validation везде
- ✅ Rate limiting защита
- ✅ Audit logging всех действий
- ✅ Atomic file writes + backups
- ✅ Защита от SQL injection

**Важно**: Никогда не коммитьте `.env` файл!

---

## 🐛 ОТЛАДКА

### Проверить логи

```bash
# Linux/Mac
tail -f logs/telegram_todo_bot.log

# Windows
Get-Content logs/telegram_todo_bot.log -Tail 50
```

### Типичные проблемы

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: aiogram` | `pip install -r requirements.txt` |
| `BOT_TOKEN not found` | Создайте `.env` файл с токеном |
| `Connection timeout` | Проверьте интернет соединение |
| `Permission denied` | Проверьте права на файлы |

---

## 📋 ЧЕКЛИСТ ПЕРЕД РАЗРАБОТКОЙ

- [ ] ✅ Python 3.8+ установлен
- [ ] ✅ Виртуальное окружение создано и активировано
- [ ] ✅ Зависимости установлены (`pip install -r requirements.txt`)
- [ ] ✅ BOT_TOKEN получен от @BotFather
- [ ] ✅ Файл `.env` создан с токеном
- [ ] ✅ Бот запущен и работает (`python main.py`)
- [ ] ✅ Прочитана документация в `docs/`
- [ ] ✅ Тестовые команды работают в Telegram

---

## 🎯 СЛЕДУЮЩИЕ ШАГИ

1. **Прочитайте документацию**
   - Откройте `docs/00_README_FIRST.md`
   - Потом `docs/01_QUICK_START.md`

2. **Запустите бота локально**
   - Следуйте инструкциям установки выше
   - Тестируйте в своей группе

3. **Изучите код**
   - Посмотрите структуру в `handlers/`
   - Посмотрите хранилище в `database/storage.py`

4. **Начните разработку**
   - Добавляйте новые команды в `handlers/`
   - Пишите тесты в `tests/`
   - Следуйте best practices из документации

5. **Разверните на production**
   - Выберите хостинг (Railway, Heroku, Docker)
   - Следуйте инструкциям в документации
   - Используйте security checklist

---

## 📞 ПОМОЩЬ

### Документация в проекте
- 📖 Полная техническая документация в `docs/02_COMPREHENSIVE_PLAN.md`
- 🔒 Гайд по безопасности в `docs/03_SECURITY_GUIDELINES.md`
- 💻 Best practices в `docs/04_BEST_PRACTICES.md`

### Внешние ресурсы
- [aiogram Документация](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

---

## 📄 ЛИЦЕНЗИЯ

MIT License - см. LICENSE файл

---

## 🙏 БЛАГОДАРНОСТИ

Создано с использованием:
- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot framework
- [Python](https://www.python.org/) - Programming language
- [Pydantic](https://github.com/pydantic/pydantic) - Data validation

---

**Статус**: 📋 Готово к разработке  
**Версия**: 1.0  
**Последнее обновление**: 2026-05-27

**→ Начните с**: `docs/00_README_FIRST.md` 🚀
