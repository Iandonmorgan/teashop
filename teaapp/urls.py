from django.urls import path
from teaapp import views
from .views import *

app_name = "teaapp"
urlpatterns = [
    path('', home, name='home'),
]
