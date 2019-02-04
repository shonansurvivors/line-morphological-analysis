import os

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage
)
from janome.tokenizer import Tokenizer

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(channel_access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=LINE_CHANNEL_SECRET)


def morphological_analysis(text):
    T = Tokenizer()
    tokens = T.tokenize(text)
    list = []
    for i in range(len(tokens)):
        word = tokens[i].base_form
        part_of_speech = tokens[i].part_of_speech.split(',')[0]
        list.append(f'{word} {part_of_speech}')
    return list


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

    results = morphological_analysis(event.message.text)

    response = ''
    for result in results:
        response += result + '\n'
    response = response.rstrip('\n')

    line_bot_api.reply_message(cd
        event.reply_token,
        TextSendMessage(text=response),
    )