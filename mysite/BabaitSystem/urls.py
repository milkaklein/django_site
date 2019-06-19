from django.urls import path

from . import views

app_name = 'BabaitSystem'
urlpatterns = [

    path('search/', views.search, name='search'),
    path('<int:product_id>/find/', views.find, name='find'),
    path('result_info', views.result_info, name='result_info'),
    path('prices_in_past', views.prices_in_past, name='prices_in_past'),

]

