from django.urls import path
from tracker.views import *

urlpatterns = [
    path('', index, name="index"),
    path('register/', registration, name='registration'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('delete-transaction/<uid>/', deleteTransaction, name="delete-transaction"),
]