from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('cart/', views.cart, name='cart'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('list-offers/', views.list_offers, name='list_offers'),
    path('list-offers/add-product/', views.add_product, name='add_product'),
    path('list-offers/edit-offer/', views.edit_offer, name='edit_offer')
]
