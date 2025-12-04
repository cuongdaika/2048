from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('single/', views.single_player_view, name='single_player'),
    path('hard/', views.hard_mode_view, name='hard_mode'),
    path('local-pvp/', views.local_pvp_view, name='local_pvp'),
    path('ai-game/', views.ai_game_view, name='ai_game'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/move/', views.move_api, name='move_api'),
    path('api/ai-move/', views.ai_move_api, name='ai_move_api'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('room/<str:room_code>/', views.room, name='room'),
]
