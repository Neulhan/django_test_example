from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
import random

from news.models import News
from news.serializers import NewsSerializer
from rest_framework import status


class NewsAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsDetailAPIView(APIView):
    def delete(self, request, pk):
        news = News.objects.get(pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def rps_logic(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice, computer_choice) in (
            ('rock', 'paper'),
            ('scissors', 'rock'),
            ('paper', 'scissors'),):
        return 'lose'
    else:
        return 'win'


class RPSAPIView(APIView):
    def get(self, request):
        user_choice = request.GET.get('choice')
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)

        res_dict = {
            'result': rps_logic(user_choice, computer_choice)
        }
        return Response(res_dict, status=status.HTTP_200_OK)

