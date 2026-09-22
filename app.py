import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '8886969003:AAEh6mkVzOqnYKGjPjvOMytDuxAiG4cUCng'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Тестлар базаси (беvosita коднинг ўзида, хатолик чиқмаслиги учун)
OLYMPIAD_TESTS = {
    "9": {
        "variant_1": [
            {"question": "9-синф 1-вариант: Физикадан Ньютоннинг нечта қонуни бор?", "options": ["A) 2 та", "B) 3 та", "C) 4 та", "D) 5 та"]},
            {"question": "9-синф 1-вариант: Тезлик бирлиги нима?", "options": ["A) m/s", "B) kg", "C) m", "D) s"]}
        ],
        "variant_2": [
            {"question": "9-синф 2-вариант: Энергия бирлиги нима?", "options": ["A) Joul", "B) Watt", "C) Newton", "D) Pascal"]}
        ]
    },
    "10": {
        "variant_1": [
            {"question": "10-синф 1-вариант: Молекуляр физика асосчиларидан бири ким?", "options": ["A) Ньютон", "B) Эйнштейн", "C) Больцман", "D) Архимед"]}
        ]
    },
    "11": {
        "variant_1": [
            {"question": "11-синф 1-вариант: Ёруғлик тезлиги тахминан қанчага тенг?", "options": ["A) 300 000 km/s", "B) 150 000 km/s", "C) 3000 km/s", "D) 10 000 km/s"]}
        ]
    }
}

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
                [KeyboardButton(text="🔙 Орқага")]
            ],
            resize_keyboard=True
        )
    elif grade == "10":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="10-синф: 1-вариант")],
                [KeyboardButton(text="🔙 Орқага")]
            ],
            resize_keyboard=True
        )
    elif grade == "11":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="11-синф: 1-вариант")],
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
    else:
        var = "variant_1"

    tests = OLYMPIAD_TESTS.get(grade, {}).get(var, [])
    if not tests:
        await message.answer("Бу вариант учун ҳали тестлар базага киритилмаган. Тез орада қўшилади!")
        return

    for index, t in enumerate(tests, start=1):
        options_text = "\n".join(t['options'])
        question_text = f"<b>{index}. {t['question']}</b>\n\n{options_text}"
        await message.answer(question_text, parse_mode="HTML")

@dp.message(lambda message: message.text == "🔙 Орқага")
async def go_back(message: types.Message):
    await send_welcome(message)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
