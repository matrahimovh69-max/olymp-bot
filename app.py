 import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токенни Railway'даги Variables'дан олиш
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# /start буйруғи учун асосий меню
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("9-синф", callback_data="class_9"),
        InlineKeyboardButton("10-синф", callback_data="class_10"),
        InlineKeyboardButton("11-синф", callback_data="class_11")
    )
    bot.send_message(
        message.chat.id,
        "Ассалому алайкум! Рус тили ва адабиёти олимпиадаси ботига хуш келибсиз.\nИлтимос, синфингизни танланг:",
        reply_markup=markup
    )

# Тугмалар босилганда ишлайдиган қисм
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "class_9":
        bot.send_message(
            call.message.chat.id, 
            "📚 **9-синф олимпиада тестлари:**\n\nБу ерга 9-синф тест саволлари ва вариантларини жойлаштиришингиз мумкин."
        )
    elif call.data == "class_10":
        bot.send_message(
            call.message.chat.id, 
            "📚 **10-синф олимпиада тестлари:**\n\nБу ерга 10-синф тест саволлари ва вариантларини жойлаштиришингиз мумкин."
        )
    elif call.data == "class_11":
        bot.send_message(
            call.message.chat.id, 
            "📚 **11-синф олимпиада тестлари:**\n\nБу ерга 11-синф тест саволлари ва вариантларини жойлаштиришингиз мумкин."
        )

if __name__ == "__main__":
    print("Бот ишга тушди...")
    bot.infinity_polling()
