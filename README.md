#  AutoSkeptic Userbot

**AutoSkeptic** is a smart Telegram userbot powered by **Google Gemini AI**. It automatically replies to messages with context-aware sarcastic stickers.

Instead of generating boring text, the bot analyzes the conversation context and selects the perfect reaction (e.g., "Doubtful", "Hardly", "No way") from a curated sticker set.

---

##  How It Works

1.  **Monitoring:** The bot listens to incoming private messages (only from users in your "Whitelist").
2.  **AI Analysis:** The message text is sent to the **Google Gemini 1.5 Flash** model.
3.  **Decision Making:** Acting as a "Sarcastic Skeptic," the AI selects the most appropriate phrase from a predefined list.
4.  **Response:** The bot maps the selected phrase to a specific Telegram sticker and sends it back.

---

##  Tech Stack

* **Python 3.14**
* **[Pyrogram](https://docs.pyrogram.org/)** — An elegant Telegram Client Library.
* **[Google Generative AI](https://ai.google.dev/)** — API for accessing Gemini models.
