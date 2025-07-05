# ai_bot_yandexgpt
ai Telegram bot with YandexGPT
# Telegram-YandexGPT Бот 🤖

Интеграция Telegram с YandexGPT для создания интеллектуального ассистента с историей диалога и адаптивным стилем общения.

## Особенности ✨
- 💬 Анализ стиля общения пользователя (формальный/неформальный)
- 🧠 Сохранение истории диалогов в JSON-файлах
- ⏱️ Искусственная задержка ответов для естественности
- ⌨️ Индикатор "печатает..." в реальном времени
- 📚 Автозагрузка истории из Telegram
- 🔒 Работа только в личных чатах (приватных сообщениях)

## Технологический стек
- Python 3.8+
- Telethon (библиотека для Telegram MTProto API)
- YandexGPT API
- ConfigParser для управления настройками

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/sergeyzhinskiy/ai_bot_yandexgpt.git
cd telegram-yandexgpt-bot
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Создайте файл конфигурации config.ini:
```ini
[Telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
username = YOUR_BOT_USERNAME

[Yandex]
yandexgpt_api = YOUR_YANDEX_GPT_API_KEY
```
Запустите бота:
```bash
python yand4.py
```
Конфигурация ⚙️
```python
# Настройки диалога
MAX_HISTORY_LENGTH = 15       # Макс. сообщений в контексте
MAX_TOKENS = 4000             # Макс. токенов в ответе
MAX_HISTORY_MESSAGES = 100    # Макс. сообщений для загрузки из Telegram

# Системный промпт
SYSTEM_PROMPT = """
Ты - дружелюбный помощник в Telegram...
"""
```
Логирование 📝

Все события логируются в telegram_bot.log

Режим логирования: INFO (можно переключить на DEBUG в коде)

Формат: Время - Имя - Уровень - Сообщение

Принцип работы 🔄
Пользователь отправляет сообщение в личный чат с ботом

Бот определяет стиль общения (формальный/неформальный)

Загружается история диалога (локальная + из Telegram)

Формируется запрос к YandexGPT с контекстом

Ответ обрабатывается и отправляется с искусственной задержкой

Весь диалог сохраняется в JSON-файл

Структура файлов 📂
```text
├── yand4.py                  # Основной скрипт бота
├── config.ini                # Файл конфигурации (не включен в репозиторий)
├── requirements.txt          # Зависимости
├── telegram_bot.log          # Файл логов (автогенерация)
└── chat_history/             # Папка с историей диалогов
    └── user_12345.json       # Пример файла истории пользователя
```
Безопасность 🔒
API-ключи хранятся в config.ini 

История диалогов сохраняется локально

Бот работает только в личных чатах

Ограничения ⚠️
Только текстовые сообщения

Макс. длина контекста: 15 сообщений

Макс. токенов в ответе: 4000

Работает только с YandexGPT API

Автор
sergeyzhinskiy - 2025

🤝 Поддержка
По вопросам доработки:

Telegram: @Russkayamednayakompaniya

Email: sergeyzhinskiy@gmail.com

📌 Коммерческое использование: Требуется согласование
==============================

# Telegram-YandexGPT Bot 🤖

Integration of Telegram with YandexGPT to create an intelligent assistant with a dialogue history and an adaptive communication style.

## Features ✨
- 💬 Analysis of user communication style (formal/informal)
- 🧠 Saving dialogue history in JSON files
- ⏱️ Artificial delay of responses for naturalness
- ⌨️ Real-time "typing..." indicator
- 📚 Auto-download of history from Telegram
- 🔒 Works only in personal chats (private messages)

## Tech stack
- Python 3.8+
- Telethon (library for Telegram MTProto API)
- YandexGPT API
- ConfigParser for managing settings

## Installation and launch

1. Clone the repository:
```bash
git clone https://github.com/sergeyzhinskiy/ai_bot_yandexgpt.git
cd telegram-yandexgpt-bot
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Create a config.ini configuration file:
```ini
[Telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
username = YOUR_BOT_USERNAME

[Yandex]
yandexgpt_api = YOUR_YANDEX_GPT_API_KEY
```
Run the bot:
```bash
python yand4.py
```
Configuration ⚙️
```python
# Dialog settings
MAX_HISTORY_LENGTH = 15 # Max. messages in context
MAX_TOKENS = 4000 # Max. tokens in response
MAX_HISTORY_MESSAGES = 100 # Max. messages to download from Telegram

# System prompt
SYSTEM_PROMPT = """
You are a friendly assistant in Telegram...
"""
```
Logging 📝
All events are logged in telegram_bot.log

Logging mode: INFO (can be switched to DEBUG in the code)

Format: Time - Name - Level - Message

How it works 🔄
The user sends a message to a personal chat with the bot

The bot determines the communication style (formal/informal)

The dialogue history is loaded (local + from Telegram)

A request to YandexGPT with context is generated

The response is processed and sent with an artificial delay

The entire dialogue is saved to a JSON file

File structure 📂
```text
├── yand4.py # Main bot script
├── config.ini # Configuration file (not included in the repository)
├── requirements.txt # Dependencies
├── telegram_bot.log # Log file (auto-generated)
└── chat_history/ # Dialog history folder
└── user_12345.json # Example of user history file
```
Security 🔒
API keys are stored in config.ini 

Dialog history is saved locally

The bot only works in private chats

Limitations ⚠️
Text messages only

Max. context length: 15 messages

Max. tokens in response: 4000

Works only with YandexGPT API

Author
sergeyzhinskiy - 2025

🤝 Support
For questions about improvements:

Telegram: @Russkayamednayakompaniya

Email: sergeyzhinskiy@gmail.com

📌 Commercial use: Requires approval
