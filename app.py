from flask import Flask, request
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json

    user_message = body["events"][0]["message"]["text"]
    reply_token = body["events"][0]["replyToken"]

    # OpenAI
    res = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1-mini",
            "input": user_message
        }
    )

    ai_reply = res.json()["output"][0]["content"][0]["text"]

    # LINE返信
    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers={
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": ai_reply
                }
            ]
        }
    )

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
