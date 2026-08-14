import logging
import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- FLASK (Render Web Service Keep-Alive) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
BOT_TOKEN = "8945239395:AAF8VDs0pLF44yv7qUY3I0Q0QK7p2x6WRwo" 
ADMIN_CHAT_ID = 6119216457
MANAGER_HANDLE = "@HerryO23"

# LINKS
REGISTER_URL = "https://h5.hipayus.com/#/register?u_userlink=OW7MNH9I" 
DOWNLOAD_URL = "https://app.hipayus.com/?app=HiPay&utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAb21jcAToIJtwZG9mAmV4dG4DYWVtAjExAHNydGMGYXBwX2lkDzU2NzA2NzM0MzM1MjQyNwABpxuMmYix_F3JC9u2oBc-DOxseNpXQDOATExDMFM0o_tUVhzuiPsAgzVnqvSl_aem_y-qIgawYG-sRerOk8uYm3g"
CHANNEL_URL = "https://t.me/CBRETURN0" 

# DIRECT TELEGRAM CHANNEL VIDEO LINKS (100% Working)
REG_VIDEO_URL = "https://t.me/CBRETURN0/258"
BIND_VIDEO_URL = "https://t.me/CBRETURN0/259"
BUY_SELL_VIDEO_ID = "BAACAgUAAxkBAAEtipNqfrYvQm9g7VlVr--jwd7Vnyl-nwAChBoAAgqH-FcuJeBYE-9ijT0E"

# 🎁 UPDATED REWARDS PHOTO FILE ID
REWARDS_PHOTO_ID = "AgACAgUAAxkBAAEtistqfr2d3EmTEx5uG3bgjn-YLFk6VAAC5BRrG2Zq2VdXQqp2O1VacQEAAwIAA3kAAz0E"

# --- MAIN MENU ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    
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
        f"👋 **Welcome {user_name} to Hipay Automated Bot!**\n\n"
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

# --- BUTTON CLICK HANDLER ---
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    back_button = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]

    if query.data == 'video_buysell':
        await query.message.reply_video(video=BUY_SELL_VIDEO_ID, caption="📹 **Buy / Sell Trading Video**", reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == 'rates':
        await query.edit_message_text("📊 **Commission Rates:** 3.2% Per Deal | USDT Rate: 107+ INR", reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == 'rewards':
        rewards_caption = (
            "🎁 **HIPAY EXCLUSIVE REWARDS & BONUSES** 🎁\n\n"
            "💰 **1st Wallet Bind:** ₹100 Instant Bonus\n"
            "🔥 **Up to 6 Wallets Bind:** ₹600 Total Rewards\n"
            "📈 **Trading Profit:** Earn Up to 3.2% Commission per deal\n\n"
            "⚡ *Abhi Register aur Wallet bind karke apna bonus claim karein!*"
        )
        await query.message.reply_photo(
            photo=REWARDS_PHOTO_ID, 
            caption=rewards_caption, 
            parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup(back_button)
        )
    elif query.data == 'contact_manager':
        context.user_data['waiting_for_support'] = True
        await query.message.reply_text(f"✍️ **Manager Support Mode Active:**\n\nApni pareshani ya sawal yahan likhkar bhejein.\nAap direct Manager {MANAGER_HANDLE} se connect ho jayenge.")
    elif query.data == 'main_menu':
        await start(update, context)

# --- USER TEXT MESSAGES & MANAGER SUPPORT ---
async def handle_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Manager Reply to User
    if update.effective_user.id == ADMIN_CHAT_ID and update.message.reply_to_message:
        try:
            orig_text = update.message.reply_to_message.text
            user_id = int(orig_text.split("User ID:** `")[1].split("`")[0])
            await context.bot.send_message(chat_id=user_id, text=f"💬 **Manager Reply ({MANAGER_HANDLE}):**\n\n{update.message.text}")
            await update.message.reply_text("✅ Reply bhej diya gaya hai!")
        except Exception as e:
            await update.message.reply_text(f"❌ Reply bhejne me error aaya: {e}")
        return

    # User send to Manager
    if context.user_data.get('waiting_for_support'):
        user = update.effective_user
        admin_notification = f"📩 **NEW MESSAGE FOR MANAGER ({MANAGER_HANDLE})!**\n\n👤 **From:** {user.first_name} (@{user.username})\n🆔 **User ID:** `{user.id}`\n\n💬 **Message:** {update.message.text}\n\n*(Is message ka 'Reply' karke jawab likhein)*"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notification, parse_mode='Markdown')
        await update.message.reply_text(f"✅ Aapka message Manager ({MANAGER_HANDLE}) ko mil gaya hai! Hum jald hi reply karenge.")
        context.user_data['waiting_for_support'] = False

if __name__ == '__main__':
    # Start Flask Server
    threading.Thread(target=run_flask).start()
    
    # Start Telegram Bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_messages))
    
    app.run_polling()
    
# Iss
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        print(f"--- FOTO ID: {file_id} ---")
        await update.message.reply_text(f"✅ Photo ID mil gayi: `{file_id}`", parse_mode='Markdown')

# app.run_polling() se pehle ye line add karein
app.add_handler(MessageHandler(filters.PHOTO, get_id))
