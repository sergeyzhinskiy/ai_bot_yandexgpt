# ai_bot_yandexgpt
ai Telegram bot with YandexGPT
# Smart Telegram bot with YandexGPT 🤖💬



**Last update**: July 2025
**Version**: 2.1.0
**License**: MIT

## 🔍 Description
AI assistant for Telegram with YandexGPT integration, which:
- Automatically detects the communication style (formal/informal)
- Saves the context of the dialogue (up to 15 messages)
- Works **only** in personal chats (ignores groups/channels)
- Format responses with Markdown and emoji

## ✨ Features
| Function | Description |
|---------|---------|
| **Chat filtering** | Reacts only to private messages |
| **Style analysis** | Determines whether to communicate on a "formal" or "formal" basis |
| **Dialog history** | Stores JSON files with history for each user |
| **Response delay** | Simulates typing (5-60 sec) |
| **Logging** | Detailed logs to the `telegram_bot.log` file |

## ⚙️ Technical requirements
- Python 3.10+
- Server with 512MB RAM (minimum)
- Access to Yandex Cloud API
- Telegram API keys

## 🚀 Quick start

1. Install dependencies:
```bash
pip install -r requirements.txt
Configure the configuration (config.ini):

ini
[Telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
username = YOUR_BOT_USERNAME

[Yandex]
yandexgpt_api = YOUR_YANDEX_API_KEY
Run the bot:

bash
python yand3.py

📂 Project structure
text
├── yand3.py # Main bot code
├── config.ini # Configuration
├── requirements.txt # Dependencies
├── chat_history/ # Directory with dialog history
│ └── user_123.json # Example of history file
└── telegram_bot.log # Log file

🌟 Additional features
python
# Enabling group processing (in code):
ALLOWED_CHANNELS = [123456] # IDs of allowed channels

# Setting up response delay:
MIN_DELAY = 5 # Minimum delay (sec)
MAX_DELAY = 60 # Maximum delay

🤝 Support
For questions about improvements:

Telegram: @Russkayamednayakompaniya

Email: sergeyzhinskiy@gmail.com

📌 Commercial use: Requires approval

=====================================
# Умный Telegram-бот с YandexGPT 🤖💬


**Последнее обновление**: Июль 2025  
**Версия**: 2.1.0  
**Лицензия**: MIT

## 🔍 Описание
AI-ассистент для Telegram с интеграцией YandexGPT, который:
- Автоматически определяет стиль общения (формальный/неформальный)
- Сохраняет контекст диалога (до 15 сообщений)
- Работает **только** в личных чатах (игнорирует группы/каналы)
- Форматирует ответы с Markdown и эмодзи

## ✨ Особенности
| Функция | Описание |
|---------|----------|
| **Фильтрация чатов** | Реагирует только на личные сообщения |
| **Анализ стиля** | Определяет "на ты" или "на вы" общаться |
| **История диалогов** | Хранит JSON-файлы с историей для каждого пользователя |
| **Задержка ответов** | Имитирует печатание (5-60 сек) |
| **Логирование** | Подробные логи в файл `telegram_bot.log` |

## ⚙️ Технические требования
- Python 3.10+
- Сервер с 512MB RAM (минимум)
- Доступ к API Yandex Cloud
- Telegram API ключи

## 🚀 Быстрый старт

1. Установите зависимости:
```bash
pip install -r requirements.txt
Настройте конфигурацию (config.ini):

ini
[Telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
username = YOUR_BOT_USERNAME

[Yandex]
yandexgpt_api = YOUR_YANDEX_API_KEY
Запустите бота:

bash
python yand3.py

📂 Структура проекта
text
├── yand3.py            # Основной код бота
├── config.ini          # Конфигурация
├── requirements.txt    # Зависимости
├── chat_history/       # Директория с историей диалогов
│   └── user_123.json   # Пример файла истории
└── telegram_bot.log    # Файл логов

🌟 Дополнительные возможности
python
# Включение обработки групп (в коде):
ALLOWED_CHANNELS = [123456] # ID разрешенных каналов

# Настройка задержки ответов:
MIN_DELAY = 5  # Минимальная задержка (сек)
MAX_DELAY = 60 # Максимальная задержка

🤝 Поддержка
По вопросам доработки:

Telegram: @Russkayamednayakompaniya

Email: sergeyzhinskiy@gmail.com

📌 Коммерческое использование: Требуется согласование
