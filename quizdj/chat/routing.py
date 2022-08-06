# chat/routing.py
from django.urls import re_path, path

from .consumers import qMconsumer

from .consumers import playersComsumer

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]
websocket_urlpatterns = [
                path("quiz/", playersComsumer.QuizConsumer.as_asgi()),
                path("quizmaster/", qMconsumer.QMConsumer.as_asgi()),
                re_path(r'ws/quiz/(?P<quiz_name>\w+)/$', playersComsumer.QuizConsumer.as_asgi()),
                # path("chat/", PublicChatConsumer.as_asgi()),
]
