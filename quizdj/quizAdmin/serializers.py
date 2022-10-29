from dataclasses import field
from rest_framework import serializers

from quizAdmin.models import Question, QuestionGroupList


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ('ID', 'group', 'question_num', 'text', 'answerA', 'answerB', 'answerC', 'answerD', 'duration', 'correctAns'  )

class QuestionGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionGroupList
        fields = ('__all__')