from django.urls import path
from django.views.decorators.http import require_POST

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_url'),
    path('dict-new/', views.DictNew.as_view(), name='dict_new_url'),
    path('dict-view/<slug:slug>/', views.DictView.as_view(), name='dict_view_url'),
    path('dict-learn/<slug:slug>/<int:pk>/', views.DictLearnView.as_view(), name='dict_learn_url'),
    path('card-handle/<int:pk>/', views.CardHandle.as_view(), name='card_handle_url'),
    path('dict-view/<slug:slug>/', views.DictView.as_view(), name='card_new_url'),
    path('bot_handler/', views.bot_handler, name='bot_handler_url'),
    path('bot_word/<int:pk>/<str:mode>', views.EditBotWord.as_view(), name='edit_bot_word_url'),

]
