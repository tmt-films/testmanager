import logging
import sqlite3
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# SQLite database setup
def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/bot.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS rules (group_id TEXT PRIMARY KEY, rules TEXT)')
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a personalized welcome message."""
    user = update.effective_user
    await update.message.reply_text(f"Hi {user.first_name}! Welcome to the bot. Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display available commands."""
    help_text = (
        "Available Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this menu\n"
        "/rules - View or set group rules\n"
        "/poll - Create a poll\n"
        "/ban - Ban a user (admin only)\n"
        "/tagall - Mention all group members (admin only)\n"
        "Send any text in private chats to get an echo reply."
    )
    await update.message.reply_text(help_text)

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View or set group rules."""
    chat_id = str(update.effective_chat.id)
    conn = sqlite3.connect('data/bot.db')
    cursor = conn.cursor()
    
    if context.args and update.effective_user.id in [admin.user.id for admin in await update.effective_chat.get_administrators()]:
        # Set new rules (admin only)
        rules_text = ' '.join(context.args)
        cursor.execute('INSERT OR REPLACE INTO rules (group_id, rules) VALUES (?, ?)', (chat_id, rules_text))
        conn.commit()
        await update.message.reply_text(f"Rules updated: {rules_text}")
    else:
        # Show existing rules
        cursor.execute('SELECT rules FROM rules WHERE group_id = ?', (chat_id,))
        result = cursor.fetchone()
        rules_text = result[0] if result else "No rules set. Admins can set rules with /rules <text>."
        await update.message.reply_text(rules_text)
    
    conn.close()

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a poll with user-specified question and options."""
    if not context.args:
        await update.message.reply_text("Usage: /poll Question? Option1, Option2")
        return
    question = context.args[0]
    options = context.args[1].split(',') if len(context.args) > 1 else ["Yes", "No"]
    await update.message.reply_poll(question=question, options=options, is_anonymous=False)

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user (admin only)."""
    if update.effective_user.id not in [admin.user.id for admin in await update.effective_chat.get_administrators()]:
        await update.message.reply_text("Admins only!")
        return
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.effective_chat.ban_member(user.id)
        await update.message.reply_text(f"Banned {user.first_name}")
    else:
        await update.message.reply_text("Reply to a user’s message to ban.")

async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mention all group members (admin only)."""
    if update.effective_user.id not in [admin.user.id for admin in await update.effective_chat.get_administrators()]:
        await update.message.reply_text("Admins only!")
        return
    members = await update.effective_chat.get_members()
    mentions = [f"@{member.user.username}" for member in members if member.user.username and not member.user.is_bot]
    if mentions:
        await update.message.reply_text(" ".join(mentions[:20]))  # Limit to avoid spam
    else:
        await update.message.reply_text("No members with usernames found.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo text messages in private chats."""
    if update.effective_chat.type == "private":
        await update.message.reply_text(update.message.text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Run the bot."""
    init_db()
    bot_token = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')  # Use environment variable or default
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("poll", poll))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("tagall", tagall))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
