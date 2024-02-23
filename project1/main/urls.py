
from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('test/', views.test, name='test'),
    path('test2/', views.test2, name='test2'),

]