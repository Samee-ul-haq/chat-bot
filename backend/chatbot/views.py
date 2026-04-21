import os
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.shortcuts import render

# 1. Load your API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Initialize the Model
model = genai.GenerativeModel('models/gemini-2.5-flash')

def index(request):
    """
    This function looks for 'index.html' inside your 
    chatbot/frontend/ folder and sends it to the browser.
    """
    return render(request, 'frontend/index.html')

@csrf_exempt
def chat_api(request):
    if request.method == "OPTIONS":
        return JsonResponse({"status": "ok"})

    if request.method == "POST":
        try:
            # 3. Parse the message from your Frontend
            data = json.loads(request.body)
            user_message = data.get("message")
            
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # 4. Call the real Gemini API
            response = model.generate_content(user_message)
            
            # 5. Send back the real AI response
            return JsonResponse({"response": response.text})

        except Exception as e:
            # This will tell you if your API Key is missing or invalid
            print(f"Gemini Error: {e}") 
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request"}, status=400)