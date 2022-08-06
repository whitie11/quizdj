
from django.db import models
from rest_framework import serializers

# Create your models here.
class Active_Channel(models.Model):
    username = models.CharField(max_length=200)
    channel_name = models.CharField(max_length=200)
    quiz_group_name = models.CharField(max_length=200)
    lastSeen = models.DateTimeField()

class Active_ChannelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Active_Channel
        fields = ['username','channel_name', 'quiz_group_name' ]
