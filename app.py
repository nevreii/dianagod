from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers.user_handlers import register_user_handlers
from bot.handlers.callback_handlers import register_callback_handlers
import data.config as config

def main():
    """Запуск бота"""
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Регистрация обработчиков
    register_user_handlers(application)
    register_callback_handlers(application)
    
    print("Bot is running!")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()