from django.shortcuts import render

# Create your views here.
# views.py
from django.http import JsonResponse
from .models import ChatMessage
import requests
import google.generativeai as genai
import os
genai.configure(api_key="AIzaSyB0-yYoOwh_RiayHltkG0dxoZXnNcnJxA0")

def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')

        # Build the Gemini API request
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)
        bot_response = response.text


        # Save chat in the database
        chat_message = ChatMessage(user_message=user_message, bot_response=bot_response)
        chat_message.save()

        return JsonResponse({"message": user_message, "response": bot_response})

    # Fetch chat history
    chat_history = ChatMessage.objects.all().order_by('timestamp')

    return render(request, "chat/chat.html", {"chat_history": chat_history})
