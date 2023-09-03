from django.urls import path
from .views import *

app_name = 'conversation'

urlpatterns = [
    path('new/<int:item_pk>/', newConversation, name='new'),
    path('', chats, name='chats'),
    path('<int:pk>/', detail, name='detail'),
]