import telegram
from creds import creds

def test_bot():
    bot = telegram.Bot(token=creds.Telegram_API_Key())
    bot_info = bot.get_me()
    print(dir(bot_info))
    if bot_info != None:
         assert bot_info != None, "nothing returned from Telegram!"
         assert "username" in dir(bot_info), "No username field in bot_info - this means we didn't get back a bot info!"