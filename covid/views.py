import datetime
import rest_framework.response
import rest_framework.decorators
import rest_framework.permissions
import rest_framework.views
from django.db.models import Max, Min
import django.core.management
from . import models as covid_models
import requests
import rest_framework.generics


class ImportCountries(rest_framework.views.APIView):

    permission_classes = [rest_framework.permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        country_list = requests.get('https://api.covid19api.com/countries')
        for current_country in country_list.json():
            queryset = covid_models.Covid19APICountry.objects.filter(remote_slug=current_country['Slug'])
            if not queryset.exists():
                covid_models.Covid19APICountry.objects.create(remote_slug=current_country["Slug"],
                                                              remote_country=current_country["Country"])
            else:
                queryset.update(
                    remote_slug=current_country["Slug"], remote_country=current_country["Country"])
        return rest_framework.response.Response(status=201)


class CountrySubscribe(rest_framework.generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        country_slug = self.kwargs['slug']
        all_slugs = covid_models.Covid19APICountry.objects.values_list('remote_slug', flat=True)
        country_object = covid_models.Covid19APICountry.objects.filter(remote_slug=country_slug)
        if country_object.exists():
            exist_check = covid_models.Covid19APICountryUserAttribution.objects.filter(user=request.user, covid_19_api_country=country_object[0]).exists()
            if exist_check:
                return rest_framework.response.Response(
                    f"This user is already subscribed to Country {country_object[0]}",
                    status=409
                )
            else:
                created_object = covid_models.Covid19APICountryUserAttribution.objects.create(
                    user=request.user,
                    covid_19_api_country=covid_models.Covid19APICountry.objects.get(remote_slug=country_slug))
                result_dictionary = {
                    "Status": "Subscribed!",
                    "User": str(created_object.user),
                    "Country": str(created_object.covid_19_api_country),
                }
                return rest_framework.response.Response(result_dictionary, status=201)
        else:
            return rest_framework.response.Response(f"Invalid input {country_slug}, please use one of these keys {all_slugs}", status=400)


class ViewPercentage(rest_framework.generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        if (self.kwargs['first_value'] or self.kwargs['second_value']) not in ["confirmed", "deaths", "active"]:
            return rest_framework.response.Response("Case must be confirmed, deaths, or active", status=400)
        if not covid_models.Covid19APICountry.objects.filter(remote_slug=self.kwargs['slug']):
            return rest_framework.response.Response("Incorrect country slug", status=400)
        country_information = requests.get("https://api.covid19api.com/total/dayone/country/{key}".format(
            key=self.kwargs['slug'])).json()
        first_value = self.kwargs['first_value'].title()
        second_value = self.kwargs['second_value'].title()
        last_entry = country_information[(len(country_information) - 1)]
        try:
            percentage = str((last_entry[first_value] / last_entry[second_value]) * 100) + '%'
        except ZeroDivisionError:
            percentage = "Division by Zero"
        result_dictionary = {
            "Country": last_entry['Country'],
            first_value: last_entry[first_value],
            second_value: last_entry[second_value],
            "Percentage": percentage
        }
        return rest_framework.response.Response(result_dictionary, status=200)


class TopCountries(rest_framework.generics.GenericAPIView):

    def get(self, request, number=3, *args, **kwargs):
        if self.kwargs['case'] not in ["confirmed", "deaths"]:
            return rest_framework.response.Response("Case must be confirmed or deaths", status=400)
        case = self.kwargs['case'].title()
        case = "Total" + case
        country_list = requests.get("https://api.covid19api.com/summary").json()
        new_list = sorted(country_list['Countries'], key=lambda d: d[case], reverse=True)
        result_dictionary = {}
        result_list = []
        for current_country in range(number):
            result_dictionary['Country'] = new_list[current_country]['Country']
            result_dictionary[case] = new_list[current_country][case]
            if result_dictionary not in result_list:
                result_list.append(result_dictionary)
            result_dictionary = {}
        return rest_framework.response.Response(result_list, status=200)


class TopCountriesByDate(rest_framework.generics.GenericAPIView):

    def get(self, request, number=3, *args, **kwargs):
        try:
            first_date = datetime.datetime.strptime(self.kwargs['from'], "%Y-%m-%d")
            second_date = datetime.datetime.strptime(self.kwargs['to'], "%Y-%m-%d")
        except ValueError:
            return rest_framework.response.Response("Date must be in YYYY-MM-DD format!", status=400)
        case = self.kwargs['case'].title()
        if case not in ("Confirmed", "Deaths", "Recovered"):
            return rest_framework.response.Response(f"Case must be 'confirmed', 'recovered' or 'deaths' not {case}", status=400)
        if first_date > second_date:
            return rest_framework.response.Response(f"{str(first_date).split(' ')[0]} must not be after {str(second_date).split(' ')[0]}", status=400)
        attribution_list = covid_models.Covid19APICountryUserAttribution.objects.all()
        countries_list = []
        result_list = []
        result_dictionary = {}
        for attribute in attribution_list:
            if covid_models.CountryStatusDay.objects.filter(covid_19_country=attribute.covid_19_api_country).exists():
                countries_list.append(attribute.covid_19_api_country)
        set(countries_list)
        for current_country in range(len(countries_list)):
            attribute_list = covid_models.CountryStatusDay.objects\
                .filter(covid_19_country=countries_list[current_country],
                        day__range=[self.kwargs['from'], self.kwargs['to']])\
                .aggregate(difference=(
                    Max(("count_cases_"+self.kwargs['case'])) - Min(("count_cases_"+self.kwargs['case'])))
                )
            result_dictionary['Country'] = str(countries_list[current_country])
            result_dictionary[case] = attribute_list['difference']
            result_list.append(result_dictionary)
            result_dictionary = {}
        result_list = sorted(result_list, key=lambda d: d[case], reverse=True)
        return rest_framework.response.Response(result_list[:number], status=200)
