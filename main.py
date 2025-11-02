import re
import asyncio
import threading
from telethon import TelegramClient, events
from flask import Flask

# 🔑 Telegram API sozlamalari
API_ID = 25545982
API_HASH = "adf731033d9de2faafbbcdb2bfa519a9"
PHONE_NUMBER = "+998919498281"  # @CardXabarBot xabar yuboradigan raqamingiz

# 📥 Guruh ID (manfiy son)
PAYMENT_GROUP_ID = -1002757804832

# Telegram sessiyasi
client = TelegramClient('card_session', API_ID, API_HASH)

# 🌐 Flask web server (UptimeRobot uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Card UserBot ishlayapti!", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Guruhni oldindan yuklash
async def preload_group():
    try:
        await client.get_entity(PAYMENT_GROUP_ID)
    except:
        pass  # Guruh topilmasa ham xatoni ko‘rsatmaydi

# Xabardan summa va karta oxirini ajratish
def extract_payment_info(text: str):
    sum_match = re.search(r'➕\s*([\d\s,\.]+)\s*UZS', text)
    if not sum_match:
        return None
    raw_sum = sum_match.group(1).replace(" ", "").replace(",", "")
    try:
        amount = int(float(raw_sum))
    except:
        return None
    card_match = re.search(r'💳\s*\*{3}(\d{4})', text)
    card_last4 = card_match.group(1) if card_match else "0000"
    return {"amount": amount, "card_last4": card_last4}

# CardXabarBot xabarlarini kuzatish
@client.on(events.NewMessage(from_users='CardXabarBot'))
async def handler(event):
    payment = extract_payment_info(event.message.message)
    if payment:
        try:
            await client.send_message(
                PAYMENT_GROUP_ID,
                f"PAYMENT|{payment['amount']}|{payment['card_last4']}"
            )
        except:
            pass  # Xatolar butunlay yashiriladi

# Ishga tushirish
print("🔄 UserBot ishga tushmoqda...")

def start_bot():
    try:
        client.start(PHONE_NUMBER)
        client.loop.run_until_complete(preload_group())
        client.run_until_disconnected()
    except:
        pass  # Terminalga hech narsa chiqmaydi

# Flask va Telethonni bir vaqtda ishga tushirish
threading.Thread(target=run_flask, daemon=True).start()
start_bot()
