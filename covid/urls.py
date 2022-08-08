from django.urls import path
from .views import RegisterAPI, LoginAPI, AddCountry, ViewPercentage, TopThreeCountries
from knox import views as knox_views


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/add/', AddCountry.as_view(), name='Add'),
    path('api/percentage/', ViewPercentage.as_view(), name="Percentage"),
    path('api/top3/', TopThreeCountries.as_view(), name="Top3"),
    #path('api/top3date/', TopThreeCountriesWithDate.as_view(), name="Top3Dates")
]