import logging
import os

from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

alphabet = {
    "а": "闩",
    "б": "石",
    "в": "乃",
    "г": "广",
    "д": "亼",
    "е": "仨",
    "ё": "庄",
    "ж": "兴",
    "з": "弓",
    "и": "仈",
    "й": "认",
    "к": "长",
    "л": "人",
    "м": "爪",
    "н": "卄",
    "о": "口",
    "п": "门",
    "р": "户",
    "с": "仁",
    "т": "丁",
    "у": "丫",
    "ф": "中",
    "х": "乂",
    "ц": "凵",
    "ч": "丩",
    "ш": "山",
    "щ": "山",
    "ь": "",
    "ы": "辷",
    "ъ": "",
    "э": "彐",
    "ю": "扣",
    "я": "兄",
}


def translate(string: str):
    translated_string = "".join([alphabet.get(char.lower(), char) for char in string])
    return translated_string


# Включим логирование для отслеживания ошибок
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Команда /start


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой учитель корейского. Отправь мне любое сообщение, и я его переведу!"
    )

# Команда /help


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - получить справку\n\n"
        "Просто отправь мне текст, и я его переведу!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'Пользователь ({update.message.chat.id}) в {message_type}: "{text}"')

    response = translate(text)

    print('Бот отвечает:', response)
    await update.message.reply_text(response)

# Обработка ошибок


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Ошибка {context.error} для обновления {update}')


def main():
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Добавляем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Добавляем обработчик ошибок
    app.add_error_handler(error_handler)

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()
