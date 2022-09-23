from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('activate/<uid>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    # path('profiles', views.ProfilesList.as_view()),
    # path('people/<int:pk>/', views.ProfileDetailView.as_view()),
    # path('create', views.ProfileCreate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
