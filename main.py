import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
from pyrogram.enums import ChatAction
import google.generativeai as genai

API_ID = 12345678  # place your ID
API_HASH = "Your_Hash" # place your hash
GEMINI_KEY = "Your_KEY_Google" # place your key
WHITELIST = [1234567890]  # Whitelist only to reply for next chats

STICKER_MAP = {
    "Затруднительно": "CAACAgIAAxkBAAEDQUBpf2pWz3wfqXC9eXXZGbJ0tlbCcQACjokAAjsAAblJ1sMFg54BBSgeBA",
    "Под вопросом": "CAACAgIAAxkBAAEDQUJpf2paeqlGx_p5b8QDJNyhOtQoKQACQYkAAiWMuUmw7_NrGPrOAAEeBA",
    "Неубедительно": "CAACAgIAAxkBAAEDQURpf2pc6mCV-Vic2KVn0xNy62TiZgACO4oAAkEeuEm7czaNiZujcR4E",
    "Ошибочное мнение": "CAACAgIAAxkBAAEDQUZpf2pdgHYedbJGkE7fEJ7D6gjFHgACmJwAAnVBwUnc8nGOe-rUGB4E",
    "Далеко от истины": "CAACAgIAAxkBAAEDQUhpf2phiNvlwZxXBTFQkbamUvyb1AACX48AAj01uUl3zMO6cL91kB4E",
    "Не": "CAACAgIAAxkBAAEDQUppf2pif4pyVXbytbwOePWikd1y_QACJIUAAvz-uUkZj404lbs0bx4E",
    "Вряд ли": "CAACAgIAAxkBAAEDQUxpf2pjKviIZ2C5kdCVRYFpBFms6wAC9o0AAiokuEmjLKbyyJDFqh4E",
    "50 на 50": "CAACAgIAAxkBAAEDQU5pf2pkKxBzEkV35czKNVsHepd9NAACgYYAAqD-uUnfSjOOVqGFyx4E",
    "Бывает": "CAACAgIAAxkBAAEDQVBpf2pmC_kKs5tBLI7_nH6wQUm6cQACIYkAArGAuEkvqIAAAT3WcLgeBA",
    "Не факт": "CAACAgIAAxkBAAEDQVJpf2pna0rtVYCLOkyLmluI-qaVWwACSoMAAjLNuEmdfrz1u1eFIx4E",
    "Не уверен": "CAACAgIAAxkBAAEDQVRpf2pon20cKJWiGEjQl3U_YpNp5QACkpcAAps-sElVd0T07vtsZx4E",
    "Хммм": "CAACAgIAAxkBAAEDQVZpf2ppxf4BsuJ_jd0AARsb_Qjn5a0AAhiLAAINDrlJPkbPLi7NYa0eBA",
    "Спорно": "CAACAgIAAxkBAAEDQVhpf2pq2IKZ9zzSiIhCIrM54ffwIgAC1pEAAuiGuUmppEyx14k_LR4E",
    "Потужно": "CAACAgIAAxkBAAEDQVppf2psG9joOgxbWZvD8xMoLM-MhAACdZIAAskMuEkIfORYZcmCgx4E",
    "Отрицаю": "CAACAgIAAxkBAAEDQVxpf2pton7WHH93Pu4Nsmm8VPLl7gACjo0AAtQluUlD74kHsTU_ex4E",
    "Едва ли": "CAACAgIAAxkBAAEDQV5pf2pu-6ntCLTLTDMl6IPF-fZeAgACG5IAAnTiyUkHOOLub53gjR4E",
    "not sure twin": "CAACAgIAAxkBAAEDQWBpf2pv9EeXs9uWKEjUCtjPLoq8CAACWpQAAsyryUmdl85KDQ677x4E",
    "Нет": "CAACAgIAAxkBAAEDQWJpf2p3O16adjydX7NGyCfyp4witwACXpEAAszDyEk9jx0AASAdtn4eBA",
    "Неа": "CAACAgIAAxkBAAEDQWRpf2p4JIX60WtTlcTWn9KgXHsnBAACh4EAAgfgyUlEDWRgvGV5yB4E"
}
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=(
        "Ты — саркастичный скептик. Выбери ИДЕАЛЬНУЮ реакцию на сообщение "
        "ТОЛЬКО из этого списка. Не пиши ничего своего. "
        f"Список фраз: {', '.join(STICKER_MAP.keys())}"
    )
)

chat_sessions = {}
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.private & ~filters.me)
async def handle_message(client, message):
    if message.chat.id not in WHITELIST: return
    if not message.text: return

    chat_id = message.chat.id

    try:
        await client.send_chat_action(chat_id, ChatAction.CHOOSE_STICKER)
        await asyncio.sleep(1)

        if chat_id not in chat_sessions:
            chat_sessions[chat_id] = model.start_chat(history=[])

        current_chat = chat_sessions[chat_id]

        response = await current_chat.send_message_async(message.text)
        ai_phrase = response.text.strip()

        sticker_found = False
        for phrase, file_id in STICKER_MAP.items():
            if phrase.lower() in ai_phrase.lower():
                if file_id != "ВСТАВЬ_КОД_СЮДА":
                    await message.reply_sticker(file_id)
                    sticker_found = True
                break

        if not sticker_found:
            await message.reply_text(ai_phrase)

    except Exception:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Lets Get it.")
    app.run()