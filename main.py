import os
import requests
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

# Загружаем переменные из .env (на Render задаются вручную)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI21_API_KEY = os.getenv("AI21_API_KEY")

# Создаём Telegram-бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Загружаем промпт с характером Деда Коли
with open("kolya_persona.txt", "r", encoding="utf-8") as f:
    kolya_prompt = f.read()

# Адрес API AI21
AI21_URL = "https://api.ai21.com/studio/v1/j2-light/complete"

# Функция для генерации ответа от AI21
def generate_ai21_response(prompt_text):
    headers = {
        "Authorization": f"Bearer {AI21_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt_text,
        "numResults": 1,
        "maxTokens": 150,
        "temperature": 0.7,
        "topP": 1,
        "topKReturn": 0,
        "stopSequences": ["Пользователь:", "Дед Коля:"]
    }
    response = requests.post(AI21_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["completions"][0]["data"]["text"].strip()
    else:
        return "Эх, что-то сломалось, пиздец..."

# Обработчик всех сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    prompt = kolya_prompt + "\nПользователь: " + message.text + "\nДед Коля:"
    answer = generate_ai21_response(prompt)
    await message.reply(answer)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
