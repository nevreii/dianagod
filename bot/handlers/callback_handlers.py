from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from bot.parser.itproger_parser import HabrParser
from bot.keyboards.inline import article_keyboard, pagination_keyboard
from bot.handlers.user_handlers import current_articles, current_page, display_article

parser = HabrParser()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Основной обработчик callback запросов"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith(('next_', 'prev_')):
        await handle_article_navigation(update, context)
    elif data.startswith('read_'):
        await handle_read_article(update, context)
    elif data.startswith('page_'):
        await handle_pagination(update, context)
    elif data == 'new_search':
        await handle_new_search(update, context)

async def handle_article_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка навигации по статьям"""
    global current_articles
    
    query = update.callback_query
    data = query.data
    current_index = int(data.split('_')[1])
    
    if data.startswith('next_'):
        new_index = current_index + 1
    elif data.startswith('prev_'):
        new_index = current_index - 1
    else:
        return
    
    if 0 <= new_index < len(current_articles):
        await query.delete_message()
        article = current_articles[new_index]
        
        text = f"<b>{article['title']}</b>\n\n"
        text += f"📅 {article['publish_time']}\n\n"
        text += f"📝 {article['preview']}\n\n"
        text += f"🔗 <a href='{article['url']}'>Источник</a>"
        
        await query.message.reply_text(
            text,
            reply_markup=article_keyboard(article['url'], new_index, len(current_articles)),
            parse_mode='HTML'
        )
    else:
        await query.answer("❌ Это первая/последняя статья")

async def handle_read_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка чтения полной статьи"""
    query = update.callback_query
    article_url = query.data.replace('read_', '')
    
    await query.answer("🔄 Загружаю полную статью...")
    
    full_article = parser.get_article_content(article_url)
    
    if full_article:
        text = f"<b>{full_article['title']}</b>\n\n"
        text += f"{full_article['content'][:4000]}..." if len(full_article['content']) > 4000 else full_article['content']
        
        await query.message.reply_text(text, parse_mode='HTML')
    else:
        await query.message.reply_text("❌ Не удалось загрузить полную статью.")

async def handle_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка пагинации"""
    global current_page, current_articles
    
    query = update.callback_query
    page = int(query.data.split('_')[1])
    current_page = page
    
    await query.answer("🔄 Загружаю статьи...")
    
    current_articles = parser.get_news_list(page=current_page)
    
    if current_articles:
        await query.delete_message()
        article = current_articles[0]
        
        text = f"<b>{article['title']}</b>\n\n"
        text += f"📅 {article['publish_time']}\n\n"
        text += f"📝 {article['preview']}\n\n"
        text += f"🔗 <a href='{article['url']}'>Источник</a>"
        
        await query.message.reply_text(
            text,
            reply_markup=article_keyboard(article['url'], 0, len(current_articles)),
            parse_mode='HTML'
        )
    else:
        await query.answer("❌ Не удалось загрузить статьи")

async def handle_new_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нового поиска"""
    query = update.callback_query
    await query.message.reply_text("🔍 Введите новый поисковый запрос:")

def register_callback_handlers(application):
    """Регистрация обработчиков callback"""
    application.add_handler(CallbackQueryHandler(handle_callback))