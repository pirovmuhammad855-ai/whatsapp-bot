from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "my_verify_token"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        else:
            return "Verification token mismatch", 403
    return "Hello world", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_number = message["from"]
        text = message["text"]["body"]

        reply = "Шумо навиштед: " + text

        url =
