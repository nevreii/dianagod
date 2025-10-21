from aiogram import Bot, Dispatcher

# УКАЖИТЕ ВАШ РЕАЛЬНЫЙ ТОКЕН ОТ @BotFather
BOT_TOKEN = "8293221474:AAFthWDq-K5k38BtIj1EKz-qpoCSG5IcmZI"

print("🔄 Создаем бота...")
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
print("🔄 Создаем диспетчер...")
dp = Dispatcher(bot)
print("✅ loader.py загружен!")