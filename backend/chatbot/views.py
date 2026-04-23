import os
import json
import google.generativeai as genai
from django.http import JsonResponse
from dotenv import load_dotenv
from django.shortcuts import render
from .models import ChatMessage
from django.views.decorators.csrf import csrf_exempt

# 1. Load your API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model=genai.GenerativeModel('models/gemini-2.5-flash-lite')

def index(request):
    return render(request, 'chatbot/index.html')


@csrf_exempt
def chat_api(request):
    data = json.loads(request.body)
    user_input = data.get("message")

    
    user_message=f"User :{user_input}"

    history_objs=ChatMessage.objects.order_by('-created_at')[:10]
    context = "\n".join([f"Message: {msg.message}" for msg in reversed(history_objs)])

    prompt=f"Context: {context}, User Message:{user_message}"

    data=model.generate_content(prompt)
    response=data.text

    ChatMessage.objects.create(message=user_input)
    ChatMessage.objects.create(message=response)
    return JsonResponse({"response" : response})
    