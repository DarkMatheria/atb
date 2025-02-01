import aiohttp
import asyncio
import json
from functools import wraps

class Bot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.handlers = []
        self.callback_handlers = []
        self.text_handlers = []
        self.start_time = None
        self.error_handled = False
    async def get_updates(self, offset=None, timeout=30):
        url = self.base_url + "getUpdates"
        params = {k: v for k, v in {"timeout": timeout, "offset": offset}.items() if v is not None}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def send_message(self, chat_id, text, reply_markup=None):
        url = self.base_url + "sendMessage"
        params = {"chat_id": chat_id, "text": text}
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def answer_callback_query(self, callback_query_id, text=None):
        url = self.base_url + "answerCallbackQuery"
        params = {
            "callback_query_id": callback_query_id,
            "text": text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def run(self, decorator, su=False, nm=False):
        self.start_time = asyncio.get_event_loop().time() if su else None
        last_update_id = None
        while True:
            try:
                updates = await self.get_updates(offset=last_update_id)
                for update in updates.get("result", []):
                    if "message" in update:
                        message_data = update["message"]
                        message = Message(message_data, self)
                        for handler in decorator.handlers:
                            await handler(message)
                        for handler in decorator.text_handlers:
                            await handler(message)
                    elif "callback_query" in update:
                        callback_query = update["callback_query"]
                        for handler in decorator.callback_handlers:
                            await handler(callback_query, self)
                    last_update_id = update["update_id"] + 1
            except Exception as e:
                if not self.error_handled:
                    print(f"{e}")
                    self.error_handled = True
                raise
            await asyncio.sleep(1)

class CallbackQuery:
    def __init__(self, callback_query_data, bot):
        self.callback_query_data = callback_query_data
        self.bot = bot
        self.id = callback_query_data["id"]
        self.data = callback_query_data.get("data", "")
        self.message = Message(callback_query_data["message"], bot) if "message" in callback_query_data else None

    async def answer(self, text=None):
        return await self.bot.answer_callback_query(self.id, text)

class Decorator:
    def __init__(self, bot):
        self.bot = bot
        self.handlers = []
        self.callback_handlers = []
        self.text_handlers = []

    def handler(self, command=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(message):
                if command is None or message.text.startswith(command):
                    await func(message)
            self.handlers.append(wrapper)
            return wrapper
        return decorator

    def callback(self, condition=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(callback_query, bot):
                if condition is None or condition(CallbackQuery(callback_query, bot)):
                    await func(CallbackQuery(callback_query, bot))
            self.callback_handlers.append(wrapper)
            return wrapper
        return decorator

    def text(self, condition=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(message):
                if condition is None or condition(message):
                    await func(message)
            self.text_handlers.append(wrapper)
            return wrapper
        return decorator

class InlineMarkup:
    def __init__(self, row=1):
        self.row = row
        self.keyboard = []

    def add(self, *buttons):
        for i in range(0, len(buttons), self.row):
            self.keyboard.append(buttons[i:i + self.row])

    def to_dict(self):
        return {"inline_keyboard": [[btn.to_dict() for btn in row] for row in self.keyboard]}

class InlineButton:
    def __init__(self, text, callback_data=None, url=None, miniapp=False):
        if miniapp and url:
            self.button = {"text": text, "web_app": {"url": url}}
        elif url:
            self.button = {"text": text, "url": url}
        elif callback_data:
            self.button = {"text": text, "callback_data": callback_data}
        else:
            self.button = {"text": text}

    def to_dict(self):
        return self.button

class ReplyMarkup:
    def __init__(self, row=1, resize_keyboard=True, one_time_keyboard=False):
        self.row = row
        self.keyboard = []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def add(self, *buttons):
        for i in range(0, len(buttons), self.row):
            self.keyboard.append(buttons[i:i + self.row])

    def to_dict(self):
        return {
            "keyboard": [[btn.to_dict() for btn in row] for row in self.keyboard],
            "resize_keyboard": self.resize_keyboard,
            "one_time_keyboard": self.one_time_keyboard
        }


class ReplyButton:
    def __init__(self, text, request_contact=False, request_location=False):
        self.button = {"text": text}
        if request_contact:
            self.button["request_contact"] = True
        if request_location:
            self.button["request_location"] = True

    def to_dict(self):
        return self.button

class Message:
    def __init__(self, message_data, bot):
        self.message_data = message_data
        self.bot = bot
        self.chat_id = message_data["chat"]["id"]
        self.message_id = message_data["message_id"]
        self.text = message_data.get("text", "")

    async def send(self, text, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        elif isinstance(reply_markup, InlineButton):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_message(self.chat_id, text, reply_markup)

    async def reply(self, text, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        elif isinstance(reply_markup, InlineButton):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_message(self.chat_id, text, reply_markup)
