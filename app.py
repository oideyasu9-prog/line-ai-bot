from flask import Flask, request
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = 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
LINE_ACCESS_TOKEN =TFeUUPncqDT2I2+JOwra4mspAsYSjW37S+cdKFjxetvL2rFb5tWBB7hp5hpSgqLMscXl0JHGu2aZgZywHZ6RI2DTac3DO4d9n/mTpDv4zFNDp4AzUN2d+TFoEhYCLBz/WbKhj2/jt8+toBXm2YW9wwdB04t89/1O/w1cDnyilFU=

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
