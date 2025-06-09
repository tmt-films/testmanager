from telethon import events
from telethon.tl.types import InputPeerUser
from help import HELP_CONTENT

async def handle_start(event):
    """Send a personalized welcome message."""
    user = await event.get_sender()
    await event.reply(f"Hi {user.first_name}! Welcome to the bot. Use /help to see commands.")

async def handle_help(event):
    """Display available commands or detailed help."""
    args = event.message.text.split(maxsplit=1)[1] if len(event.message.text.split()) > 1 else ""
    if args:
        command = args.strip().lower()
        help_text = HELP_CONTENT.get(command, f"No detailed help found for /{command}. Try /help.")
        await event.reply(help_text)
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
        await event.reply(help_text)

async def handle_rules(event):
    """View or set group rules."""
    db = event.client.db
    chat_id = str(event.chat_id)
    collection = db.rules
    args = event.message.text.split(maxsplit=1)[1] if len(event.message.text.split()) > 1 else ""
    
    chat = await event.get_chat()
    admins = [admin.user.id async for admin in event.client.iter_participants(chat, filter=event.client.types.ChatAdminRights)]
    
    if args and event.sender_id in admins:
        rules_text = args
        collection.update_one(
            {'group_id': chat_id},
            {'$set': {'rules': rules_text}},
            upsert=True
        )
        await event.reply(f"Rules updated: {rules_text}")
    else:
        result = collection.find_one({'group_id': chat_id})
        rules_text = result['rules'] if result else "No rules set. Admins can set rules with /rules <text>."
        await event.reply(rules_text)

async def handle_poll(event):
    """Create a poll with user-specified question and options."""
    args = event.message.text.split(maxsplit=2)[1:] if len(event.message.text.split()) > 1 else []
    if not args:
        await event.reply("Usage: /poll Question? Option1, Option2")
        return
    question = args[0]
    options = args[1].split(',') if len(args) > 1 else ["Yes", "No"]
    await event.reply(f"Poll: {question}", reply_markup=event.client.build_reply_markup([
        [event.client.types.KeyboardButtonPollOption(text=option.strip(), voters=0) for option in options]
    ], poll=event.client.types.Poll(question=question, answers=[event.client.types.PollAnswer(text=option.strip(), option_id=i) for i, option in enumerate(options)])))

async def handle_ban(event):
    """Ban a user (admin only)."""
    chat = await event.get_chat()
    admins = [admin.user.id async for admin in event.client.iter_participants(chat, filter=event.client.types.ChatAdminRights)]
    
    if event.sender_id not in admins:
        await event.reply("Admins only!")
        return
    if event.is_reply:
        replied_msg = await event.get_reply_message()
        user = await replied_msg.get_sender()
        await event.client.edit_permissions(chat, user, view_messages=False)
        await event.reply(f"Banned {user.first_name}")
    else:
        await event.reply("Reply to a user’s message to ban.")

async def handle_tagall(event):
    """Mention all group members (admin only)."""
    chat = await event.get_chat()
    admins = [admin.user.id async for admin in event.client.iter_participants(chat, filter=event.client.types.ChatAdminRights)]
    
    if event.sender_id not in admins:
        await event.reply("Admins only!")
        return
    members = [member async for member in event.client.iter_participants(chat)]
    mentions = [f"@{member.username}" for member in members if member.username and not member.bot]
    if mentions:
        await event.reply(" ".join(mentions[:20]))
    else:
        await event.reply("No members with usernames found.")

async def handle_echo(event):
    """Echo text messages in private chats."""
    if event.is_private and not event.message.text.startswith('/'):
        await event.reply(event.message.text)
