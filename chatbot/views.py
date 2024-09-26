from django.shortcuts import render

import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageSendMessage
import json

parser = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def reply_cat_url():
    url = "https://api.thecatapi.com/v1/images/search?limit=1"
    response = requests.get(url)
    content = json.loads(response.text)
    image_url = content[0]["url"]
    return image_url


@csrf_exempt
def callback(request):
    # 確認請求是來自 LINE 的 webhook
    signature = request.META['HTTP_X_LINE_SIGNATURE']

    # 取得 request body
    body = request.body.decode('utf-8')

    try:
        # 驗證來自 LINE 的簽名
        parser.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseForbidden()

    return HttpResponse('OK')

# 處理訊息的事件
@parser.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得貓咪圖片的 URL
    image_url = reply_cat_url()

    # 建立要回傳的 ImageSendMessage
    image_message = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url
    )

    # 回覆使用者的訊息
    line_bot_api.reply_message(
        event.reply_token,
        image_message
    )