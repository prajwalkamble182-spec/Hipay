import logging
import os
import threading
import json
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- FLASK (Render Web Service Keep-Alive 24/7) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
BOT_TOKEN = "8945239395:AAF8VDs0pLF44yv7qUY3I0Q0QK7p2x6WRwo" 
ADMIN_CHAT_ID = 6119216457
MANAGER_HANDLE = "@HerryO23"
USERS_FILE = "users.json"

# LINKS
REGISTER_URL = "https://h5.hipayus.com/#/register?u_userlink=OW7MNH9I" 
DOWNLOAD_URL = "https://app.hipayus.com/?app=HiPay&utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAb21jcAToIJtwZG9mAmV4dG4DYWVtAjExAHNydGMGYXBwX2lkDzU2NzA2NzM0MzM1MjQyNwABpxuMmYix_F3JC9u2oBc-DOxseNpXQDOATExDMFM0o_tUVhzuiPsAgzVnqvSl_aem_y-qIgawYG-sRerOk8uYm3g"
CHANNEL_URL = "https://t.me/CBRETURN0" 

# VIDEO LINKS & FILE IDs
REG_VIDEO_URL = "https://t.me/CBRETURN0/258"
BIND_VIDEO_URL = "https://t.me/CBRETURN0/259"
BUY_SELL_VIDEO_ID = "BAACAgUAAxkBAAEtipNqfrYvQm9g7VlVr--jwd7Vnyl-nwAChBoAAgqH-FcuJeBYE-9ijT0E"

# 🎁 HIGH-QUALITY REWARDS PHOTO DIRECT LINK
REWARDS_PHOTO_URL = "https://i.ibb.co/GQRmNm92/image.jpg"

# --- USER STORAGE (FOR BROADCAST) ---
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.add(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(list(users), f)

# --- START / WELCOME HANDLER ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)  # Auto save for broadcast

    keyboard = [
        [InlineKeyboardButton("📢 Join Official Telegram Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("📝 Register Hipay Now", url=REGISTER_URL),
         InlineKeyboardButton("📥 Download Hipay App", url=DOWNLOAD_URL)],
        [InlineKeyboardButton("🔗 Bind Wallet Now", url=REGISTER_URL)],
        [InlineKeyboardButton("📹 Registration Video", url=REG_VIDEO_URL),
         InlineKeyboardButton("📹 Wallet Bind Video", url=BIND_VIDEO_URL)],
        [InlineKeyboardButton("📹 Buy / Sell Video", callback_data='video_buysell')],
        [InlineKeyboardButton("📊 Commission & Rates", callback_data='rates'),
         InlineKeyboardButton("🎁 Rewards Info", callback_data='rewards')],
        [InlineKeyboardButton("💬 Talk to Manager", callback_data='contact_manager')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"👋 **Welcome {user.first_name} to Hipay Automated Bot!**\n\n"
        "⚡ **Platform Features & Tutorial Guides:**\n"
        "• Latest updates ke liye hamara Official Telegram Channel join karein.\n"
        "• Registration, App Download aur Wallet Bind ke links niche hain.\n"
        "• Instant ₹100 Bonus on 1st Wallet Bind | Up to 3.2% Commission\n\n"
        "Niche kisi bhi option par click karein:"
    )
    
    if update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# --- BUTTON HANDLER ---
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    back_button = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]

    if query.data == 'video_buysell':
        await query.message.reply_video(video=BUY_SELL_VIDEO_ID, caption="📹 **Buy / Sell Trading Video**", reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == 'rates':
        await query.message.reply_text("📊 **Commission Rates:** 3.2% Per Deal | USDT Rate: 107+ INR", reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == 'rewards':
        rewards_caption = (
            "🎁 **HIPAY EXCLUSIVE REWARDS & BONUSES** 🎁\n\n"
            "💰 **1st Wallet Bind:** ₹100 Instant Bonus\n"
            "🔥 **Up to 6 Wallets Bind:** ₹600 Total Rewards\n"
            "📈 **Trading Profit:** Earn Up to 3.2% Commission per deal\n\n"
            "⚡ *Abhi Register aur Wallet bind karke apna bonus claim karein!*"
        )
        try:
            # Send HD Photo directly
            await query.message.reply_photo(
                photo=REWARDS_PHOTO_URL, 
                caption=rewards_caption, 
                parse_mode='Markdown', 
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        except Exception:
            await query.message.reply_text(
                rewards_caption, 
                parse_mode='Markdown', 
                reply_markup=InlineKeyboardMarkup(back_button)
            )
    elif query.data == 'contact_manager':
        context.user_data['waiting_for_support'] = True
        await query.message.reply_text(f"✍️ **Manager Support Mode Active:**\n\nApni pareshani ya sawal yahan likhkar bhejein.\nAap direct Manager {MANAGER_HANDLE} se connect ho jayenge.")
    elif query.data == 'main_menu':
        await start(update, context)

# --- ADMIN BROADCAST HANDLER ---
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ **Format:** `/broadcast Aapka message yahan`", parse_mode='Markdown')
        return

    message_to_send = " ".join(context.args)
    users = load_users()
    sent_count = 0

    await update.message.reply_text(f"📢 Broadcasting to {len(users)} users...")

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 **IMPORTANT ANNOUNCEMENT:**\n\n{message_to_send}", parse_mode='Markdown')
            sent_count += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ **Broadcast Done!**\nDelivered to: `{sent_count}/{len(users)}` users.", parse_mode='Markdown')

# --- LIVE MANAGER SUPPORT HANDLER ---
async def handle_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Manager Admin Reply Logic
    if update.effective_user.id == ADMIN_CHAT_ID and update.message.reply_to_message:
        try:
            orig_text = update.message.reply_to_message.text
            user_id = int(orig_text.split("User ID:** `")[1].split("`")[0])
            await context.bot.send_message(chat_id=user_id, text=f"💬 **Manager Reply ({MANAGER_HANDLE}):**\n\n{update.message.text}")
            await update.message.reply_text("✅ Reply bhej diya gaya hai!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
        return

    # User Support Mode Logic
    if context.user_data.get('waiting_for_support'):
        user = update.effective_user
        admin_notification = f"📩 **NEW MESSAGE FOR MANAGER ({MANAGER_HANDLE})!**\n\n👤 **From:** {user.first_name} (@{user.username})\n🆔 **User ID:** `{user.id}`\n\n💬 **Message:** {update.message.text}\n\n*(Is message ka 'Reply' karke jawab likhein)*"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notification, parse_mode='Markdown')
        await update.message.reply_text(f"✅ Aapka message Manager ({MANAGER_HANDLE}) ko mil gaya hai! Hum jald hi reply karenge.")
        context.user_data['waiting_for_support'] = False

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("broadcast", broadcast))
    app_bot.add_handler(CallbackQueryHandler(button_click))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_messages))
    
    app_bot.run_polling()
