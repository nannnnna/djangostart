from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:item_id>/', views.get_session_id, name='get_session_id'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
]