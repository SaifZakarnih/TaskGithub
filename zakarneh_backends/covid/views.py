import datetime
import rest_framework.response
from . import models as covid_models
import requests
import rest_framework.generics


class ImportCountries(rest_framework.generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        country_list = requests.get('https://api.covid19api.com/countries')
        for current_country in country_list.json():
            if not covid_models.Covid19APICountry.objects.filter(remote_slug=current_country["Slug"]).exists():
                print(current_country["Country"])
                covid_models.Covid19APICountry.objects.create(remote_slug=current_country["Slug"],
                                                              remote_country=current_country["Country"])
            else:
                covid_models.Covid19APICountry.objects.all().filter(remote_slug=current_country["Slug"]).update(
                    remote_slug=current_country["Slug"], remote_country=current_country["Country"])
            return rest_framework.response.Response("All {count} countries have been added/updated successfully".format(count=len(country_list.json())))


class CountrySubscribe(rest_framework.generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        country_slug = self.kwargs['slug']
        all_slugs = covid_models.Covid19APICountry.objects.values_list('remote_slug')
        all_slugs = list(all_slugs)
        country_object = covid_models.Covid19APICountry.objects.filter(remote_slug=country_slug)
        if country_object.exists():
            exist_check = covid_models.Covid19APICountryUserAttribution.objects.all().filter(user=request.user, covid_19_api_country=country_object[0]).exists()
            if exist_check:
                return rest_framework.response.Response("Country {input} for user {user} already exists!".format(input=str(country_object[0]), user=str(request.user)))
            elif not exist_check:
                created_object = covid_models.Covid19APICountryUserAttribution.objects.create(
                    user=request.user,
                    covid_19_api_country=covid_models.Covid19APICountry.objects.get(remote_slug=country_slug))
                result_dictionary = {
                    "Status": "Subscribed!",
                    "User": str(created_object.user),
                    "Country": str(created_object.covid_19_api_country),
                }
                return rest_framework.response.Response(result_dictionary)
        else:
            return rest_framework.response.Response("Invalid input {input}, please use one of these keys {keys}".format(input=self.kwargs['slug'], keys=all_slugs))


class ViewPercentage(rest_framework.generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        country_information = requests.get("https://api.covid19api.com/total/dayone/country/{key}".format(
            key=self.kwargs['slug'])).json()
        first_value = self.kwargs['first_value'].title()
        second_value = self.kwargs['second_value'].title()
        last_entry = country_information[(len(country_information)-1)]
        percentage = (last_entry[first_value] / last_entry[second_value]) * 100
        percentage = str(percentage) + "%"
        result_dictionary = {
            "Country": last_entry['Country'],
            first_value: last_entry[first_value],
            second_value: last_entry[second_value],
            "Percentage": percentage
        }
        return rest_framework.response.Response(result_dictionary)


class TopCountries(rest_framework.generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        case = self.kwargs['case'].title()
        case = "Total" + case
        country_list = requests.get("https://api.covid19api.com/summary").json()
        new_list = sorted(country_list['Countries'], key=lambda d: d[case], reverse=True)
        result_dictionary = {}
        result_list = []
        for current_country in range(self.kwargs['number']):
            result_dictionary['Country'] = new_list[current_country]['Country']
            result_dictionary[case] = new_list[current_country][case]
            result_list.append(result_dictionary)
            result_dictionary = {}
        return rest_framework.response.Response(result_list)


class TopCountriesByDate(rest_framework.generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        first_date = datetime.datetime.strptime(self.kwargs['from'], "%Y-%m-%d")
        second_date = datetime.datetime.strptime(self.kwargs['to'], "%Y-%m-%d")
        case = self.kwargs['case'].title()
        if case not in ("Confirmed", "Deaths", "Recovered"):
            return rest_framework.response.Response("Case must be 'confirmed', 'recovered' or 'deaths' not {case}".format(case=case))
        if first_date > second_date:
            return rest_framework.response.Response("Please enter a proper date range, {first_date} is after {second_date}".format(first_date=str(first_date).split(" ")[0], second_date=str(first_date).split(" ")[0]))
        first_date = first_date - datetime.timedelta(days=1)
        date_difference = second_date - first_date
        date_difference = str(date_difference)[0]
        date_difference = int(date_difference) + 1
        first_date = str(first_date)
        first_date = first_date.split(" ")
        second_date = str(second_date)
        second_date = second_date.split(" ")
        real_first_date = first_date[0]
        real_second_date = second_date[0]
        attribution_list = covid_models.Covid19APICountryUserAttribution.objects.all()
        result_list = []
        for current_object in attribution_list:
            current_country = covid_models.Covid19APICountry.objects.filter(remote_country=current_object.covid_19_api_country)
            country_information = requests.get("https://api.covid19api.com/country/{slug}/status/{case}?from={first_date}&to={second_date}".format(
                slug=current_country[0].remote_slug,
                case=case.lower(),
                first_date=real_first_date,
                second_date=real_second_date)).json()
            result_dictionary = {}
            sum_of_cases = 0
            previous_country = 0
            for current_day in country_information[1:]:
                sum_of_cases = sum_of_cases + (current_day['Cases'] - country_information[previous_country]['Cases'])
                previous_country += 1
            result_dictionary['Country'] = current_day['Country']
            result_dictionary[case] = sum_of_cases
            if result_dictionary not in result_list:
                result_list.append(result_dictionary)

        result_list = sorted(result_list, key=lambda d: d[case], reverse=True)

        return rest_framework.response.Response(result_list[:self.kwargs['number']])
