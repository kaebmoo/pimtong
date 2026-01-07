import asyncio
import logging
from app.core.telegram_bot import create_app

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def main():
    """Start the bot."""
    application = create_app()
    
    if not application:
        print("Failed to initialize bot. Check your settings.")
        return

    print("Starting Telegram Bot (Polling Mode)...")
    print("Press Ctrl+C to stop.")
    
    # Ensure any existing webhook (from Vercel) is removed before Polling
    # This specifically addresses the user's question about local testing.
    print("- Cleaning up webhooks...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(application.bot.delete_webhook(drop_pending_updates=True))
    
    # Run the bot until the user presses Ctrl-C
    # application.run_polling() is blocking and handles the event loop internally
    application.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bot stopped.")
