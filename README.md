# atb
ATB is free-use library for developing telegram bots
<br>The abbreviation ATB means asyncio telegram bot
<br>version: 0.1
# installing (locally)

``` sh
cd atb & pip install .
```

# test use
``` python
import asyncio
from atb import *

API_TOKEN = ""

bot = Bot(API_TOKEN)
decorator = Decorator(bot)

@decorator.handler("/start")
async def start_handler(message):
    keyboard = InlineMarkup(row=1)
    button1 = InlineButton("huy", "huy")
    button2 = InlineButton("Click on me", "call_to_site", url="https://example.com/", miniapp=True) 
    button3 = InlineButton("Test", "test")
    keyboard.add(button1, button2)
    await message.send("Hello, world!", reply_markup=keyboard)

@decorator.callback(lambda cq: cq.data == "test")
async def callback_handler(callback_query):
    await callback_query.answer("test message...")
    
@decorator.callback(lambda cq: cq.data == "huy")
async def callback_handler(callback_query):
    await callback_query.message.send("Huy!")

@decorator.handler("/keyboard")
async def keyboard_handler(message):
    keyboard = ReplyMarkup(row=1)
    button1 = ReplyButton("Button")
    button2 = ReplyButton("Request contact", request_contact=True)
    button3 = ReplyButton("Request location", request_location=True)
    keyboard.add(button1, button2, button3)
    await message.send("Choose button:", keyboard)

@decorator.text(lambda message: message.text == "Button")
async def location(message):
	await message.send("...")
@decorator.text(lambda message: message.text == "Request location")
async def location(message):
	await message.answer("..")

@decorator.text(lambda message: message.text == "Request contact")
async def contact(message):
    await message.reply(".")

async def main():
    await bot.run(decorator)

if __name__ == "__main__":
    asyncio.run(main())
```
