from django.urls import include, path

# from rest_framework_simplejwt.views import (
#     # TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )

from quizusr import views as QUV

urlpatterns = [
    path('token/', QUV.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', QUV.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', QUV.TokenVerifyView.as_view(), name='token_verify'),
    path('getUser/', QUV.QuizUser.as_view(), name='get_user_s'  ),
]