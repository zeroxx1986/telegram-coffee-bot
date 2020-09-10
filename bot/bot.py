import telegram
from telegram.ext import Updater, MessageHandler, Filters
import os
import logging
from datetime import datetime, timezone
import requests
from lxml import html
import json
import re

updater = None
dispatcher = None

def Init():
    global updater, dispatcher
    if updater is None:
        updater = Updater(token=os.environ['TELEGRAM_BOT_API_KEY'], use_context=True)
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        dispatcher.add_handler(echo_handler)
        updater.start_polling()
        logger = logging.getLogger(__name__)
        logger.info("Starting bot...")
        return updater
    return None

def echo(update, context):
    logger = logging.getLogger(__name__)
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

