from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage
)

from .utils import morphological_analysis, list_to_string_with_line_feed

line_bot_api = LineBotApi(channel_access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    return HttpResponse('OK', status=200)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    text = list_to_string_with_line_feed(morphological_analysis(event.message.text))

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text),
    )
