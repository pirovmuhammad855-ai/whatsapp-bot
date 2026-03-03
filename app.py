from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

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
        user_text = message["text"]["body"]

        # === OpenAI Request ===
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ту як ёрдамчии зираки тоҷикӣ ҳастӣ."},
                {"role": "user", "content": user_text}
            ]
        )

        ai_reply = response.choices[0].message.content

        # === Send back to WhatsApp ===
        url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": ai_reply}
        }

        requests.post(url, headers=headers, json=payload)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
