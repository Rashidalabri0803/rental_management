from django.urls import path
from . import views 
app_name = 'rental'
urlpatterns = [
    path('builings/', views.BuildingListView.as_view(), name='building_list'),
]