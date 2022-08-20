import django.urls
from . import views as covid_views


urlpatterns = [
    django.urls.path('api/v1/subscribe/<str:slug>', covid_views.CountrySubscribe.as_view(), name='Add'),
    django.urls.path('api/v1/percentage/<str:first_value>/<str:second_value>/<str:slug>', covid_views.ViewPercentage.as_view(), name="C/D Percentage"),
    django.urls.path('api/v1/top/<str:case>', covid_views.TopCountries.as_view(), name="Top Countries Optional"),
    django.urls.path('api/v1/top/<str:case>/<int:number>', covid_views.TopCountries.as_view(), name="Top Countries"),
    django.urls.path('import-countries/', covid_views.import_countries, name='Add Countries'),
    django.urls.path('api/v1/topdate/<str:from>/<str:to>/<str:case>', covid_views.TopCountriesByDate.as_view(), name='Top Countries by Date Optional'),
    django.urls.path('api/v1/topdate/<str:from>/<str:to>/<str:case>/<int:number>', covid_views.TopCountriesByDate.as_view(), name='Top Countries by Date')]
