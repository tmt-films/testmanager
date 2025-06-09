import logging
import os
from telethon import TelegramClient, events
from pymongo import MongoClient
from pymongo.errors import ConnectionError
from dotenv import load_dotenv
from commands import handle_start, handle_help, handle_rules, handle_poll, handle_ban, handle_tagall, handle_echo

# Load environment variables
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

async def main():
    """Run the bot."""
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    bot_token = os.getenv('BOT_TOKEN')
    
    if not all([api_id, api_hash, bot_token]):
        raise ValueError("API_ID, API_HASH, or BOT_TOKEN not set in .env file")
    
    # Initialize Telethon client
    client = TelegramClient('bot', int(api_id), api_hash).start(bot_token=bot_token)
    
    # Initialize MongoDB
    db = init_db()
    
    # Register event handlers
    client.add_event_handler(handle_start, events.NewMessage(pattern='^/start(?:@\\w+)?$'))
    client.add_event_handler(handle_help, events.NewMessage(pattern='^/help(?:@\\w+)?(?:\\s+.*)?$'))
    client.add_event_handler(handle_rules, events.NewMessage(pattern='^/rules(?:@\\w+)?(?:\\s+.*)?$'))
    client.add_event_handler(handle_poll, events.NewMessage(pattern='^/poll(?:@\\w+)?(?:\\s+.*)?$'))
    client.add_event_handler(handle_ban, events.NewMessage(pattern='^/ban(?:@\\w+)?$'))
    client.add_event_handler(handle_tagall, events.NewMessage(pattern='^/tagall(?:@\\w+)?$'))
    client.add_event_handler(handle_echo, events.NewMessage)
    
    # Store db in client data
    client.db = db
    
    # Start the client
    try:
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Client error: {e}")
        raise

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
