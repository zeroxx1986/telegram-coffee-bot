import telegram
import Telegram_API_Key from creds

bot = telegram.Bot(token=Telegram_API_Key())
print(bot.get_me())