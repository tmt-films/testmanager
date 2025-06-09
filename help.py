HELP_CONTENT = {
    "start": """**`/start` Command**

Sends a personalized welcome message to the user.

**Usage**:
```
/start
```

**Description**:
- Greets the user by their first name.
- Provides a brief introduction to the bot.
- Suggests using `/help` to view all commands.

**Example**:
```
/start
```
**Response**: `Hi John! Welcome to the bot. Use /help to see commands.`
""",
    "help": """**`/help` Command**

Displays a list of available commands or detailed help for a specific command.

**Usage**:
```
/help [command]
```

**Description**:
- Without arguments, lists all available commands.
- With a command name (e.g., `/help rules`), shows detailed help for that command.

**Example**:
```
/help
```
**Response**: Lists all commands.

```
/help rules
```
**Response**: Shows detailed help for the `/rules` command.
""",
    "rules": """**`/rules` Command**

View or set group rules, stored in MongoDB.

**Usage**:
```
/rules [text]
```

**Description**:
- Without arguments, displays the current group rules.
- With text (admin-only), updates the group rules.
- Rules are stored in MongoDB for persistence.

**Example**:
```
/rules
```
**Response**: `No spam, be respectful` (or "No rules set" if none exist).

```
/rules No spam, be kind
```
**Response** (admin): `Rules updated: No spam, be kind`
""",
    "poll": """**`/poll` Command**

Creates a poll with a question and options.

**Usage**:
```
/poll Question? Option1, Option2
```

**Description**:
- Requires a question as the first argument.
- Options are comma-separated (defaults to "Yes", "No" if omitted).
- Polls are non-anonymous by default.

**Example**:
```
/poll Favorite color? Red, Blue
```
**Response**: Creates a poll with the question "Favorite color?" and options "Red", "Blue".
""",
    "ban": """**`/ban` Command**

Bans a user from the group (admin-only).

**Usage**:
```
/ban
```

**Description**:
- Must reply to a user’s message to ban them.
- Requires the bot to have admin permissions with ban privileges.
- Only group admins can use this command.

**Example**:
Reply to a user’s message with:
```
/ban
```
**Response**: `Banned [User's Name]`
""",
    "tagall": """**`/tagall` Command**

Mentions all group members with usernames (admin-only).

**Usage**:
```
/tagall
```

**Description**:
- Mentions up to 20 group members with usernames to avoid Telegram rate limits.
- Requires the bot to have admin permissions.
- Only group admins can use this command.
- Excludes bots and members without usernames.

**Example**:
```
/tagall
```
**Response**: `@User1 @User2 ...` (up to 20 usernames)
""",
    "echo": """**Echo Reply**

Echoes text messages sent in private chats.

**Usage**:
Send any text message in a private chat with the bot.

**Description**:
- The bot replies with the exact text message sent.
- Only works in private chats (not groups).
- Ignores commands (e.g., /start).

**Example**:
**Message**: `Hello`
**Response**: `Hello`
"""
}
