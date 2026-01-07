from fastapi import APIRouter, Request, HTTPException
from app.core.telegram_bot import create_app, process_webhook_update
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Lazy load the bot app only when needed (for serverless efficiency)
bot_app = None

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """
    Handle incoming Telegram updates via Webhook.
    """
    global bot_app
    
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Initialize Bot App if not ready
    if not bot_app:
        bot_app = create_app()
        if not bot_app:
            raise HTTPException(status_code=500, detail="Bot configuration failed")
        
        # Initialize the application (connects to bot API, etc.)
        await bot_app.initialize()

    # Process the update
    await process_webhook_update(bot_app, data)
    
    return {"status": "ok"}
