from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from quizusr.serializers import QuizUserSerializer, MyTokenObtainPairSerializer, RegisterSerializer

User = get_user_model()

class QuizUser(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        userID = request.GET.get('userId')
        if userID:
            user = User.objects.get(pk=userID)
            serialiser = QuizUserSerializer(user, many=False,  context={'request': request})
            return JsonResponse(serialiser.data, safe=False)
        else:
            user_all = User.objects.all()
            serialiser = QuizUserSerializer(user_all, many=True,  context={'request': request})
            return JsonResponse(serialiser.data, safe=False)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
