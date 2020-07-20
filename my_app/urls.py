from django.urls import path
from . import views

urlpatterns = [
    # leave empty string for your base(homepage) URL
    path('',views.base,name='base'),
    path('new_search',views.new_search,name ='new_search')
]
