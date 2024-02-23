
from django.urls import path
from . import views

app_name = 'plans'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path(
        '<int:plan_pk>/comments/<int:comment_pk>/delete/',
        views.comments_delete,
        name='comments_delete',
    ),
    path('<int:plan_pk>/likes/', views.likes, name='likes'),
    path('<int:plan_pk>/likes/<int:comment_pk>/', views.likes_comment, name='likes_comment'),
]