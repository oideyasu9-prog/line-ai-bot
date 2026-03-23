from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    user_message = data["events"][0]["message"]["text"]

    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": "Bearer あなたのAPIキー",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_message}]
        }
    )

    data = res.json()
    print(data)

    reply = data.get("choices", [{}])[0].get("message", {}).get("content", "エラー")

    requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers={
            "Authorization": "Bearer あなたのLINEトークン",
            "Content-Type": "application/json"
        },
        json={
            "replyToken": data["events"][0]["replyToken"],
            "messages": [{"type": "text", "text": reply}]
        }
    )

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
