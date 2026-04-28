import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
conversations = {}

PERSONALITY = """أنت شخص اسمك VYNOX، شاب عربي طبيعي بتكلم أصدقاءك على تيليجرام.
- كلم الناس بشكل طبيعي وغير رسمي
- استخدم نفس لغتهم
- ما تقول أبداً إنك AI أو بوت
- ردودك قصيرة مثل واتساب
- استخدم إيموجي بشكل طبيعي"""

@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        uid = message.chat.id
        text = message.text
        if uid not in conversations:
            conversations[uid] = []
        conversations[uid].append(f"User: {text}")
        if len(conversations[uid]) > 20:
            conversations[uid] = conversations[uid][-20:]
        history = "\n".join(conversations[uid])
        response = model.generate_content(f"{PERSONALITY}\n\nالمحادثة:\n{history}\n\nVYNOX:")
        reply = response.text
        conversations[uid].append(f"VYNOX: {reply}")
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "...")

bot.infinity_polling(timeout=60)
