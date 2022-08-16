import django.urls
from . import views as covid_views


urlpatterns = [
    django.urls.path('api/v1/subscribe/<str:slug>', covid_views.CountrySubscribe.as_view(), name='Add'),
    django.urls.path('api/v1/percentage/<str:first_value>/<str:second_value>/<str:slug>', covid_views.ViewPercentage.as_view(), name="C/D Percentage"),
    django.urls.path('api/v1/top/<int:number>/<str:case>', covid_views.TopCountries.as_view(), name="Top Countries"),
    django.urls.path('import-countries/', covid_views.ImportCountries.as_view(), name='Add Countries'),
    django.urls.path('api/v1/topbydate/<int:number>/<str:from>/<str:to>/<str:case>', covid_views.TopCountriesByDate.as_view(), name='Top Countries by Date')]
