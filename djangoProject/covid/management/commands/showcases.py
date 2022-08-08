from datetime import date, timedelta
from sys import stdout

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import requests
from covid.models import Country, CountryInfo
from rest_framework.generics import get_object_or_404


class Command(BaseCommand):
    help = "Requirement #2 of Task"

    def add_arguments(self, parser):
        parser.add_argument("param", type=str)

    def handle(self, *args, **kwargs):
        param = kwargs.get('param')
        user = get_object_or_404(User, username=param)
        obj = Country.objects.get(userName=user.id)
        info_list = []
        for x in obj.countryName:
            recovered_sum = 0
            confirmed_sum = 0
            deaths_sum = 0
            actives_sum = 0
            country_information = requests.get(
                "https://api.covid19api.com/country/{slug}?from={today}T00:00:00Z&to={today}T00:00:01Z".format
                (slug=x,today=date.today() - timedelta(days=2)))
            json_information = country_information.json()
            if len(json_information) == 1:
                y = json_information[len(json_information) - 1]
                info_list.append("Country: ")
                info_list.append(y["Country"])
                info_list.append(" Confirmed: ")
                info_list.append(y["Confirmed"])
                info_list.append(" Recovered: ")
                info_list.append(y["Recovered"])
                info_list.append(" Deaths: ")
                info_list.append(y["Deaths"])
                info_list.append(" Active: ")
                info_list.append(y["Active"])
                if CountryInfo.objects.filter(country_name=y["Country"]).exists():
                    CountryInfo.objects.filter(country_name=y["Country"]).update(country_deaths=y["Deaths"],
                                                                                 country_actives=y["Active"],
                                                                                 country_confirmed=y["Confirmed"],
                                                                                 country_recovered=y["Recovered"])
                else:
                    CountryInfo.objects.create(country_name=y["Country"],
                                               country_deaths=y["Deaths"],
                                               country_actives=y["Active"],
                                               country_confirmed=y["Confirmed"],
                                               country_recovered=y["Recovered"]),
            else:
                country = ""
                for z in json_information:
                    recovered_sum = recovered_sum + int(z['Recovered'])
                    confirmed_sum = confirmed_sum + int(z['Confirmed'])
                    deaths_sum = deaths_sum + int(z['Deaths'])
                    actives_sum = actives_sum + int(z['Active'])
                    country = z['Country']
                info_list.append("Country: ")
                info_list.append(country)
                info_list.append(" Confirmed: ")
                info_list.append(confirmed_sum)
                info_list.append(" Recovered: ")
                info_list.append(recovered_sum)
                info_list.append(" Deaths: ")
                info_list.append(deaths_sum)
                info_list.append(" Active: ")
                info_list.append(actives_sum)
                if CountryInfo.objects.filter(country_name=country).exists():
                    CountryInfo.objects.filter(country_name=country).update(country_deaths=deaths_sum,
                                                                            country_actives=actives_sum,
                                                                            country_confirmed=confirmed_sum,
                                                                            country_recovered=recovered_sum)
                else:
                    CountryInfo.objects.create(country_name=country,
                                               country_deaths=deaths_sum,
                                               country_actives=actives_sum,
                                               country_confirmed=confirmed_sum,
                                               country_recovered=recovered_sum)
        return str(info_list)
