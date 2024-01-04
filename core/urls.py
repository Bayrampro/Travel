from django.urls import path, include

from Tavel import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('cities_hotels/', cities_hotels, name='cities_hotels'),
    path('tours/', tours, name='tours'),
    path('search/', Search.as_view(), name='search'),
    path('view_city/<str:slug>/', view_city, name='view_city'),
    path('view_hotel/<str:slug>/', view_hotels, name='view_hotels'),
    path('view_blog/<str:slug>/', view_blog, name='view_blog'),
    path('view_tour/<str:slug>/', view_tour, name='view_tour'),
    path('signup/', create_user, name='sign-up'),
    path('signin/', user_login, name='sign-in'),
    path('logout/', user_logout, name='logout'),
    path('explore_more/', explore_more, name='explore_more'),
    path('explore_more/<str:slug>/', view_more, name='view_more'),
    path('privacy_and_polices/', privacy, name='privacy'),
    path('about_us/', about, name='about'),
    path('weather/<str:city>/', get_weather, name='get_weather'),
    path('weekly_forecast/<str:city>/', weekly_weather_forecast, name='weekly_weather_forecast'),
    path('weekly_forecast/', weekly_forecast, name='weekly_forecast'),
]