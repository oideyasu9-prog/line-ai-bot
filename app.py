from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "TFeUUPncqDT2I2+JOwra4mspAsYSjW37S+cdKFjxetvL2rFb5tWBB7hp5hpSgqLMscXl0JHGu2aZgZywHZ6RI2DTac3DO4d9n/mTpDv4zFNDp4AzUN2d+TFoEhYCLBz/WbKhj2/jt8+toBXm2YW9wwdB04t89/1O/w1cDnyilFU="
OPENAI_API_KEY = ""

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    for event in data["events"]:
        if event["type"] == "message":
            user_msg = event["message"]["text"]
            reply_token = event["replyToken"]

            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            body = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": user_msg}]
            }

            res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=body
            )

            reply = res.json()["choices"][0]["message"]["content"]

            requests.post(
                "https://api.line.me/v2/bot/message/reply",
                headers={
                    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
                },
                json={
                    "replyToken": reply_token,
                    "messages": [{"type": "text", "text": reply}]
                }
            )

    return "OK"

app.run()
