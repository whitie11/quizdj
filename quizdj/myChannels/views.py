import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from myChannels.models import Active_Channel, Active_ChannelSerializer

# Create your views here.
def index(request):
    return render(request, 'myChannels/index.html')

def room(request, room_name):
    return render(request, 'myChannels/room.html', {
        'room_name': room_name
    })    

class ActivePlayers(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        players = Active_Channel.objects.all()
        serialiser = Active_ChannelSerializer(players, many=True)
        return JsonResponse(serialiser.data, safe=False)
