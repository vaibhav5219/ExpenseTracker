from django.urls import path
from tracker.views import *

urlpatterns = [
    path('', index, name="index"),
    path('/delete-transaction/<uid>/', deleteTransaction, name="delete-transaction"),
]