from telebot import TeleBot, types

bot = TeleBot("8293611697:AAEDpkamKQE1ebbqkM3CerjffFxMKAh93Cc")

REQUIRED_CHANNELS = ["https://t.me/SR_Technology7", "@SR_Technology7"]

def check_membership(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_membership(user_id):
        bot.send_message(message.chat.id, "✅ Access granted! Welcome to EarnHub.")
    else:
        markup = types.InlineKeyboardMarkup()
        for ch in REQUIRED_CHANNELS:
            markup.add(types.InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch[1:]}"))
        markup.add(types.InlineKeyboardButton("✅ I've Joined", callback_data="check_join"))
        bot.send_message(message.chat.id, "🚫 To use this bot, please join all channels below:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def recheck(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.edit_message_text("✅ Thanks for joining! Now you can use the bot.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "❌ You haven't joined all required channels.")
