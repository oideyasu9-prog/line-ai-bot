from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ← ここにあなたのAPIキーとLINEアクセストークンを直接書く
OPENAI_API_KEY = "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"  # GPT-3.5用キー
LINE_ACCESS_TOKEN = "TFeUUPncqDT2I2+JOwra4mspAsYSjW37S+cdKFjxetvL2rFb5tWBB7hp5hpSgqLMscXl0JHGu2aZgZywHZ6RI2DTac3DO4d9n/mTpDv4zFNDp4AzUN2d+TFoEhYCLBz/WbKhj2/jt8+toBXm2YW9wwdB04t89/1O/w1cDnyilFU="

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.json
        print("Received body:", body)  # LINEからのメッセージ確認用

        events = body.get("events", [])
        for event in events:
            if event.get("type") == "message" and event["message"]["type"] == "text":
                user_message = event["message"]["text"]
                reply_token = event["replyToken"]

                print("Sending to OpenAI:", user_message)  # 送信前ログ

                # OpenAI API へ送信（無料で使える gpt-3.5-turbo）
                try:
                    res = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [{"role": "user", "content": user_message}]
                        },
                        timeout=15
                    )
                    print("OpenAI response status:", res.status_code)
                    print("OpenAI response:", res.text)

                    res.raise_for_status()
                    ai_reply = res.json()["choices"][0]["message"]["content"]

                except Exception as e:
                    print("OpenAI request failed:", e)
                    ai_reply = "すみません、AIの処理中にエラーが発生しました。"

                # LINE に返信
                try:
                    requests.post(
                        "https://api.line.me/v2/bot/message/reply",
                        headers={
                            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
                            "Content-Type": "application/json"
                        },
                        json={"replyToken": reply_token, "messages": [{"type": "text", "text": ai_reply}]},
                        timeout=15
                    )
                except Exception as e:
                    print("LINE reply failed:", e)

        return "OK"

    except Exception as e:
        print("Webhook error:", e)
        return "Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
