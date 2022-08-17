import django.core.management.base
import requests
import rest_framework.response
from rest_framework import status

from ... import models as covid_models


class Command(django.core.management.base.BaseCommand):
    help = "This command registers all users' registered countries status in the database."

    def handle(self, *args, **kwargs):
        attribution_list = covid_models.Covid19APICountryUserAttribution.objects.all()
        for current_object in attribution_list:
            current_country = covid_models.Covid19APICountry.objects.filter(remote_country=current_object.covid_19_api_country)
            country_information = requests.get("https://api.covid19api.com/total/dayone/country/{key}".format(key=current_country[0])).json()
            last_entry = country_information[len(country_information) - 1]
            date = last_entry['Date']
            date = date.split('T')
            if covid_models.CountryStatusDay.objects.all().filter(covid_19_country=current_object.covid_19_api_country).exists():
                covid_models.CountryStatusDay.objects.filter(covid_19_country=current_object.covid_19_api_country).update(
                    count_cases_confirmed=last_entry['Confirmed'],
                    count_cases_recovered=last_entry['Recovered'],
                    count_cases_deaths=last_entry['Deaths'],
                    count_cases_active=last_entry['Active'],
                    day=date[0])
                self.stdout.write('Successfully updated object for {country}'.format(country=last_entry['Country']))
            else:
                covid_models.CountryStatusDay.objects.create(
                    covid_19_country=current_object.covid_19_api_country,
                    count_cases_confirmed=last_entry['Confirmed'],
                    count_cases_recovered=last_entry['Recovered'],
                    count_cases_deaths=last_entry['Deaths'],
                    count_cases_active=last_entry['Active'],
                    day=date[0])
                self.stdout.write('Successfully created object for {country}'.format(country=last_entry['Country']))

