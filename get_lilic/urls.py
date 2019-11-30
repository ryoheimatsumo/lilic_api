from django.urls import path
from django.contrib import admin
from get_lilic import views

app_name = 'get_lilic'

urlpatterns=[
    path('get_lilic/',views.GetLilicApiView.as_view(),),

]
