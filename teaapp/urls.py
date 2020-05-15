from django.urls import path
from teaapp import views
from .views import *

app_name = "teaapp"
urlpatterns = [
    path('', home, name='home'),
    path('teas', home, name='home'),
    path('teas/form', tea_form, name='tea_form'),
    path('teas/<int:tea_id>/', tea_detail, name='tea_detail'),
]
