from django.shortcuts import render

import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageSendMessage
from linebot.exceptions import InvalidSignatureError, LineBotApiError

import json
from .models import *
 
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
    user_message = event.message.text  # 取得使用者發送的文字
    if "-" in user_message:
        teacher_name = user_message.split("-")[0]
        course_name = user_message.split("-")[1]
        filtered_courses = Course.objects.filter(teacher_name=teacher_name, course_name=course_name)[:5]
        if filtered_courses.exists():
            messages = []
            for course in filtered_courses:
                messages.append(TextMessage(
                    text=f"""課程: {course.course_name}\
                    評價: {course.feedback_content}
                    """))

            line_bot_api.reply_message(
                event.reply_token,
                messages  
                
            )         
        else:
            print("Empty")
    