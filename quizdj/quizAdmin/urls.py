from django.urls import include, path

from quizAdmin import views as QAViews


urlpatterns = [
    path('questions/', QAViews.QuestionList.as_view()), 
    path('questions/groups/', QAViews.GetQuestionGroups.as_view()),   
]
