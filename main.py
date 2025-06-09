from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery

import asyncio
from aiohttp import web 
import os

# 🔐 Впиши сюда свой секретный токен
TOKEN = "7862255887:AAG3G-76mmHj15DaZ8KGfWWcc6cVAhq0I7w"

# 🧠 Инициализация бота и диспетчера
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)  # Настройка parse_mode
bot = Bot(token=TOKEN, default=default_properties)  # Передаем default_properties
dp = Dispatcher(storage=MemoryStorage())

# Простой HTTP-сервер для Render.com
async def on_startup(app):
    asyncio.create_task(dp.start_polling(bot))

app = web.Application()
app.on_startup.append(on_startup)

# Маршрут для проверки работоспособности
async def healthcheck(request):
    return web.Response(text="OK")

app.router.add_get("/", healthcheck)

START_TEXT = """
➤ ТАКСИ-БОТ | НӨКИС - ШЫМБАЙ

Хош келдиңиз!
Бул бот Нөкис ҳәм Шымбай арасында такси буйыртпа етиўдиң ең әпиўайы усылы.

🔹 ЕКИ ЖӨНЕЛИС АРТИҚША ЕМЕС.
🔹 ҲӘММЕ НӘРСЕ ТЕЗ ҲӘМ КҮТИЛМЕГЕН ҲАЛДА ИСЛЕЙДИ.
🔹 АЙДАЎШИЛАР ТЕКСЕРИЛДИ, БУЙЫРТПАЛАР БАҚЛАЎ АЛДИНДА.
🔹 СИЗ ТАНЛАЙСИЗ - БИР НЕШЕ СЕКУНДТА

✅ Маршрут таңласаңыз болды, қалғаны менен биз шуғылланамыз.

✅ 24/7 ислейди.
✅ Әпиўайы. Тез. Исенимли.

☎️ +998905774447

☎️ +998994804848


"""

TEXT_NOKIS_SHYMBAY = """
🚕 <b>Нокистен → Шымбайга</b>  
   - Жол узынлығы: <i>59,3 км</i>  
   - Уақыт: <i>1 сагат</i>

📞 <b>Телефон</b>: +998905774447
📞 <b>Телефон</b>: +998994804848

✅ <b>Қосымша хызметлер</b>: АМАНАТ БОЛСА АЛЫП КЕТЕМИЗ ХАМ БАГАЖ БАР
"""

TEXT_SHYMBAY_NOKIS = """
🚗 <b>Шымбайдан → Нокиске</b>
   - Жол узынлығы: <i>59,3 км</i>   
   - Уақыт: <i>1 сагат</i> 

📞 <b>Телефон</b>: +998905774447
📞 <b>Телефон</b>: +998994804848
✅ <b>Қосымша хызметлер</b>: АМАНАТ БОЛСА АЛЫП КЕТЕМИЗ ХАМ БАГАЖ БАР
"""

# Словарь для хранения статистики
user_stats = {}

# 🪑 Обычные кнопки маршрутов
# def get_main_keyboard():
#     return ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="Нокис-Шымбай")],
#             [KeyboardButton(text="Шымбай-Нукус")]
#         ],
#         resize_keyboard=True,  # подгоняет размер
#         one_time_keyboard=False  # клавиатура остаётся
#     )
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Нокис-Шымбай", callback_data="nukis_shymbay"),
                InlineKeyboardButton(text="Шымбай-Нукус", callback_data="shymbay_nukis")
            ]
        ],
    )

# 🌀 Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    # Если пользователь новый, добавляем его в статистику
    if user_id not in user_stats:
        user_stats[user_id] = 1
    else:
        user_stats[user_id] += 1

    await message.answer(
        START_TEXT,
        reply_markup=get_main_keyboard()
    )

# 🚖 Обработка выбора маршрута
# @dp.message(F.text == "Нокис-Шымбай")
# async def handle_nukus_shymbay(message: Message):
#     user_id = message.from_user.id

#     # Увеличиваем счетчик взаимодействий пользователя
#     if user_id not in user_stats:
#         user_stats[user_id] = 1
#     else:
#         user_stats[user_id] += 1

#     await message.answer(TEXT_NOKIS_SHYMBAY)

# @dp.message(F.text == "Шымбай-Нукус")
# async def handle_shymbay_nukus(message: Message):
#     user_id = message.from_user.id

#     # Увеличиваем счетчик взаимодействий пользователя
#     if user_id not in user_stats:
#         user_stats[user_id] = 1
#     else:
#         user_stats[user_id] += 1

#     await message.answer(TEXT_SHYMBAY_NOKIS)
@dp.callback_query(F.data == "nukis_shymbay")
async def handle_nukus_shymbay(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Обновляем статистику
    user_stats[user_id] = user_stats.get(user_id, 0) + 1

    # Отправляем сообщение с маршрутом
    await callback.message.answer(TEXT_NOKIS_SHYMBAY)
    await callback.answer()  # Убираем "часики"

@dp.callback_query(F.data == "shymbay_nukis")
async def handle_shymbay_nukus(callback: CallbackQuery):
    user_id = callback.from_user.id

    user_stats[user_id] = user_stats.get(user_id, 0) + 1

    await callback.message.answer(TEXT_SHYMBAY_NOKIS)
    await callback.answer()



# 📊 Команда /stats для вывода статистики
@dp.message(F.text == "/stats")
async def show_stats(message: Message):
    total_users = len(user_stats)  # Количество уникальных пользователей
    total_interactions = sum(user_stats.values())  # Общее количество взаимодействий

    await message.answer(
        f"📊 <b>Боттын статистикасы:</b>\n"
        f"• Колдарнушылар саны: <b>{total_users}</b>\n"
        f"• Катнаслар саны: <b>{total_interactions}</b>",
        parse_mode=ParseMode.HTML
    )

# Запуск HTTP-сервера
if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
