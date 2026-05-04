from flask import Flask, request, abort
import os
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

@app.route("/callback", methods=['POST'])
def callback():
    body = request.json
    
    for event in body['events']:
        if event['type'] == 'message':
            reply_token = event['replyToken']
            user_msg = event['message']['text']

            reply(reply_token)

    return 'OK'


def reply(reply_token):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    flex_message = {
        "type": "flex",
        "altText": "衛寶熊選單",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://picsum.photos/800/400",
                "size": "full",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "衛寶熊",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "有我在，你的健康熊安心！",
                        "wrap": True,
                        "margin": "md",
                        "size": "sm",
                        "color": "#666666"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "message",
                            "label": "📘 登入學生ID",
                            "text": "登入學生ID"
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "📰 保健最新資訊",
                            "text": "保健最新資訊"
                        }
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "🔥 TDEE試算",
                            "text": "TDEE試算"
                        }
                    }
                ]
            }
        }
    }

    data = {
        "replyToken": reply_token,
        "messages": [flex_message]
    }

    requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))