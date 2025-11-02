import re
import asyncio
from telethon import TelegramClient, events

# ======================
# ⚙️ Telegram API ma'lumotlari
# ======================
API_ID = 25545982
API_HASH = "adf731033d9de2faafbbcdb2bfa519a9"
PHONE_NUMBER = "+998919498281"
PAYMENT_GROUP_ID = -1002757804832
CARD_BOT_USERNAME = "CardXabarBot"

# Telegram sessiya fayli
client = TelegramClient('card_session', API_ID, API_HASH)

# ======================
# 💳 Xabardan to‘lov ma’lumotini ajratish
# ======================
def extract_payment_info(text: str):
    if not text:
        return None
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

# ======================
# 📥 Karta botidan kelgan xabarlarni kuzatish
# ======================
@client.on(events.NewMessage(from_users=CARD_BOT_USERNAME))
async def card_message_handler(event):
    try:
        payment = extract_payment_info(event.message.message)
        if not payment:
            return

        await client.send_message(
            PAYMENT_GROUP_ID,
            f"PAYMENT|{payment['amount']}|{payment['card_last4']}"
        )
    except:
        pass  # ❌ Hech qanday xato terminalga chiqmaydi

# ======================
# 🌀 Ishga tushirish
# ======================
async def main():
    try:
        await client.get_entity(PAYMENT_GROUP_ID)
    except:
        pass  # Guruh yuklanmasa ham bot ishlaydi

    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        client.start(PHONE_NUMBER)
        client.loop.run_until_complete(main())
    except:
        pass  # ❌ Har qanday xato terminalga chiqmaydi