import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your actual admin chat ID
ADMIN_CHAT_ID = '6767895906'

# Dictionary to store user chat IDs
user_chat_ids = {}

# Function to handle the /getid command
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Your chat ID is: {user_id}")

# Function to handle messages in the group and send personal messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    user_query = update.message.text

    # Store user chat ID if not already stored
    if user_id not in user_chat_ids:
        user_chat_ids[user_id] = update.message.chat_id

    # Process the query and send a personal message to the user
    response = await process_query(user_query)
    if response:
        await send_personal_message(context, user_id, response)
    
    # Notify admin of the new query
    await notify_admin(context, user_id, user_name, user_query)

# Function to process user queries
async def process_query(query: str) -> str:
    print(f"Received query: {query}")  # Debug statement
    # Define a pattern to capture source and destination dynamically
    pattern = r'any runner from (\w+) to (\w+)|any runner to (\w+) from (\w+)'
    
    try:
        match = re.search(pattern, query.lower())
        if match:
            if match.group(1) and match.group(2):
                source = match.group(1)
                destination = match.group(2)
                return f"1.name:  2.Order Name: 3.payment: online or Cash your order is from {source} to {destination}. @ubairnoormalaysia"
            elif match.group(3) and match.group(4):
                source = match.group(4)
                destination = match.group(3)
                return f"Checking for runners to {destination} from {source}."
        else:
            return "No matching pattern found."
    except re.error as e:
        print(f"Regex error: {e}")
        return "Error processing your query."

# Function to send a personal message to a user
async def send_personal_message(context: ContextTypes.DEFAULT_TYPE, user_id: int, message: str) -> None:
    try:
        await context.bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"Error sending message to {user_id}: {e}")

# Function to notify the admin of a new user query
async def notify_admin(context: ContextTypes.DEFAULT_TYPE, user_id: int, user_name: str, user_query: str) -> None:
    admin_message = (f"Please @{user_name} (User ID: {user_id}):\n"
                     f"Query: {user_query}\n\n"
                     "Reply with '/reply <user_id> <message>' to respond to the user.")
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception as e:
        print(f"Error notifying admin: {e}")

# Function to handle admin replies
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id != int(ADMIN_CHAT_ID):
        return

    text = update.message.text
    if text.startswith('/reply'):
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            await update.message.reply_text("Usage: /reply <user_id> <message>")
            return

        user_id = int(parts[1])
        message = parts[2]

        if user_id in user_chat_ids:
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
                await update.message.reply_text(f"Message sent to user {user_id}.")
            except Exception as e:
                await update.message.reply_text(f"Error sending message: {e}")
        else:
            await update.message.reply_text("User ID not found.")

def main() -> None:
    application = ApplicationBuilder().token("7218750208:AAGL9bwS6II7-nfoKvesc83Dr2uq1kjO33M").build()

    # Add handlers
    application.add_handler(CommandHandler("getid", get_chat_id))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, handle_admin_reply))

    application.run_polling()

if __name__ == '__main__':
    main()



# 7218750208:AAGL9bwS6II7-nfoKvesc83Dr2uq1kjO33M