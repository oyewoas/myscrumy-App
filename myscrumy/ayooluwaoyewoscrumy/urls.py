from django.urls import path,include
from django.contrib.auth import views as auth_views


from . import views

app_name = 'ayooluwaoyewoscrumy'
urlpatterns = [
    path('', views.index, name='index'),
    path('scrumygoals/', views.scrumygoals, name='scrumygoals'),
    path('specificscrumygoal/', views.specificgoal, name='specificgoal'),
    path('movegoal/<int:goal_id>/', views.move_goals, name='movegoals'),
    path('addgoal/', views.add_goal, name='addgoal'),
    path('home/', views.home, name='home'),
    path('homepage/', views.homepage, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
]
