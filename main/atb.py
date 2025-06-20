import aiohttp
import asyncio
import json
from functools import wraps
import re

class Bot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.handlers = []
        self.callback_handlers = []
        self.text_handlers = []
        self.media_handlers = []
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

    async def send_photo(self, chat_id, photo, caption=None, reply_markup=None):
        url = self.base_url + "sendPhoto"
        params = {"chat_id": chat_id, "photo": photo}
        if caption:
            params["caption"] = caption
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_video(self, chat_id, video, caption=None, reply_markup=None):
        url = self.base_url + "sendVideo"
        params = {"chat_id": chat_id, "video": video}
        if caption:
            params["caption"] = caption
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_audio(self, chat_id, audio, caption=None, reply_markup=None):
        url = self.base_url + "sendAudio"
        params = {"chat_id": chat_id, "audio": audio}
        if caption:
            params["caption"] = caption
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_document(self, chat_id, document, caption=None, reply_markup=None):
        url = self.base_url + "sendDocument"
        params = {"chat_id": chat_id, "document": document}
        if caption:
            params["caption"] = caption
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_voice(self, chat_id, voice, caption=None, reply_markup=None):
        url = self.base_url + "sendVoice"
        params = {"chat_id": chat_id, "voice": voice}
        if caption:
            params["caption"] = caption
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_video_note(self, chat_id, video_note, reply_markup=None):
        url = self.base_url + "sendVideoNote"
        params = {"chat_id": chat_id, "video_note": video_note}
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_sticker(self, chat_id, sticker, reply_markup=None):
        url = self.base_url + "sendSticker"
        params = {"chat_id": chat_id, "sticker": sticker}
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_media_group(self, chat_id, media):
        url = self.base_url + "sendMediaGroup"
        params = {"chat_id": chat_id, "media": json.dumps(media)}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_location(self, chat_id, latitude, longitude, reply_markup=None):
        url = self.base_url + "sendLocation"
        params = {"chat_id": chat_id, "latitude": latitude, "longitude": longitude}
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                return await response.json()

    async def send_animation(self, chat_id, animation, caption=None, reply_markup=None):
        url = self.base_url + "sendAnimation"
        params = {"chat_id": chat_id, "animation": animation}
        if caption:
            params["caption"] = caption
        if reply_markup:
            params["reply_markup"] = json.dumps(reply_markup)
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
                        for handler in decorator.media_handlers:
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

class ContentType:
    photo = "photo"
    video = "video"
    music = "audio"
    file = "document"
    voice = "voice"
    cvm = "video_note"
    sticker = "sticker"
    animation = "animation"
    location = "location"
    media = {photo, video, music, file, voice, cvm, sticker, animation, location}

class F:
    @staticmethod
    def text(value):
        return lambda message: message.text == value

    @staticmethod
    def from_user_id(user_id):
        return lambda message: message.from_user and message.from_user.id == user_id

    @staticmethod
    def chat_type(chat_type):
        return lambda message: message.message_data["chat"]["type"] == chat_type

    @staticmethod
    def data(value):
        return lambda callback_query: callback_query.data == value

    @staticmethod
    def contains(value):
        return lambda message: value in message.text

    @staticmethod
    def startswith(value):
        return lambda message: message.text.startswith(value)

class Decorator:
    def __init__(self, bot):
        self.bot = bot
        self.handlers = []
        self.callback_handlers = []
        self.text_handlers = []
        self.media_handlers = []

    def handler(self, command=None, filter=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(message):
                if command is None or message.text.startswith(command):
                    if filter is None or filter(message):
                        await func(message)
            self.handlers.append(wrapper)
            return wrapper
        return decorator

    def callback(self, condition=None, filter=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(callback_query, bot):
                if condition is None or condition(CallbackQuery(callback_query, bot)):
                    if filter is None or filter(callback_query):
                        await func(CallbackQuery(callback_query, bot))
            self.callback_handlers.append(wrapper)
            return wrapper
        return decorator

    def text(self, condition=None, filter=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(message):
                if condition is None or condition(message):
                    if filter is None or filter(message):
                        await func(message)
            self.text_handlers.append(wrapper)
            return wrapper
        return decorator

    def media_handler(self, content_type=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(message):
                if message.content_type != "text" and (content_type is None or message.content_type == content_type):
                    await func(message)
            self.media_handlers.append(wrapper)
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
        self.from_user = User(message_data.get("from", {})) if "from" in message_data else None

        self.content_type = None
        self.photo = None
        self.video = None
        self.audio = None
        self.document = None
        self.voice = None
        self.video_note = None
        self.sticker = None
        self.animation = None
        self.location = None
        
        if "photo" in message_data:
            self.content_type = ContentType.photo
            self.photo = message_data["photo"]
        elif "video" in message_data:
            self.content_type = ContentType.video
            self.video = message_data["video"]
        elif "audio" in message_data:
            self.content_type = ContentType.music
            self.audio = message_data["audio"]
        elif "document" in message_data:
            self.content_type = ContentType.file
            self.document = message_data["document"]
        elif "voice" in message_data:
            self.content_type = ContentType.voice
            self.voice = message_data["voice"]
        elif "video_note" in message_data:
            self.content_type = ContentType.cvm
            self.video_note = message_data["video_note"]
        elif "sticker" in message_data:
            self.content_type = ContentType.sticker
            self.sticker = message_data["sticker"]
        elif "animation" in message_data:
            self.content_type = ContentType.animation
            self.animation = message_data["animation"]
        elif "location" in message_data:
            self.content_type = ContentType.location
            self.location = message_data["location"]
        elif "text" in message_data:
            self.content_type = "text"

    async def send(self, text, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        elif isinstance(reply_markup, InlineButton):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_message(
            self.chat_id,
            text,
            reply_markup=reply_markup,
        )

    async def reply(self, text, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        elif isinstance(reply_markup, InlineButton):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_message(
            self.chat_id,
            text,
            reply_markup=reply_markup,
        )

    async def send_photo(self, photo, caption=None, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_photo(self.chat_id, photo, caption, reply_markup)

    async def send_video(self, video, caption=None, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_video(self.chat_id, video, caption, reply_markup)

    async def send_audio(self, audio, caption=None, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_audio(self.chat_id, audio, caption, reply_markup)

    async def send_document(self, document, caption=None, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_document(self.chat_id, document, caption, reply_markup)

    async def send_voice(self, voice, caption=None, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_voice(self.chat_id, voice, caption, reply_markup)

    async def send_video_note(self, video_note, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_video_note(self.chat_id, video_note, reply_markup)

    async def send_sticker(self, sticker, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_sticker(self.chat_id, sticker, reply_markup)

    async def send_media_group(self, media):
        return await self.bot.send_media_group(self.chat_id, media)

    async def send_location(self, latitude, longitude, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_location(self.chat_id, latitude, longitude, reply_markup)

    async def send_animation(self, animation, caption=None, reply_markup=None):
        if isinstance(reply_markup, (InlineMarkup, ReplyMarkup)):
            reply_markup = reply_markup.to_dict()
        return await self.bot.send_animation(self.chat_id, animation, caption, reply_markup)

class User:
    def __init__(self, user_data):
        self.user_data = user_data
        self.id = user_data.get("id")
        self.first_name = user_data.get("first_name", "")
        self.last_name = user_data.get("last_name", "")
        self.username = user_data.get("username", "")
        self.language_code = user_data.get("language_code", "")

    @property
    def mention(self):
        if self.username:
            return f"@{self.username}"
        elif self.first_name:
            return f"[{self.first_name}](tg://user?id={self.id})"
        else:
            return print("Unknown parameter for user(check your code)")

    def __str__(self):
        return self.mention

