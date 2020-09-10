import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import os
import logging
from datetime import datetime, timezone, timedelta
import requests
from lxml import html
import json
import re
from threading import Timer
from bot.quotes import quotes
import random

updater = None
dispatcher = None
logger = logging.getLogger(__name__)

coffeeTime = None
subscribers = []
t10 = t5 = t0 = None

def Init():
    global updater, dispatcher, logger
    if updater is None:
        updater = Updater(token=os.environ['TELEGRAM_BOT_API_KEY'], use_context=True)
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        
        gag_handler = MessageHandler(Filters.text & (~Filters.command), gag)
        coffee_handler = CommandHandler('coffee', coffee)
        sub_handler = CommandHandler('sub', sub)
        unsub_handler = CommandHandler('unsub', unsub)
        cancel_handler = CommandHandler('cancel', cancel)
        help_handler = CommandHandler('help', help)
        quote_handler = CommandHandler('quote', quote)

        dispatcher.add_handler(gag_handler)
        dispatcher.add_handler(coffee_handler)
        dispatcher.add_handler(sub_handler)
        dispatcher.add_handler(unsub_handler)
        dispatcher.add_handler(cancel_handler)
        dispatcher.add_handler(help_handler)
        dispatcher.add_handler(quote_handler)
        updater.start_polling()
        logger.info("Starting bot...")
        return updater
    return None

def sendNotification(bot, message):
    global logger, subscribers
    logger.info("HERE")
    for subscriber in subscribers:
        bot.send_message(chat_id=subscriber,
                         parse_mode=telegram.ParseMode.MARKDOWN_V2,
                         text=message)

def help(update, context):
    global logger
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 text='''
Hey fellow Coffee Lover\! Here are the commands you can use:

`/coffee <time>` \- set a time for coffee\! Can be relative \(e\.g\. 1\.5h\) or absolute \(10:00\)
`/sub` \- subscribe to the coffee event\!
`/unsub` \- unsubscribe from the coffee event :\(
`/cancel` \- cancel the coffee event :\(\(\(
`/quote` \- see a very helpful coffee quote to help you survive until Coffee Time\!\!\!
`/help` \- see this very helpful helping help\.halp\.haaaalp\!ha\#aA@2\.D\.\.\. rebooting in 3\.\.2\.\.1\.\. 🖖🏻
                                 ''')

def coffee(update, context):
    global logger, coffeeTime, subscribers, t10, t5, t0
    logger.info("Command received")
    logger.info(update.message.text)
    if update.message.text == '/coffee':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 text="Usage: `/coffee <time>`\nExample:\n`/coffee 1h` \- Coffee in 1 hour\n`/coffee 12:00` \- Coffee at noon \(24h format\)")
        return
    
    now = datetime.now()
    relTime = re.match('/coffee (\d+[,.]?\d*[hm])', update.message.text.lower())
    absTime = re.match('/coffee (\d+):(\d+)', update.message.text.lower())
    
    if relTime is not None:
        relTime = relTime.group(1).replace(',', '.')
        logger.info(relTime)
        if relTime[-1:] == 'h':
            coffeeTime = now + timedelta(hours=float(relTime[:-1]))
            logger.info("Coffee time: {}".format(coffeeTime))
        if relTime[-1:] == 'm':
            coffeeTime = now + timedelta(minutes=float(relTime[:-1]))
            logger.info("Coffee time: {}".format(coffeeTime))
    
    elif absTime is not None:
        coffeeTime = datetime(now.year, now.month, now.day, int(absTime[1]), int(absTime[2]))
        if coffeeTime < now:
            coffeeTime = coffeeTime + timedelta(days=1)
        logger.info(coffeeTime)
    
    if coffeeTime:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 text="New Coffee Time Announcement\!\!\nCoffee gathering at *{:0>2d}:{:0>2d}*\nSubscribe with `/sub` to receive notification\!".format(coffeeTime.hour, coffeeTime.minute))
        # clear subscribers & add sender
        subscribers = []
        subscribers.append(update.effective_user.id)
        subscribers.append(update.effective_chat.id)
        subscribers = list(dict.fromkeys(subscribers))
        # set T-10 notification timer
        if t10 is not None:
            t10.cancel()
            t10 = None
        secondsUntilNotification = ((coffeeTime - now) - timedelta(minutes=10)).total_seconds()
        logger.info("Seconds until T-10: {}".format(secondsUntilNotification))
        if secondsUntilNotification > 0:
            t10 = Timer(secondsUntilNotification, sendNotification, (context.bot, "10 minutes until Coffee Time\!"))
            t10.start()
        # set T-5 notification timer
        if t5 is not None:
            t5.cancel()
            t5 = None
        secondsUntilNotification = ((coffeeTime - now) - timedelta(minutes=5)).total_seconds()
        logger.info("Seconds until T-5: {}".format(secondsUntilNotification))
        if secondsUntilNotification > 0:
            t5 = Timer(secondsUntilNotification, sendNotification, (context.bot, "5 minutes until Coffee Time\!"))
            t5.start()
        # set T-0 notification timer
        if t0 is not None:
            t0.cancel()
            t0 = None
        secondsUntilNotification = (coffeeTime - now).total_seconds()
        logger.info("Seconds until T-0: {}".format(secondsUntilNotification))
        if secondsUntilNotification > 0:
            t0 = Timer(secondsUntilNotification, sendNotification, (context.bot, "Coffee Time\! ☕☕☕"))
            t0.start()

def sub(update, context):
    global logger, subscribers
    logger.info("Command received")
    subscribers.append(update.effective_user.id)
    subscribers = list(dict.fromkeys(subscribers))
    context.bot.send_message(chat_id=update.effective_user.id,
                             text="You are subscribed for the next Coffee Time! 😄")

def unsub(update, context):
    global logger, subscribers
    logger.info("Command received")
    subscribers.remove(update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_user.id,
                             text="You are unsubscribed from the next coffee event 😥")

def cancel(update, context):
    global logger, subscribers, t10, t5, t0, coffeeTime
    logger.info("Command received")
    sendNotification(context.bot, "Coffee time cancelled! 💔😭")
    subscribers = []
    if t10 is not None:
        t10.cancel()
        t10 = None
    if t5 is not None:
        t5.cancel()
        t5 = None
    if t0 is not None:
        t0.cancel()
        t0 = None
    coffeeTime = None

def quote(update, context):
    global logger
    logger.info("Command received")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=random.choice(quotes()))

def gag(update, context):
    global logger
    if update.message.text == None:
        return
    logger.info(update.message.text)
    # logger.info(dir(update.message))
    if (datetime.now(timezone.utc) - update.message.date).total_seconds() < 10:
        # recent message, let's deal with it!
        if 'https://9gag.com' in update.message.text:
            url = re.match('.*(https://(www\.)?9gag\.com/.*?)(\s|\n|$)', update.message.text)
            if url is None or len(url.groups()) != 3:
                return
            url = url.group(1)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            response = requests.get(url, headers=headers)
            tree = html.fromstring(response.content)

            title = tree.xpath('//meta[@property="og:title"]/@content')
            if len(title) > 0:
                title = title[0]
            else:
                title = None

            # determine if image or video
            gagType = tree.xpath('//meta[@property="og:description"]/@content')
            if len(gagType) > 0:
                gagType = gagType[0]
            logger.info(gagType)
            if gagType == "Watch the video and join the fun convo with 9GAG community":
                # video
                logger.info("gagType video")
                #logger.info(response.content)
                lastJS = tree.xpath('//script[@type="text/javascript"]/text()')
                if len(lastJS) > 0:
                    lastJS = lastJS[-1]
                    lastJS = lastJS.replace('window._config = JSON.parse("', "")[:-3].replace("\\\"", "\"").replace("\\\\/","/")
                    allData = json.loads(lastJS)
                    #print(json.dumps(allData, indent=4, sort_keys=True))
                    video = allData["data"]["post"]["images"]["image460sv"]["url"]
                    logger.info(video)
                    context.bot.send_video(chat_id=update.effective_chat.id, 
                                        reply_to_message_id=update.effective_message.message_id,
                                        caption=title,
                                        video=video)
            else:
                # image
                logger.info("gagType image")
                image = tree.xpath('//link[@rel="image_src"]/@href')
                logger.info(image)
                if len(image) > 0:
                    context.bot.send_photo(chat_id=update.effective_chat.id, 
                                        reply_to_message_id=update.effective_message.message_id,
                                        caption=title,
                                        photo=image[0])

