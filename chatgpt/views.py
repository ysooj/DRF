from rest_framework.views import APIView
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings
from . bots import translat_bot

class TranslateAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        chatgpt_response = translat_bot(user_message)
        return Response({"message": chatgpt_response})