from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('NHkQkmWBo8jgwRap5YoTeLK8hnrFwpJjreTf8/Vj5EzPRGILXV7LZW10JIkXYtPDQ3X+qsLJB+et4gYSnHIQEBLptczcXi6ai10qjVlXUpOP4l7GB5woESRsKLOFI7oQ96gyAOyGWKzfaBlgHtIJqgdB04t89/1O/w1cDnyilFU= ')
handler = WebhookHandler('8907812554e4a896ef76926ec74a16ba')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()