import telegram
from creds import creds

bot = telegram.Bot(token=creds.Telegram_API_Key())
print(bot.get_me())