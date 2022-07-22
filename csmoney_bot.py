import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import asyncio


# bot = Bot(token=os.getenv("5492941687:AAGcc4FFgdkVSjH4XQ1hUOTtz9WR9jM4Uts"), parse_mode=types.ParseMode.HTML)
# dp = Dispatcher(bot)
# Токен, выданный BotFather в телеграмме
API_TOKEN = '5492941687:AAGcc4FFgdkVSjH4XQ1hUOTtz9WR9jM4Uts'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['🔪 Ножи', '🔫 Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите категорию', reply_markup=keyboard)
    

@dp.message_handler(Text(equals='🔪 Ножи'))
async def get_discount_knives(message: types.Message):
    await message.answer('Please waiting...')
    
    collect_data(cat_type=2)
    
    with open('result.json') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{(item.get("full_name"), item.get("3d"))}\n' \
            f'{("Скидка: ")}{item.get("overprice")}%\n' \
            f'{("Цена: ")}${item.get("item_price")}🔥'
    
    
        if index%20 == 0:
            asyncio.sleep(3)
            
        await message.answer(card)

        
@dp.message_handler(Text(equals='🔫 Снайперские винтовки'))
async def get_discount_guns(message: types.Message):
    await message.answer('Please waiting...')
    
    collect_data(cat_type=4)
    
    with open('result.json') as file:
        data = json.load(file)
        
    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("overprice")}%\n' \
            f'{hbold("Цена: ")}${item.get("item_price")}🔥'
    
    
        if index%20 == 0:
            asyncio.sleep(3)
            
        await message.answer(card)
    
def main():
    executor.start_polling(dp)
    
    
if __name__ == '__main__':
    main()
    