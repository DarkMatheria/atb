import asyncio
from atb.main.atb import *

API_TOKEN = "7597375886:AAGxEpXIc_PZxVYprI0Tui2ClWfxsNkhJzU"

bot = Bot(API_TOKEN)
decorator = Decorator(bot)

@decorator.handler("/start")
async def start_handler(message):
    keyboard = InlineMarkup(row=2)
    button1 = InlineButton("📸 Photo", "send_photo")
    button2 = InlineButton("🎥 Video", "send_video")
    button3 = InlineButton("🎵 Audio", "send_audio")
    button4 = InlineButton("📄 Document", "send_document")
    button5 = InlineButton("🎤 Voice", "send_voice")
    button6 = InlineButton("📹 Video Note", "send_video_note")
    button7 = InlineButton("😄 Sticker", "send_sticker")
    button8 = InlineButton("🎬 Animation", "send_animation")
    button9 = InlineButton("📍 Location", "send_location")
    button10 = InlineButton("📋 Media Group", "send_media_group")
    button11 = InlineButton("⌨️ Keyboard", "show_keyboard")
    button12 = InlineButton("🌐 Web App", url="https://example.com", miniapp=True)
    keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12)
    await message.send(f"Hello, {message.from_user.first_name}! Choose an action:", reply_markup=keyboard)

@decorator.handler("/help")
async def help_handler(message):
    help_text = "Available commands:\n/start - Main menu\n/help - Help\n/info - User info\n/keyboard - Reply keyboard\n/media_group - Send media group"
    await message.reply(help_text)

@decorator.handler("/info")
async def info_handler(message):
    user_info = (
        f"ID: {message.from_user.id}\n"
        f"First name: {message.from_user.first_name}\n"
        f"Last name: {message.from_user.last_name}\n"
        f"Username: {message.from_user.username}\n"
        f"Language: {message.from_user.language_code}\n"
        f"Mention: {message.from_user.mention}"
    )
    await message.send(user_info)

@decorator.handler("/keyboard")
async def keyboard_handler(message):
    keyboard = ReplyMarkup(row=2, resize_keyboard=True, one_time_keyboard=False)
    button1 = ReplyButton("Regular Button")
    button2 = ReplyButton("Contact", request_contact=True)
    button3 = ReplyButton("Location", request_location=True)
    button4 = ReplyButton("Remove Keyboard")
    keyboard.add(button1, button2, button3, button4)
    await message.send("Reply keyboard:", reply_markup=keyboard)

@decorator.text(F.text("Regular Button"))
async def normal_button_handler(message):
    await message.send("You pressed the regular button!")

@decorator.text(F.text("Remove Keyboard"))
async def remove_keyboard_handler(message):
    await message.send("Keyboard removed")

@decorator.text(F.contains("hello"))
async def greeting_handler(message):
    await message.send("Hello to you too!")

@decorator.text(F.startswith("/custom"))
async def custom_command_handler(message):
    await message.send("Custom command!")

@decorator.text(F.from_user_id(123456789))
async def specific_user_handler(message):
    await message.send("This message is for a specific user")

@decorator.text(F.chat_type("private"))
async def private_chat_handler(message):
    await message.send("This is a private chat")

@decorator.media_handler("photo")
async def photo_handler(message):
    await message.send("📸 Photo received!")
    photo_file_id = message.photo[-1]["file_id"]
    await message.send_photo(photo_file_id, caption="Your photo")

@decorator.media_handler("video")
async def video_handler(message):
    await message.send("🎥 Video received!")
    video_file_id = message.video["file_id"]
    await message.send_video(video_file_id, caption="Your video")

@decorator.media_handler("audio")
async def audio_handler(message):
    await message.send("🎵 Audio received!")
    audio_file_id = message.audio["file_id"]
    await message.send_audio(audio_file_id, caption="Your audio")

@decorator.media_handler("document")
async def document_handler(message):
    await message.send("📄 Document received!")
    document_file_id = message.document["file_id"]
    await message.send_document(document_file_id, caption="Your document")

@decorator.media_handler("voice")
async def voice_handler(message):
    await message.send("🎤 Voice message received!")
    voice_file_id = message.voice["file_id"]
    await message.send_voice(voice_file_id)

@decorator.media_handler("video_note")
async def video_note_handler(message):
    await message.send("📹 Video note received!")
    video_note_file_id = message.video_note["file_id"]
    await message.send_video_note(video_note_file_id)

@decorator.media_handler("sticker")
async def sticker_handler(message):
    await message.send("😄 Sticker received!")
    sticker_file_id = message.sticker["file_id"]
    await message.send_sticker(sticker_file_id)

@decorator.media_handler("animation")
async def animation_handler(message):
    await message.send("🎬 Animation received!")
    animation_file_id = message.animation["file_id"]
    await message.send_animation(animation_file_id, caption="Your animation")

@decorator.media_handler("location")
async def location_handler(message):
    await message.send("📍 Location received!")
    latitude = message.location["latitude"]
    longitude = message.location["longitude"]
    await message.send_location(latitude, longitude)

@decorator.media_handler()
async def all_media_handler(message):
    await message.send(f"Received media of type: {message.content_type}")

@decorator.callback(F.data("send_photo"))
async def send_photo_callback(callback_query):
    photo_url = "https://via.placeholder.com/300x200.png?text=Test+Photo"
    await callback_query.message.send_photo(photo_url, caption="Test photo")
    await callback_query.answer("Photo sent!")

@decorator.callback(F.data("send_video"))
async def send_video_callback(callback_query):
    await callback_query.message.send("Send me a video!")
    await callback_query.answer("Waiting for video")

@decorator.callback(F.data("send_audio"))
async def send_audio_callback(callback_query):
    await callback_query.message.send("Send me audio!")
    await callback_query.answer("Waiting for audio")

@decorator.callback(F.data("send_document"))
async def send_document_callback(callback_query):
    await callback_query.message.send("Send me a document!")
    await callback_query.answer("Waiting for document")

@decorator.callback(F.data("send_voice"))
async def send_voice_callback(callback_query):
    await callback_query.message.send("Send me a voice message!")
    await callback_query.answer("Waiting for voice message")

@decorator.callback(F.data("send_video_note"))
async def send_video_note_callback(callback_query):
    await callback_query.message.send("Send me a circle video note!")
    await callback_query.answer("Waiting for video note")

@decorator.callback(F.data("send_sticker"))
async def send_sticker_callback(callback_query):
    await callback_query.message.send("Send me a sticker!")
    await callback_query.answer("Waiting for sticker")

@decorator.callback(F.data("send_animation"))
async def send_animation_callback(callback_query):
    await callback_query.message.send("Send me a GIF!")
    await callback_query.answer("Waiting for animation")

@decorator.callback(F.data("send_location"))
async def send_location_callback(callback_query):
    await callback_query.message.send_location(55.7558, 37.6176)
    await callback_query.answer("Moscow location sent!")

@decorator.callback(F.data("send_media_group"))
async def send_media_group_callback(callback_query):
    media_group = [
        {
            "type": "photo",
            "media": "https://via.placeholder.com/300x200.png?text=Photo+1",
            "caption": "First photo"
        },
        {
            "type": "photo",
            "media": "https://via.placeholder.com/300x200.png?text=Photo+2",
            "caption": "Second photo"
        }
    ]
    await callback_query.message.send_media_group(media_group)
    await callback_query.answer("Media group sent!")

@decorator.callback(F.data("show_keyboard"))
async def show_keyboard_callback(callback_query):
    keyboard = ReplyMarkup(row=1)
    button = ReplyButton("Test Button")
    keyboard.add(button)
    await callback_query.message.send("Here is a regular keyboard:", reply_markup=keyboard)
    await callback_query.answer("Keyboard shown")

@decorator.callback(lambda cq: cq.data.startswith("test_"))
async def test_callback_handler(callback_query):
    await callback_query.answer(f"Test callback: {callback_query.data}")

async def main():
    print("Bot started...")
    await bot.run(decorator)

if __name__ == "__main__":
    asyncio.run(main())

