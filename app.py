from flask import Flask, request, abort
import time

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('E8M/Zgv4jKfyH/13Y/qcZ3YosAzkp9IRUFDRN0ZOYvKUVFLBrjqCAQzKruz6y2dvODQ57vf07Y+DlJJ4CZCHzToyhLm8dhPkmcz4aFNwFicKuHnDl2WGeNTA9id2jRVhr4Mhr2RyoP39f+7Wonbl0gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6af8e930dab9b3a977719185adc48a99')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
    text += "display_name ： " + profile.display_name + "\n"
    text += "user_id ： " + profile.user_id + "\n"
    text += "type ： " + event.source.type + "\n"
    if event.source.type == "group":
        group_id = event.source.group_id
        text += "group_id ： " + group_id + "\n"
        if group_id == "C193ba92879d441b6a12a533a18be62a9":
            fp = open("member","w+")
            fp.write("24128 二兵 戴立宸 0920108958 未回報\n24129 二兵 林翰霳 0939085913\n24130 二兵 魏廷宇 0963085102\n24131 二兵 薛博尹 0989997805\n24132 二兵 劉　煒 0966087873\n24133 二兵 陳嘉宏 0936742136\n24134 二兵 張秉禎 0930265781\n24135 二兵 蘇弘碩 0975507212\n24136 二兵 陳昇昇 0932023953\n24137 二兵 周川景 0973282283\n24138 二兵 翁浩哲 0972143417\n24139 二兵 胡皓翔 0973767218\n24140 二兵 陳芳順 0963053651\n24141 二兵 許家瑋 0988218690\n")
            fp.close()
            fp = open("member","rw")
            line = fp.readline()
            while line:
                text += line
                line = fp.readline()
            fp.close()
    message = TextSendMessage(text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


'''
24128 二兵 戴立宸 0920108958

24129 二兵 林翰霳 0939085913

24130 二兵 魏廷宇 0963085102

24131 二兵 薛博尹 0989997805

24132 二兵 劉　煒 0966087873

24133 二兵 陳嘉宏 0936742136

24134 二兵 張秉禎 0930265781

24135 二兵 蘇弘碩 0975507212

24136 二兵 陳昇昇 0932023953

24137 二兵 周川景 0973282283

24138 二兵 翁浩哲 0972143417

24139 二兵 胡皓翔 0973767218

24140 二兵 陳芳順 0963053651

24141 二兵 許家瑋 0988218690
'''