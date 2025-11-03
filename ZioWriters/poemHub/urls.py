from django.urls import path
from .views import (
    LipaNaMpesaStkPush,
    PoemCreateView,          
    PoemListView,           
    PaymentTransactionView,  
)
from django.http import HttpResponse

def poemHub_home(request):
    return HttpResponse("Welcome to ZIOWRITERS")

urlpatterns = [
    path('', poemHub_home, name='poenHub-home'),  
    path('stkpush/', LipaNaMpesaStkPush.as_view(), name='stkpush'),
    path('poems/', PoemCreateView.as_view(), name='poem-create'),  
    path('poems/list/', PoemListView.as_view(), name='poem-list'), 
    path('transactions/', PaymentTransactionView.as_view(), name='payment-transactions'),
]
