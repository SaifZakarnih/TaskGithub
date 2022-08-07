import datetime
from django.contrib.auth import login
from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from knox.views import LoginView as KnoxLoginView
from .models import Country
import requests


# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class AddCountry(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Country.objects.filter(userName=request.user).exists():
            Country.objects.filter(userName=request.user).update(countryName=request.data['countryName'])
            return HttpResponse("Entry already exists, information overridden!")
        else:
            serializer.save(userName=request.user)
            return HttpResponse("New Countries Saved!")


# Requirement 3!
class ViewPercentage(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        input_country = request.data
        cSlug = ()
        cName = ()
        country = requests.get('https://api.covid19api.com/countries')
        for x in country.json():
            cSlug = cSlug + (f'{x["Slug"]}',)
            cName = cName + (f'{x["Country"]}',)
        finalTuple = zip(cSlug, cName)
        country_dict = dict(finalTuple)
        if input_country in country_dict.values():
            key = list(country_dict.keys())[list(country_dict.values()).index(input_country)]
            raw_information = requests.get("https://api.covid19api.com/total/dayone/country/{slug}".format(slug=key))
            raw_information = raw_information.json()
            f = 0
            recovered = 0
            x = raw_information[len(raw_information)-1]
            confirmed = x['Confirmed']
            for y in raw_information[30:]:
                if y['Recovered'] == 0:
                    f = y['Date']
                    break
            date_of_0 = f.split("T")
            previous_date = datetime.datetime.strptime(date_of_0[0], '%Y-%m-%d')
            previous_date = previous_date - datetime.timedelta(days=1)
            string_date = str(previous_date)
            string_date = string_date.split(" ")
            actual_date = string_date[0]
            actual_date2 = actual_date + "T00:00:00Z"
            for y in raw_information[30:]:
                if y['Date'] == actual_date2:
                    recovered = y["Recovered"]
                    break
            percentage = (recovered / confirmed) * 100
            return HttpResponse("Total recovered cases: " + str(recovered) + "\nTotal confirmed cases: " + str(confirmed) + "\n"
                                "Percentage of recovered over confirmed in "
                                ""+input_country+": "+str(format(percentage, ".4f")) + "%"
                                + "\n***DATA MAY BE INACCURATE DUE TO THE API NOT REGISTERING RECOVERED CASES AFTER:"
                                  " " + actual_date+"***")
        else:
            return HttpResponse('Please insert a proper country name, example: "South Africa"')


class TopThreeCountries(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        case = request.data
        case = str(case)
        case = str.lower(case)
        list_of_data = requests.get("https://api.covid19api.com/summary")
        new_list_of_data = list_of_data.json()
        country_total = []
        if case == "confirmed":
            for x in new_list_of_data['Countries']:
                country_total.append(x['TotalConfirmed'])
            sorted_list = sorted(country_total, reverse=True)
            country_names = []
            for y in new_list_of_data['Countries']:
                if y['TotalConfirmed'] in {sorted_list[0], sorted_list[1], sorted_list[2]}:
                    country_names.append(y['Country'])
            return HttpResponse(f"Top 3 total confirmed cases are: {country_names[2]} with {sorted_list[0]} cases, "
                                f"{country_names[1]} with {sorted_list[1]} cases "
                                f"and {country_names[0]} with {sorted_list[2]} cases.")
        elif case == "deaths":
            for x in new_list_of_data['Countries']:
                country_total.append(x['TotalDeaths'])
            sorted_list = sorted(country_total, reverse=True)
            country_names = []
            for y in new_list_of_data['Countries']:
                if y['TotalDeaths'] in {sorted_list[0], sorted_list[1], sorted_list[2]}:
                    country_names.append(y['Country'])
            return HttpResponse(f"Top 3 total deaths  are: {country_names[2]} with {sorted_list[0]} deaths, "
                                f"{country_names[0]} with {sorted_list[1]} deaths "
                                f"and {country_names[1]} with {sorted_list[2]} deaths.")

        elif case == "recovered":
            # country_name = []
            # cSlug = ()
            # country = requests.get('https://api.covid19api.com/countries')
            # for x in country.json():
            #     cSlug = cSlug + (f'{x["Slug"]}',)
            # for x in cSlug:
            #     recovered_link = requests.get("https://api.covid19api.com/total/dayone/country/{x}".format(x=x))
            #     recovered_link = recovered_link.json()
            #     for y in recovered_link[30:]:
            #         if y['Recovered'] == 0:
            #             date_of_0 = y['Date']
            #             date_of_0 = date_of_0.split("T")
            #             previous_date = datetime.datetime.strptime(date_of_0[0], '%Y-%m-%d')
            #             previous_date = previous_date - datetime.timedelta(days=1)
            #             string_date = str(previous_date)
            #             string_date = string_date.split(" ")
            #             actual_date = string_date[0]
            #             actual_date2 = actual_date + "T00:00:00Z"
            #             for z in recovered_link[30:]:
            #                 if z['Date'] == actual_date2:
            #                     country_total.append(z["Recovered"])
            #                     country_name.append(z["Country"])
            #                     break
            #         break
            return HttpResponse("Recovered data are no longer registered at some point, total recovered equals 0 "
                                "Looping through all of the countries resulted in: "
                                "'message': 'Too Many Requests on /total/dayone/country/latvia. "
                                "Please upgrade to a subscription at https://covid19api.com/#subscribe', "
                                "'success': False")
        else:
            return HttpResponse('Please insert "confirmed", "deaths" or "recovered"')

#Requirement # 5 , I don't know if possible.
# class TopThreeCountriesWithDate(generics.GenericAPIView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request, *args, **kwargs):
#         all_information = request.data
#         all_information["case"] = str.lower((all_information.get("case")))
#         try:
#             a = datetime.datetime.strptime(all_information["from_date"], '%Y-%m-%d')
#             b = datetime.datetime.strptime(all_information["to_date"], '%Y-%m-%d')
#         except:
#             raise ValueError("Incorrect Date Format, should be YYYY-MM-DD!")
#         delta = b - (a - timedelta(days=1))
#         if delta.days > 7:
#             return HttpResponse("Range must be less than 7 days!")
#         list_of_data = requests.get("https://api.covid19api.com/summary?from={from_date}T00:00:00Z&to={to_date}T00:00:01Z".format(
#             from_date=str((a - timedelta(days=1))), to_date=all_information.get("to_date")))
#         new_list_of_data = list_of_data.json()
#         return HttpResponse(new_list_of_data['Countries'])
#         country_total = []
#         if all_information.get("case") == "confirmed":
#             for x in new_list_of_data['Countries']:
#
#
#         elif all_information.get("case") == "deaths":
#             for x in new_list_of_data['Countries']:
#                 print(x['NewDeaths'])
#                 country_total.append(x['NewDeaths'])
#             sorted_list = sorted(country_total, reverse=True)
#             print(sorted_list)
#             country_names = []
#             for y in new_list_of_data['Countries']:
#                 if y['NewDeaths'] in {sorted_list[0], sorted_list[1], sorted_list[2]}:
#                     country_names.append(y['Country'])
#             return HttpResponse(f"Top 3 total deaths date range {all_information.get('from_date')} to"
#                                 f"{all_information.get('to_date')} are: {country_names[2]} with {sorted_list[0]} deaths, "
#                                 f"{country_names[0]} with {sorted_list[1]} deaths "
#                                 f"and {country_names[1]} with {sorted_list[2]} deaths.")
#
#         elif all_information.get("case") == "recovered":
#             return HttpResponse("Summary link gives straight 0's, decided not to loop through 10k+ cases.")
#         else:
#             return HttpResponse('Please insert "confirmed", "deaths" or "recovered"')