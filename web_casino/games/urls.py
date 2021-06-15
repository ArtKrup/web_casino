from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.redirct),
    path('games/', GamesHome.as_view(), name='home'),
    path('game/<slug:slug_game>/', ShowGame.as_view(), name='game'),
    path('game/category/<slug:cat_slug>/', GamesCategory.as_view(), name='category'),
    path('about/', views.about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('feedback/', ContactFormView.as_view(), name='feedback'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('assistant/bj_start/', HandFormView.as_view(), name='bj_start'),
    path('assistant/bj_result/<int:pk>/', BjResult.as_view(), name='bj_result'),
    path('assistant/statistic/', HandStatistic.as_view(), name='statistic')


    # path('assistant/ar_start', views.ar_start, name='ar_start'),
    # path('assistant/ar_result', views.ar_result, name='ar_result'),
    # path('statistic/bj', views.statistic_bj, name='statistic_bj'),
    # path('statistic/ar', views.statistic_ar, name='statistic_ar'),
]