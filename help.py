import logging
import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from pymongo import MongoClient
from pymongo.errors import ConnectionError
from dotenv import load_dotenv
from commands import start, help_command, rules, poll, ban, tagall, echo

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# MongoDB setup
def init_db():
    try:
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI not set in .env file")
        client = MongoClient(mongo_uri)
        db = client.get_database()
        client.admin.command('ping')
        logger.info("Connected to MongoDB")
        return db
    except ConnectionError as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise
    except ValueError as e:
        logger.error(e)
        raise

async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Run the bot."""
    db = init_db()
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("BOT_TOKEN not set in .env file")
    
    app = ApplicationBuilder().token(bot_token).build()
    app.bot_data['db'] = db
    
    # Add handlers from commands.py
    app.add_handler(start)
    app.add_handler(help_command)
    app.add_handler(rules)
    app.add_handler(poll)
    app.add_handler(ban)
    app.add_handler(tagall)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)
    
    app.run_polling()

if __name__ == '__main__':
    main()
