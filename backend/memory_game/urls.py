from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('select-level/', views.select_level, name='select_level'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('game/<str:level>/', views.game_board, name='game_board'),
    path('save-stats/', views.save_stats, name='save_stats'),
    path('stats/', views.stats_view, name='stats'),
]
