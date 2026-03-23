from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ← ここにあなたのAPIキーとLINEアクセストークンを直接書く
OPENAI_API_KEY = "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"
LINE_ACCESS_TOKEN =　"TFeUUPncqDT2I2+JOwra4mspAsYSjW37S+cdKFjxetvL2rFb5tWBB7hp5hpSgqLMscXl0JHGu2aZgZywHZ6RI2DTac3DO4d9n/mTpDv4zFNDp4AzUN2d+TFoEhYCLBz/WbKhj2/jt8+toBXm2YW9wwdB04t89/1O/w1cDnyilFU="

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.json
        print("Received body:", body)  # ここでLINEからのJSONを確認できる

        events = body.get("events", [])
        for event in events:
            # テキストメッセージのみ処理
            if event.get("type") == "message" and event["message"]["type"] == "text":
                user_message = event["message"]["text"]
                reply_token = event["replyToken"]

                # OpenAI に送信
                try:
                    res = requests.post(
                        "https://api.openai.com/v1/responses",
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={"model": "gpt-4.1-mini", "input": user_message},
                        timeout=15
                    )
                    res.raise_for_status()
                    ai_reply = res.json()["output"][0]["content"][0]["text"]
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
