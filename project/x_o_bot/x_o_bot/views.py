
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.conf import settings
# from dialogflow_lite.dialogflow import Dialogflow
from .dialogflow import Dialogflow
import speech_recognition
from .data import *

'''
This is views.py file:
    control the html file how to display in this web server.

'''

import json

'''
This function is to judge the data's type.
Needed type is like show below.

'''
def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items))
    if isinstance(data, tuple):
        return map(convert, data)
    return data

# render(request, template_name, context=None, content_type=None, status=None, using=None)[source]
@require_http_methods(['GET'])
def index_view(request):
    return render(request, 'app.html')


@require_http_methods(['POST'])
def chat_view(request):
    dialogflow = Dialogflow(**settings.DIALOGFLOW)

    '''
    input_dict should be a format in json
    { type: 'POST',
      url : url needed,
      data: {'text': text input},
      contentType: 'application/json'}

    '''
    # request.body: {all things}
    input_dict = convert(request.body)
    input_text = json.loads(input_dict)['text']

    # function text_request(text):
    #     return answer(text)
    responses, isFallbackIntent = dialogflow.text_request(str(input_text))
    if str(isFallbackIntent) == 'false':
        res = responses[0]
    else:
        res_list = similarity(str(input_text))
        res = responses[0]
        print(res)
        res = res + '\n' + 'Recommendation Questions:' + '\n' + ''.join('\t' + r + '\n' for r in res_list)
        

    if request.method == "GET":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status = 405)
        
    elif request.method == "POST":
        data = {
            'text': res,
        }
        return JsonResponse(data, status=200)

    elif request.method == "PATCH":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)

    elif request.method == "DELETE":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)


@require_http_methods(['POST'])
def voice_chat_view(request):
    dialogflow = Dialogflow(**settings.DIALOGFLOW)

    # voice = dialogflow.voice_request()

    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Start to say something: ')
        audio = recognizer.listen(source)

    try:
        result = recognizer.recognize_google(audio)
    except speech_recognition.UnknownValueError:
        result = 'I am sorry, I could not understand that.'
    except speech_recognition.RequestError as e:
        m = 'My speech recognition service has failed. {0}'
        result =  m.format(e)
    # print(result)
    # responses, isFallbackIntent = dialogflow.text_request(str(result))
    # if str(isFallbackIntent) == 'false':
    #     res = responses[0]
    # else:
    #     res_list = similarity(str(result))
    #     res = responses[0]
    #     print(res)
    #     res = res + '\n' + 'Recommendation Questions:' + '\n' + ''.join('\t' + r + '\n' for r in res_list)

    # res = result + "||" + res
    res = str(result);
    if request.method == "GET":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status = 405)
        
    elif request.method == "POST":
        data = {
            'text': res,
            # 'voice': voice,
        }
        return JsonResponse(data, status=200)

    elif request.method == "PATCH":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)

    elif request.method == "DELETE":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)


















