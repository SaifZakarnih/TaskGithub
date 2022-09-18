import django.contrib.admin
from . import models as covid_models
import django.contrib.auth.admin


class CountryAPIAdmin(django.contrib.admin.ModelAdmin):
    change_list_template = 'admin/custom_change_list.html'


class CountyStatusDayAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('covid_19_country', 'day')
    ordering = ('covid_19_country', 'day')
    search_fields = ('covid_19_country__remote_country', 'day')
    list_filter = ('day', ('covid_19_country', django.contrib.admin.RelatedOnlyFieldListFilter))


django.contrib.admin.site.register(covid_models.Covid19APICountryUserAttribution)
django.contrib.admin.site.register(covid_models.CountryStatusDay, CountyStatusDayAdmin)
django.contrib.admin.site.register(covid_models.Covid19APICountry, CountryAPIAdmin)
django.contrib.admin.site.register(covid_models.User)
