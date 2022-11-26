from django.urls import path
from . import views

urlpatterns = [
    path('', views.peopleList, name='list'),
    path('detail/<str:pk>/', views.peopleDetail, name='detail'),
    path('create', views.peopleCreate, name='create'),
    path('update/<str:pk>/', views.peopleUpdate, name='update'),
    path('delete/<str:pk>/', views.peopleDelete, name='delete'),
]
