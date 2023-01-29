from django.urls import path
from . import views
app_name = "scraper"

urlpatterns = [
    path('get/<int:pk>/',views.get_csv,name="get_csv"),
    path('get/result/<int:pk>/',views.scrape,name='result'),
]