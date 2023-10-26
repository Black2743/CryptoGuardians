import logging
import json
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


joinedUsersJson={}
BUFFER_FILE="/home/black/Desktop/CryptoGuardians/detectSystem/telegramBot/buffer.json"
USERS_FILE = "/home/black/Desktop/CryptoGuardians/detectSystem/telegramBot/data.json"
with open(USERS_FILE, "r") as file:
    joinedUsersJson=json.load(file)
    

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    print(user_id)
    user_name = update.effective_user.first_name
    if user_id not in joinedUsersJson:
        joinedUsersJson[user_id]=True
        with open(USERS_FILE, "w") as users_file:
            json.dump(joinedUsersJson,users_file)
            print('in file writen '+user_id)
    
    print(joinedUsersJson)
    welcome_message = f"Здравствуйте, {user_name}!\nЭтот бот предназначен для помощи в реагировании на инциденты"
    await update.message.reply_text(welcome_message)


async def send_scheduled_message(bot,data):
    for chat_id,status in joinedUsersJson.items():
            if status:
                incident_text = (
                    f"Camera: {data['camera_name']}, {data['time']}\n"
                    f"Location: {data['location']}\n"
                    f"Incident: {data['incident']}\n"
                    f"Photo path: {data['photo']}"
                    )
                await bot.send_message(chat_id=chat_id, text=incident_text)
                await bot.send_photo(photo=open(data['photo'], 'rb'),chat_id=chat_id)

async def change_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    print(user_id)
    if joinedUsersJson[user_id]:
        joinedUsersJson[user_id]=False
    else:
        joinedUsersJson[user_id]=True
    await update.message.reply_text(f'Status {joinedUsersJson[user_id]}')
    print(joinedUsersJson)
    with open(USERS_FILE, "w") as users_file:
        json.dump(joinedUsersJson,users_file)
        print('in file writen '+user_id)


def buffer_empty_check(filePath):
    try:
        with open(filePath, 'r') as file:
            data = json.load(file)
            if not data:
                return 1  # JSON file empty
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return 2 
def clear_json_file(file_path):
    try:
        with open(file_path, 'w') as file:
            file.truncate(0)
    except (FileNotFoundError, json.JSONDecodeError):
        return

def schedule_messages(bot):
    async def scheduled_task():
        while True:
            try:
                data=buffer_empty_check(BUFFER_FILE)
                if buffer_empty_check==1 or buffer_empty_check==2:
                    pass
                else:
                    
                    clear_json_file(BUFFER_FILE)
                    await asyncio.gather(send_scheduled_message(bot,data))
                await asyncio.sleep(10) 
            except:
                await asyncio.sleep(10) 
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_task())

    
application = Application.builder().token("6839756530:AAGB0NG0hbkUyAa1QpQQGLWhrdhc6IKATzk").build()

def main() -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("changeStatus", change_status))
    schedule_messages(application.bot)
    application.run_polling()

if __name__ == "__main__":
    main()