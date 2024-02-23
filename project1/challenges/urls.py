
from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('<int:challenge_pk>/', views.detail, name='detail'),
    path('<int:challenge_pk>/code/',views.code, name='code'),
    path('code/<int:code_pk>',views.watch, name='watch'),
]
