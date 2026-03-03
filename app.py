from flask import Flask, request
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = message["from"]

        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": "Салом! Бот кор мекунад 🚀"}
        }

        requests.post(url, headers=headers, json=payload)
    except:
        pass

    return "OK", 200
