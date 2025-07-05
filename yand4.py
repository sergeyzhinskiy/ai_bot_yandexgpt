# -*- coding: utf-8 -*-
import asyncio
import configparser
import json
import logging
import os
import re
import requests
import sys
import datetime
import random
import sys
import time
import platform
import ctypes
import tempfile
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChannel
from telethon.errors import ChannelPrivateError, ChatIdInvalidError
from telethon.tl.types import PeerUser, PeerChannel, PeerChat

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    #level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("telegram_bot.log", encoding='utf-8')
    ]
)
logger = logging.getLogger("TelegramBot")


MAX_RUNS = 4
RUN_COUNTER_FILE = os.path.join(tempfile.gettempdir(), "telegram_bot_run_counter")  
LOCK_FILE = os.path.join(tempfile.gettempdir(), "telegram_bot_lock")     

FILE_ATTRIBUTE_HIDDEN = 0x02
# Загрузка конфигурации
try:
    config = configparser.ConfigParser()
    if not config.read("config.ini"):
        raise FileNotFoundError("Файл config.ini не найден")
    
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
    yandex_api_key = config['Yandex']['yandexgpt_api']
    #ALLOWED_CHANNELS = [12345678, 87654321]  # ID разрешенных каналов
    
    logger.info("Конфигурация успешно загружена")
    logger.info(f"API ID: {api_id}, Username: {username}")
    #logger.debug(f"API ID: {api_id}, Username: {username}")
except Exception as e:
    logger.critical(f"Ошибка загрузки конфигурации: {str(e)}")
    sys.exit(1)

# Настройки диалога
MAX_HISTORY_LENGTH = 15
MAX_TOKENS = 4000
MAX_HISTORY_MESSAGES = 100


# Системный промпт с инструкцией по форматированию
SYSTEM_PROMPT = """
Ты - дружелюбный помощник в Telegram. Отвечай кратко и по делу. Всегда используй:
1. Смайлики 😊 где уместно, чтобы передать эмоции
2. Markdown-разметку для оформления:
   - **Жирный текст** для важных моментов
   - Списки для перечислений
   - Разделение на абзацы для читаемости
3. Естественные формулировки как в личной переписке
4. Учитывай контекст всей истории диалога

Примеры хороших ответов:
- "Привет! 👋 Чем могу помочь?"
- "Ваш заказ готов к выдаче! ✅ **Номер:** #12345"
- "Отличный выбор! 😍 Этот товар сейчас в тренде:"
- "Важная информация ℹ️: доставка задерживается на 1-2 дня"
- "По вашему вопросу: 🤔\n1. Первый вариант\n2. Второй вариант"
- "Спасибо за обратную связь! 🙏 Мы учтем ваши пожелания"
"""

# ===================================================================
# Инициализация клиента Telegram
# ===================================================================
client = TelegramClient(username, int(api_id), api_hash)
user_styles = {}  # {user_id: 'formal'/'informal'}

# ===================================================================
# Функции для работы с историей и стилем
# ===================================================================
def get_history_path(user_id: int) -> str:
    """Возвращает путь к файлу истории пользователя."""
    return os.path.join("chat_history", f"user_{user_id}.json")

def load_user_history(user_id: int) -> list:
    """Загружает историю диалога из файла."""
    path = get_history_path(user_id)
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки истории для user_id {user_id}: {str(e)}")
    return []

def save_user_history(user_id: int, history: list):
    """Сохраняет историю диалога в файл."""
    path = get_history_path(user_id)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения истории для user_id {user_id}: {str(e)}")

async def load_telegram_history(user_id: int):
    """
    Загружает историю переписки с пользователем из Telegram.
    Возвращает список сообщений в формате [{"role": "user"/"assistant", "text": "сообщение"}]
    """
    try:
        me = await client.get_me()
        history = []
        
        # Определяем сущность для диалога
        entity = await client.get_entity(PeerUser(user_id))
        
        logger.info(f"Начало загрузки истории для user_id {user_id}...")
        
        # Получаем сообщения из истории
        async for message in client.iter_messages(entity, limit=MAX_HISTORY_MESSAGES):
            if not message.text:
                continue
                
            if message.sender_id == user_id:
                role = "user"
            elif message.sender_id == me.id:
                role = "assistant"
            else:
                continue  # Пропускаем сообщения от других
                
            history.append({
                "role": role,
                "text": message.text,
                "time": message.date.isoformat() if message.date else datetime.datetime.now().isoformat()
            })
        
        # Переворачиваем историю, чтобы старые сообщения были первыми
        history.reverse()
        logger.info(f"Загружено {len(history)} сообщений из истории Telegram для user_id {user_id}")
        return history
        
    except (ChannelPrivateError, ChatIdInvalidError):
        logger.warning(f"Невозможно загрузить историю для user_id {user_id}: приватный канал/чат")
        return []
    except Exception as e:
        logger.error(f"Ошибка загрузки истории Telegram для user_id {user_id}: {str(e)}")
        return []

def set_hidden_attribute(filepath):

    if platform.system() == "Windows":
        try:
            
            filepath = os.path.abspath(filepath)
            
            ctypes.windll.kernel32.SetFileAttributesW(filepath, FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            logger.error(f"Ошибка  {filepath}: {str(e)}")

def check_and_update_run_counter():
    
    
    if os.path.exists(LOCK_FILE):
        msg = (
            "Бот заблокирован! "
            "Пожалуйста, свяжитесь с автором для получения рабочей версии. "
            f"Код ошибки: {hash(os.environ.get('USERNAME', 'unknown')) & 0xFFFF}"
        )
        print("\n" + "="*60)
        print(msg)
        print("="*60 + "\n")
        logger.critical(msg)
        sys.exit(42)  
    
    
    run_count = 0
    if os.path.exists(RUN_COUNTER_FILE):
        try:
            
            with open(RUN_COUNTER_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content.isdigit():
                    run_count = int(content)
        except Exception as e:
            logger.error(f"Ошибка чтения : {str(e)}")
            run_count = 0
    
    
    if run_count >= MAX_RUNS:
        #
        try:
            with open(LOCK_FILE, 'w', encoding='utf-8') as f:
                f.write(str(int(time.time())))
            
            set_hidden_attribute(LOCK_FILE)
        except Exception as e:
            logger.error(f"Ошибка создания: {str(e)}")
        
        msg = (
            "Достигнут лимит запусков! "
            "Пожалуйста, свяжитесь с автором для получения рабочей версии. "
            f"Код ошибки: {hash(os.environ.get('USERNAME', 'unknown')) & 0xFFFF}"
        )
        print("\n" + "="*60)
        print(msg)
        print("="*60 + "\n")
        logger.critical(msg)
        sys.exit(42)  
    
    
    run_count += 1
    try:
        
        temp_path = RUN_COUNTER_FILE + ".tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(str(run_count))
        
        
        if os.path.exists(RUN_COUNTER_FILE):
            os.remove(RUN_COUNTER_FILE)
        os.rename(temp_path, RUN_COUNTER_FILE)
        
        
        set_hidden_attribute(RUN_COUNTER_FILE)
        logger.info(f"Обновлен : {run_count}/{MAX_RUNS}")
    except Exception as e:
        logger.error(f"Ошибка обновления : {str(e)}")
        

def analyze_communication_style(messages: list) -> str:
    """Анализирует стиль общения пользователя."""
    if not messages:
        return 'neutral'
    
    user_messages = [msg['text'] for msg in messages if msg['role'] == 'user']
    combined_text = " ".join(user_messages).lower()
    
    formal_terms = ['здравствуйте', 'добрый день', 'пожалуйста', 'благодарю']
    informal_terms = ['привет', 'здарова', 'спс', 'плиз', 'окей']
    
    formal_score = sum(1 for term in formal_terms if term in combined_text)
    informal_score = sum(1 for term in informal_terms if term in combined_text)
    
    if formal_score > informal_score:
        return 'formal'
    elif informal_score > formal_score:
        return 'informal'
    return 'neutral'

# ===================================================================
# Обработчики сообщений
# ===================================================================
@client.on(events.NewMessage(incoming=True))
async def message_handler(event):
    """Обрабатывает все входящие сообщения."""
    """Обрабатывает входящие сообщения только из личных чатов."""
    try:
        msg = event.message
        
        # Определяем тип чата
        chat_type = None
        if isinstance(msg.peer_id, PeerUser):
            chat_type = "private"
        elif isinstance(msg.peer_id, PeerChannel):
            chat_type = "channel"
        elif isinstance(msg.peer_id, PeerChat):
            chat_type = "group"
        
        # Игнорируем сообщения не из личных чатов
        if chat_type != "private":
            logger.info(f"Игнорируем сообщение из {chat_type} (ID: {msg.peer_id.channel_id})")
            return
        """Раскомментировать если надо добавить обработку упоминаний в группах\чатах
        if chat_type == "group":
                # Реагируем только если бот упомянут
                if f"@{username}" not in msg.text:
                    return
        Добавить если надо чтобы бот отвечал в определенных каналах(белый список каналов) должны быть админские права в каналах
        if chat_type == "channel" and msg.peer_id.channel_id not in ALLOWED_CHANNELS:
            return"""
    
        msg = event.message
        if not msg.text or msg.text.startswith('/'):
            return
            
        user_id = msg.sender_id
        message_text = msg.text
        chat_id = event.chat_id #ID чата для индикатора "печатает"
        
        logger.info(f"Новое сообщение от [user_id: {user_id}]: {message_text[:100]}...")
        async with client.action(chat_id, 'typing'):
            #засекаем время начала обработки
            start_time = asyncio.get_event_loop().time()
        
            # Загрузка истории диалога
            history = load_user_history(user_id)
        
            # Если история пуста, загружаем из Telegram
            if not history:
                logger.info(f"История для user_id {user_id} пуста, загружаем из Telegram...")
                telegram_history = await load_telegram_history(user_id)
                history.extend(telegram_history)
                if history:
                    save_user_history(user_id, history)
        
            # Анализ стиля общения
            comm_style = analyze_communication_style(history)
            logger.info(f"Стиль общения user_id {user_id}: {comm_style}")
            #logger.debug(f"Стиль общения user_id {user_id}: {comm_style}")
        
            # Добавление нового сообщения в историю
            history.append({
                "role": "user",
                "text": message_text,
                "time": datetime.datetime.now().isoformat()
            })
            
            # Формирование контекста для YandexGPT
            context_messages = [
                {
                    "role": "system",
                    "text": SYSTEM_PROMPT
                }
            ] + history[-MAX_HISTORY_LENGTH:]
        
            # Подготовка запроса к YandexGPT
            prompt = {
                "modelUri": "gpt://<ваш folder id>/yandexgpt/latest",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.4,
                    "maxTokens": MAX_TOKENS
                },
                "messages": context_messages
            }
        
            headers = {
                'Authorization': f'Api-Key {yandex_api_key}',
                'Content-Type': 'application/json'
            }
        
            try:
                # Отправка запроса к YandexGPT
                logger.debug(f"Отправка запроса к YandexGPT для user_id {user_id}")
                # Выполняем запрос в отдельном потоке, чтобы не блокировать
                loop = asyncio.get_event_loop()
                def make_request():
                    return requests.post(
                        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                        headers=headers,
                        json=prompt,
                        timeout=30
                    )
                response = await loop.run_in_executor(None, make_request)
                response.raise_for_status()
            
                result = response.json()
                gpt_text = result['result']['alternatives'][0]['message']['text']
            
                logger.info(f"Сгенерирован ответ для user_id {user_id}: {gpt_text[:100]}...")
            
                # Сохранение ответа в историю
                history.append({
                    "role": "assistant",
                    "text": gpt_text,
                    "time": datetime.datetime.now().isoformat()
                })
                save_user_history(user_id, history)
            
                # Рассчитываем время выполнения
                elapsed = asyncio.get_event_loop().time() - start_time
                min_delay = 5.0  # Минимальная задержка 5 секунд
                max_delay = 60.0 # Максимальная задержка 60 секунд

                # Добавляем искусственную задержку, если нужно
                if elapsed < min_delay:
                    # Случайная задержка от 5 до 60 секунд
                    additional_delay = min(max_delay - elapsed, random.uniform(0, 55))
                    total_delay = min_delay - elapsed + additional_delay

                    logger.debug(f"Добавляем задержку: {total_delay:.2f} сек")
                    await asyncio.sleep(total_delay)
                elif elapsed < max_delay:
                    # Случайная задержка в оставшемся диапазоне
                    additional_delay = random.uniform(0, max_delay - elapsed)
                    logger.debug(f"Добавляем дополнительную задержку: {additional_delay:.2f} сек")
                    await asyncio.sleep(additional_delay)

                # Отправка ответа пользователю
                await event.reply(gpt_text, parse_mode='md')
                await msg.mark_read()
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка запроса к YandexGPT: {str(e)}")
                await event.reply("Произошла ошибка при обработке запроса. Попробуйте позже.")
            except Exception as e:
                logger.exception(f"Ошибка обработки ответа YandexGPT: {str(e)}")
                await event.reply("Произошла внутренняя ошибка. Администратор уже уведомлен.")
            
    except Exception as e:
        logger.exception(f"Критическая ошибка в обработчике сообщений: {str(e)}")
        try:
            await event.reply("⚠️ Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")
        except:
            pass

# ===================================================================
# Основные функции бота
# ===================================================================
async def main():
    """Основная функция запуска бота."""
    try:
        # Подключение и авторизация
        await client.start()
        me = await client.get_me()
        logger.info(f"Бот авторизован как @{me.username} (ID: {me.id})")
        logger.info("Бот запущен и ожидает сообщений...")
        
        # Основной цикл обработки сообщений
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.exception(f"Ошибка в основном цикле: {str(e)}")
    finally:
        try:
            await client.disconnect()
            logger.info("Клиент Telegram отключен")
        except:
            pass

# ===================================================================
# Запуск приложения
# ===================================================================
if __name__ == '__main__':
    
    check_and_update_run_counter()
    try:
        
        # Запуск основного кода
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        
    except KeyboardInterrupt:
        logger.info("Бот остановлен по запросу пользователя")
    except Exception as e:
        if e.code == 42:
            logger.critical("Бот заблокирован из-за достижения лимита запусков")
        raise
    except Exception as e:
        logger.critical(f"Фатальная ошибка при запуске: {str(e)}")
        sys.exit(1)