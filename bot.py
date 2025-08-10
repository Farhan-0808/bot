
from telethon import TelegramClient, events, Button
import re

# ==== TELEGRAM API ====
api_id = 29000589
api_hash = '400f8c83f38bc8be898a3c99136986f3'

# ==== CHANNEL / GROUP SETUP ====
file_source = -1002739980245         # File Channel
file_forward_to = -1002195476761     # Your Channel

otp_source = -1002881339479          # OTP Group
otp_forward_to = -1002791500688      # Your OTP Group

# ==== CUSTOM LINKS ====
your_group_link = "https://t.me/rctotp"
your_channel_link = "https://t.me/RctAdsEarning"

client = TelegramClient('user_forward_session', api_id, api_hash)

# ✅ 1. FILE FORWARDING (with caption cleaned)
@client.on(events.NewMessage(chats=file_source))
async def forward_file(event):
    if event.file:
        caption = event.raw_text or ""

        # Remove line containing "OTP : JOIN HERE" and telegram links/usernames
        lines = caption.splitlines()
        cleaned_lines = [
            re.sub(r'(@\w+|https?://t\.me/\S+|t\.me/\S+|telegram\.me/\S+)', '', line)  # 🔥 Only this line added
            for line in lines
            if "OTP : JOIN HERE" not in line
        ]
        cleaned_caption = "\n".join(cleaned_lines).strip()

        await client.send_file(
            file_forward_to,
            file=event.media,
            caption=cleaned_caption,
            buttons=[Button.url("🔐 OTP Group Join Here", your_group_link)]
        )

# ✅ 2. OTP FORWARDING (as before)
@client.on(events.NewMessage(chats=otp_source))
async def forward_otp(event):
    text = event.raw_text

    if re.search(r'\b(\d{4,8})\b', text):
        await client.send_message(
            otp_forward_to,
            message=text,
            buttons=[Button.url("📢 Main Channel", your_channel_link)]
        )

print("✅ Forwarding system is running...")
client.start()
client.run_until_disconnected()