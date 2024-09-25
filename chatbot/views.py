from django.shortcuts import render

import requests
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
from linebot.exceptions import InvalidSignatureError, LineBotApiError

import json
from .models import *

from pathlib import Path
import os

parser = WebhookHandler(settings.LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

BASE_DIR = Path(__file__).resolve().parent.parent

def flex_message_package(course_info):
    json_path = os.path.join(BASE_DIR, 'chatbot', 'reply_evaluation.json')
    flex = json.load(open(json_path, 'r', encoding='utf-8'))

    flex['header']['contents'][0]['text'] = course_info['course_name']
    flex['header']['contents'][1]['text'] = course_info['teacher_name']
    flex['body']['contents'][0]['contents'][0]['contents'][0]['text'] = course_info['feedback_content']
    flex['body']['contents'][0]['contents'][2]['contents'][1]['text'] = course_info['course_type']
    flex['body']['contents'][0]['contents'][3]['contents'][1]['text'] = course_info['evaluation_semester']
    flex['body']['contents'][0]['contents'][4]['contents'][1]['text'] = course_info['submitter_name']
    flex['footer']['contents'][0]['contents'][0]['text'] = f"{course_info['teacher_name']}-{course_info['course_name']}"
    flex['footer']['contents'][0]['contents'][1]['text'] = f"第{course_info['number']}則"

    return flex

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
            for idx, course in enumerate(filtered_courses, start=1):  # 使用 enumerate 給每個課程加上編號
                # 準備課程資料以傳入 flex_message_package 函式
                course_info = {
                    'course_name': course.course_name,
                    'teacher_name': course.teacher_name,
                    'course_type': course.course_type,
                    'feedback_content': course.feedback_content,
                    'evaluation_semester': course.evaluation_semester,
                    'submitter_name': course.submitter_name,
                    'number': str(idx),  # 這裡的 idx 是第幾則的意思
                    }
                # 呼叫 flex_message_package 函式來產生 Flex Message
                flex_message = flex_message_package(course_info)
                # 使用 FlexSendMessage 回傳 Flex Message
                messages.append(FlexSendMessage(
                        alt_text=f"課程評價：{course.course_name}",
                        contents=flex_message
                    ))
            line_bot_api.reply_message(
                event.reply_token,
                messages  # 回傳 Flex Message 列表
            )         
        else:
            print("Empty")
    