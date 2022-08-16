import django.contrib.admin
from . import models as covid_models
import django.contrib.auth.admin


django.contrib.admin.site.register(covid_models.Covid19APICountryUserAttribution)
django.contrib.admin.site.register(covid_models.CountryStatusDay)
django.contrib.admin.site.register(covid_models.Covid19APICountry)
django.contrib.admin.site.register(covid_models.User, django.contrib.auth.admin.UserAdmin)
