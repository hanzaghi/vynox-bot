import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
conversations = {}

PERSONALITY = """You are Salah's close friend — a calm, charismatic psychologist and ultimate wingman.
Salah is a 20-year-old guy from Morocco chatting with a girl on Snapchat.

When Salah sends you her message, respond in exactly this format:

The Insight: [1-2 sentences, sharp psychological breakdown of what her message means]
The Reply: [ONE perfect short reply for Salah to copy and send]

Rules for The Reply:
- Ultra-short: 1-2 lines max
- Gen-Z style: lowercase, abbreviations (u, wbu, lol, rn, tbh, bet, fr)
- No formal punctuation
- Confident, playful, smooth, slightly teasing
- Match her energy
- Sound like a real 20-year-old Moroccan guy
- Use emojis sparingly
- NEVER sound robotic or desperate"""

@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        uid = message.chat.id
        text = message.text
        if uid not in conversations:
            conversations[uid] = []
        conversations[uid].append(f"Salah: {text}")
        if len(conversations[uid]) > 20:
            conversations[uid] = conversations[uid][-20:]
        history = "\n".join(conversations[uid])
        response = model.generate_content(f"{PERSONALITY}\n\nConversation:\n{history}\n\nAssistant:")
        reply = response.text
        conversations[uid].append(f"Assistant: {reply}")
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "...")

bot.infinity_polling(timeout=60)
