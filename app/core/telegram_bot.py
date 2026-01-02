from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.core.config import settings

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to Pimtong Work Manager.",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help! Use /today to see your tasks.")

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show today's tasks."""
    # In a real app, query the database here using the user's telegram_id
    await update.message.reply_text("You have 2 tasks today:\n1. Repair TV at Mr. Somchai\n2. Install A/C @ Project X")

def create_app():
    """Create and configure the bot application."""
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Telegram Token not set, skipping bot setup.")
        return None
    
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("today", today_command))

    return application
