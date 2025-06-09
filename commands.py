from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from help import HELP_CONTENT

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a personalized welcome message."""
    user = update.effective_user
    await update.message.reply_text(f"Hi {user.first_name}! Welcome to the bot. Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display available commands or detailed help."""
    if context.args:
        command = context.args[0].lower()
        help_text = HELP_CONTENT.get(command, f"No detailed help found for /{command}. Try /help.")
        await update.message.reply_text(help_text)
    else:
        help_text = (
            "Available Commands:\n"
            "/start - Welcome message\n"
            "/help - Show this menu\n"
            "/rules - View or set group rules\n"
            "/poll - Create a poll\n"
            "/ban - Ban a user (admin only)\n"
            "/tagall - Mention all group members (admin only)\n"
            "Send any text in private chats to get an echo reply.\n"
            "Use /help <command> for detailed help (e.g., /help rules)."
        )
        await update.message.reply_text(help_text)

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View or set group rules."""
    db = context.bot_data.get('db')
    chat_id = str(update.effective_chat.id)
    collection = db.rules
    
    if context.args and update.effective_user.id in [admin.user.id for admin in await update.effective_chat.get_administrators()]:
        rules_text = ' '.join(context.args)
        collection.update_one(
            {'group_id': chat_id},
            {'$set': {'rules': rules_text}},
            upsert=True
        )
        await update.message.reply_text(f"Rules updated: {rules_text}")
    else:
        result = collection.find_one({'group_id': chat_id})
        rules_text = result['rules'] if result else "No rules set. Admins can set rules with /rules <text>."
        await update.message.reply_text(rules_text)

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
        await update.message.reply_text(" ".join(mentions[:20]))
    else:
        await update.message.reply_text("No members with usernames found.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo text messages in private chats."""
    if update.effective_chat.type == "private":
        await update.message.reply_text(update.message.text)

# Export handlers
start = CommandHandler("start", start)
help_command = CommandHandler("help", help_command)
rules = CommandHandler("rules", rules)
poll = CommandHandler("poll", poll)
ban = CommandHandler("ban", ban)
tagall = CommandHandler("tagall", tagall)
