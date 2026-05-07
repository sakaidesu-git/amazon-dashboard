from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

# ←←← ここに追加（UptimeRobot が叩く GET / 用）
@app.route("/", methods=['GET'])
def home():
    return "OK", 200

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()

    if text == "amazon":
        url = "https://sakaidesu-git.github.io/amazon-dashboard/amazon_dashboard.html"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=url)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="コマンドが違います")
        )

if __name__ == "__main__":
    app.run()
