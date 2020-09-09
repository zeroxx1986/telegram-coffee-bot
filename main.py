from bot import bot as Bot
import requests
from lxml import html

url = 'https://9gag.com/gag/amvMvQ2'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)
tree = html.fromstring(response.content)

image = tree.xpath('//link[@rel="image_src"]/@href')
if len(image) > 0:
    image_data = requests.get(image[0]).content
    print(image_data)
# print(image)

# bot = Bot.Get()

# print(bot.get_me())
print("testing")