from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='listings'), #index method
    path('<int:listing_id>', views.listing, name='listing'), #listing method listings/12
    path('search', views.search, name='search'), #search method listings/search

]
