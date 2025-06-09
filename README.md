Telegram Bot

A Python-based Telegram bot with user-friendly and admin-focused features, built using the python-telegram-bot library. This bot uses MongoDB to store group rules and provides tools for group management and user interaction within Telegram.

Features

User Features





/start: Receive a personalized welcome message.



/help: View all available commands.



/poll: Create a poll with a question and options (e.g., /poll Favorite color? Red, Blue).



Echo Reply: Get an echo of your text messages in private chats.

Admin Features





/rules: View or set group rules (e.g., /rules No spam, be respectful), stored in MongoDB.



/ban: Ban a user by replying to their message (admin-only).



/tagall: Mention all group members with usernames (admin-only, limited to 20 to avoid spam).

Prerequisites





Python 3.8 or higher



A Telegram bot token from BotFather



MongoDB (local instance or MongoDB Atlas)



Git (optional, for Cloning the repository)

Setup





Clone the Repository:

git clone https://github.com/tmt-films/testmanager.git telegram-bot



Install Dependencies:

pip install -r requirements.txt



Set Up MongoDB:





Option 1: MongoDB Atlas (Cloud):





Create a free account at MongoDB Atlas.



Set up a cluster and get the connection string (e.g., mongodb+srv://user:password@cluster0.mongodb.net/telegram_bot).



Whitelist your IP address in Atlas for connectivity.



Option 2: Local MongoDB:





Install MongoDB locally (instructions).



Ensure MongoDB is running (mongod).



Use the default connection string: mongodb://localhost:27017/telegram_bot.



Set the MongoDB URI as an environment variable:

export MONGO_URI='your_mongodb_connection_string'



Get a Bot Token:





Open Telegram and start a chat with @BotFather.



Send /start and then /newbot.



Follow the prompts to create a bot and copy the token.



Set the Bot Token:





Option 1: Replace 'YOUR_BOT_TOKEN' in main.py with your token.



Option 2: Set an environment variable:

export BOT_TOKEN='your_bot_token_here'



Run the Bot:

python main.py



Add the Bot to a Group:





Add the bot to your Telegram group.



Grant admin permissions for features like /ban and /tagall.

Usage





Private Chats:





Send /start to get a welcome message.



Send any text to receive an echo reply.



Use /help to see commands.



Group Chats:





Use /rules to view rules or /rules <text> to set rules (admin-only).



Create polls with /poll Question? Option1, Option2.



Admins can ban users with /ban (reply to a user’s message).



Admins can mention all members with /tagall.

Database





The bot uses MongoDB to store group rules in a rules collection.



Each document has a group_id (chat ID) and rules (text).



The database is automatically accessed via the connection string provided in MONGO_URI.

Notes





Rate Limits: Telegram limits bot actions (e.g., 20 messages/minute per group). The bot is designed to avoid flooding.



Scalability: For large groups, consider switching to webhook mode and hosting on a server (e.g., Heroku).



Security: Keep your bot token and MongoDB URI secure. Use environment variables to avoid hardcoding.



MongoDB Connection: Ensure your MongoDB instance is running and accessible. Check logs for connection errors.

Contributing





Fork the repository.



Create a feature branch (git checkout -b feature/new-feature).



Commit changes (git commit -m 'Add new feature').



Push to the branch (git push origin feature/new-feature).



Open a pull request.

License

MIT License. See LICENSE for details.

Contact

For issues or suggestions, open an issue on GitHub or contact the repository owner.
