import telegram
import os

bot = None

def Get():
  if bot is None:
      bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_API_KEY'])
  return bot