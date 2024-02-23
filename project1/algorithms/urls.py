from django.urls import path
from . import views


app_name = 'algorithms'
urlpatterns = [
    # path('crawling/problem_list/', views.problem_list_crawling),
    # path('crawling/problem_list/check/', views.check),
    # path('crawling/problem/<int:problem_num>/', views.problem_crawling3),
    # path('crawling/class_num', views.classes_num, name='classes_num')
    path('user/<user_pk>/', views.user_crawling, name='user_crawling'),
    path('crawling/solved/<user_pk>/', views.solved_crawling, name='solved_crawling'),
    path('solved/<user_pk>/', views.solved, name='solved'),
    path('index/', views.index, name='index'),
    path('create/', views.create, name='create'),

]