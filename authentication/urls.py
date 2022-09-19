from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView, LoginView, UserView, LogoutView, ActivateAccount

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('activate/<uid>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]
