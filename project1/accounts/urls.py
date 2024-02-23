
from django.urls import path
from . import views
from accounts.views import UserRegistrationView, UserLoginView

app_name = 'accounts'
urlpatterns = [
    # path('login/', views.login, name='login'),
    path('login/', UserLoginView.as_view(), name='login'),         # 로그인
    path('logout/', views.logout, name='logout'),
    path('signup/',  UserRegistrationView.as_view(), name='signup'),
    path('delete/',views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('manage_board/', views.manage_board, name="manage_board"),
    path('follow/<int:user_pk>/', views.follow, name='following'),
    path('<int:user_pk>/', views.profile, name='profile'),
    
]