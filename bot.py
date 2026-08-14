import logging
import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Flask Setup (To keep the bot alive on Render Web Service)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
BOT_TOKEN = "8945239395:AAF8VDs0pLF44yv7qUY3I0Q0QK7p2x6WRwo" 
ADMIN_CHAT_ID = 6119216457
MANAGER_HANDLE = "@HerryO23"

# LINKS
REGISTER_URL = "https://h5.hipayus.com/#/register?u_userlink=OW7MNH9I" 
DOWNLOAD_URL = "https://app.hipayus.com/?app=HiPay&utm_source=ig&utm_medium=social&utm_content=link_in_bio&fbclid=PAb21jcAToIJtwZG9mAmV4dG4DYWVtAjExAHNydGMGYXBwX2lkDzU2NzA2NzM0MzM1MjQyNwABpxuMmYix_F3JC9u2oBc-DOxseNpXQDOATExDMFM0o_tUVhzuiPsAgzVnqvSl_aem_y-qIgawYG-sRerOk8uYm3g"
CHANNEL_URL = "https://t.me/CBRETURN0" 

# FILE IDs
REGISTRATION_VIDEO_ID = "BAACAgUAAxkBAAEtio1qfrXByZp2B6hw0tMU8VfBYIhqUwACgiMAAt_g8Vcd4OeB13MU1j0E"
WALLET_BIND_VIDEO_ID = "BAACAgUAAxkBAAEtio9qfrYZrHfwsruvhcEVL4NT5ZO6fAAChCMAAt_g8VdTtE-MjffbZz0E"
BUY_SELL_VIDEO_ID = "BAACAgUAAxkBAAEtipNqfrYvQm9g7VlVr--jwd7Vnyl-nwAChBoAAgqH-FcuJeBYE-9ijT0E"
REWARDS_PHOTO_ID = "AgACAgUAAxkBAAEtistqfr2d3EmTEx5uG3bgjn-YLFk6VAAC5BRrG2Zq2VdXQqp2O1VacQEAAwIAA3kAAz0E"

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("📝 Register", url=REGISTER_URL), InlineKeyboardButton("📥 Download", url=DOWNLOAD_URL)],
        [InlineKeyboardButton("🔗 Bind Wallet", url=REGISTER_URL)],
        [InlineKeyboardButton("📹 Registration Video", callback_data='video_reg'), InlineKeyboardButton("📹 Wallet Bind Video", callback_data='video_bind')],
        [InlineKeyboardButton("📹 Buy / Sell Video", callback_data='video_buysell')],
        [InlineKeyboardButton("📊 Rates", callback_data='rates'), InlineKeyboardButton("🎁 Rewards", callback_data='rewards')],
        [InlineKeyboardButton("💬 Talk to Manager", callback_data='contact_manager')]
    ]
    await update.message.reply_text("👋 Welcome to Hipay Bot! Select an option:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    back = [[InlineKeyboardButton("⬅️ Back", callback_data='main_menu')]]
    
    if query.data == 'video_reg': await query.message.reply_video(REGISTRATION_VIDEO_ID, reply_markup=InlineKeyboardMarkup(back))
    elif query.data == 'video_bind': await query.message.reply_video(WALLET_BIND_VIDEO_ID, reply_markup=InlineKeyboardMarkup(back))
    elif query.data == 'video_buysell': await query.message.reply_video(BUY_SELL_VIDEO_ID, reply_markup=InlineKeyboardMarkup(back))
    elif query.data == 'rates': await query.edit_message_text("📊 Rates: 3.2% Profit | USDT: 107+", reply_markup=InlineKeyboardMarkup(back))
    elif query.data == 'rewards': await query.message.reply_photo(REWARDS_PHOTO_ID, caption="🎁 Rewards: 1st Bind ₹100, Total ₹600", reply_markup=InlineKeyboardMarkup(back))
    elif query.data == 'contact_manager': 
        context.user_data['support'] = True
        await query.message.reply_text("✍️ Support Mode Active. Message likhein.")
    elif query.data == 'main_menu': await start(update, context)

if __name__ == '__main__':
    # Start Flask in background
    threading.Thread(target=run_flask).start()
    
    # Start Telegram Bot
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button_click))
    app_bot.run_polling()
    
