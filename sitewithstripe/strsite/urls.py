from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:item_id>/', views.get_session_id, name='get_session_id'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/', views.item_list, name='item_list'),
    path('order/', views.order, name='order'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
]