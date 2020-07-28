import telegram
from creds import Telegram_API_Key

bot = telegram.Bot(token=Telegram_API_Key())
print(bot.get_me())