import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from olympiad_db import OLYMPIAD_TESTS

# Бот токени
TOKEN = os.getenv("BOT_TOKEN", "TOKEN_INGIZNI_SHU_YERGA_YOZING")
bot = telebot.TeleBot(TOKEN)

# Фойдаланувчилар танловини вақтинча сақлаш
user_data = {}

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("class_"))
def select_class(call):
    class_num = call.data.split("_")[1]
    user_data[call.from_user.id] = {"class": class_num}
    
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("1-вариант", callback_data="var_1"),
        InlineKeyboardButton("2-вариант", callback_data="var_2")
    )
    bot.edit_message_text(
        f"Сиз {class_num}-синфни танладингиз.\nЭнди вариантни танланг:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("var_"))
def select_variant(call):
    var_num = call.data.split("_")[1]
    user_id = call.from_user.id
    
    if user_id not in user_data or "class" not in user_data[user_id]:
        bot.answer_callback_query(call.id, "Илтимос, аввал /start буйруғини босиб синфни танланг!")
        return
        
    class_num = user_data[user_id]["class"]
    tests = OLYMPIAD_TESTS.get(class_num, {}).get(f"variant_{var_num}", [])
    
    bot.answer_callback_query(call.id, "Тестлар юкланмоқда...")
    
    # Ҳар бир савол ва унинг вариантларини тугмалар билан чиқарамиз
    for item in tests:
        markup = InlineKeyboardMarkup()
        for opt in item["options"]:
            btn_text = opt[:3]  # Масалан: А), В) ва ҳ.к.
            markup.add(InlineKeyboardButton(opt, callback_data=f"ans_{btn_text[0]}"))
            
        bot.send_message(
            call.message.chat.id,
            f"{item['question']}",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("ans_"))
def check_answer(call):
    answer = call.data.split("_")[1]
    bot.answer_callback_query(call.id, f"Сиз {answer} жавобини танладингиз!")

if __name__ == "__main__":
    print("Бот ишга тушди...")
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
