from functools import partial
import json
from xmlrpc.client import TRANSPORT_ERROR
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from quizAdmin.models import Question
from quizAdmin.serializers import QuestionGroupListSerializer, QuestionSerializer
from django.db.models import Count
from django.core import serializers
from django.forms.models import model_to_dict


class QuestionList(APIView):
    def get(self, request):
        question_all = Question.objects.all()
        serializer = QuestionSerializer(question_all, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        group = data['group']
        try:
            ql = Question.objects.filter(
                group=group).order_by('question_num')
        except Question.DoesNotExist:
            return JsonResponse('No questions found', status=404, safe=False)
        serialiser = QuestionSerializer(ql, many=True)
        return JsonResponse(serialiser.data, status=201, safe=False)

    def put(self, request):
        data = JSONParser().parse(request)
        if (data['question_num'] == 0):
            try:
                lastQuestion = Question.objects.filter(
                    group=data['group']).order_by('-question_num').first()
                if (lastQuestion):
                    x = lastQuestion.question_num
                    data['question_num'] = x + 1
                    lastQuestion = None
                else:
                    lastQuestion = None
                    data['question_num'] = 1
            except:
                lastQuestion = None
                data['question_num'] = 1
        else:
            lastQuestion = Question.objects.filter(
                group=data['group'], question_num=data['question_num']).first()

        serializer = QuestionSerializer(lastQuestion, data=data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetQuestionGroups(APIView):
    def get(self, request):
        qs = Question.objects.values('group').annotate(
            count=Count('group')).order_by('group').distinct()
        serializer = QuestionGroupListSerializer(qs, many=True, )
        # json_data = JSONRenderer().render(serializer.data)
        return JsonResponse(serializer.data, safe=False)
