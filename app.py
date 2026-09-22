# Mybot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from olympiad_db import OLYMPIAD_TESTS

# БОТ ТОКЕНИНИ ҚУЙИДАГИ ПУСТИНГ ИЧИГА ЁЗАСИЗ:
API_TOKEN = '8886969003:AAEh6mkVzOqnYKGjPjvOMytDuxAiG4cUCng'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="9-синф"), KeyboardButton(text="10-синф"), KeyboardButton(text="11-синф")]
        ],
        resize_keyboard=True
    )
    await message.answer("Ассалому алайкум! Олимпиада тест ботига хуш келибсиз. Синфни танланг:", reply_markup=keyboard)

@dp.message(lambda message: message.text in ["9-синф", "10-синф", "11-синф"])
async def select_class(message: types.Message):
    grade = message.text.split("-")[0]

    if grade == "9":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="9-синф: 1-вариант"), KeyboardButton(text="9-синф: 2-вариант")],
                [KeyboardButton(text="9-синф: 3-вариант"), KeyboardButton(text="9-синф: 4-вариант")],
                [KeyboardButton(text="🔙 Орқага")]
            ],
            resize_keyboard=True
        )
    elif grade == "10":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="10-синф: 1-вариант"), KeyboardButton(text="10-синф: 2-вариант")],
                [KeyboardButton(text="10-синф: 3-вариант")],
                [KeyboardButton(text="🔙 Орқага")]
            ],
            resize_keyboard=True
        )
    elif grade == "11":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="11-синф: 1-вариант"), KeyboardButton(text="11-синф: 2-вариант")],
                [KeyboardButton(text="11-синф: 3-вариант")],
                [KeyboardButton(text="🔙 Орқага")]
            ],
            resize_keyboard=True
        )
    else:
        return

    await message.answer(f"Сиз {message.text}ни танладингиз. Керакли вариантни танланг:", reply_markup=keyboard)

@dp.message(lambda message: "вариант" in message.text.lower())
async def select_variant(message: types.Message):
    text = message.text
    if "9-синф" in text:
        grade = "9"
    elif "10-синф" in text:
        grade = "10"
    elif "11-синф" in text:
        grade = "11"
    else:
        await message.answer("Хатолик юз берди.")
        return

    if "1-вариант" in text:
        var = "variant_1"
    elif "2-вариант" in text:
        var = "variant_2"
    elif "3-вариант" in text:
        var = "variant_3"
    elif "4-вариант" in text:
        var = "variant_4"
    else:
        return

    tests = OLYMPIAD_TESTS.get(grade, {}).get(var, [])
    if not tests:
        await message.answer("Бу вариант учун ҳали тестлар базага киритилмаган.")
        return

    for t in tests:
        question_text = f"<b>{t['question']}</b>\n\n" + "\n".join(t['options'])
        await message.answer(question_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "🔙 Орқага")
async def go_back(message: types.Message):
    await send_welcome(message)

async def main():
    # aiogram 3.x учун ишга тушириш қисми
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())