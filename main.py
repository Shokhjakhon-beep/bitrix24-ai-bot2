import os
from flask import Flask, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BITRIX_WEBHOOK_URL = os.getenv("BITRIX_WEBHOOK_URL")
RESPONSIBLE_ID = 1

def send_to_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def create_bitrix_task(task_text):
    url = f"{BITRIX_WEBHOOK_URL}/task.item.add.json"
    payload = {
        "fields": {
            "TITLE": "Заявка из Telegram-бота",
            "DESCRIPTION": task_text,
            "RESPONSIBLE_ID": RESPONSIBLE_ID
        }
    }
    return requests.post(url, json=payload)

@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")

    if not text or not chat_id:
        return "no message"

    if text == "/start":
        welcome_msg = (
            "Уважаемый клиент, здравствуйте!\n\n"
            "Мы рады приветствовать Вас в нашем информационном боте.\n\n"
            "Если Вы хотите получить более подробную информацию о нашей компании и услугах, "
            "просим Вас предоставить следующую информацию:\n\n"
            "🔹 Ваши имя и фамилия\n"
            "🔹 Ваш контактный номер телефона\n"
            "🔹 Какой именно услугой Вы заинтересованы\n"
            "🔹 Удобное для Вас время для обратной связи\n\n"
            "Пожалуйста, заполните эти данные одним сообщением — и мы обязательно свяжемся с Вами в кратчайшие сроки."
        )
        send_to_telegram(chat_id, welcome_msg)
    else:
        create_bitrix_task(text)
        thanks_msg = (
            "Благодарим Вас за уделённое время. "
            "Мы обязательно свяжемся с Вами в ближайшее время."
        )
        send_to_telegram(chat_id, thanks_msg)

    return "ok"