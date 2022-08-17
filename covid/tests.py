import unittest

import rest_framework.test
import rest_framework.authtoken.models

from . import models as covid_models
import requests


class TestSubscription(rest_framework.test.APITestCase):

    def setUp(self):
        self.username = "testcase"
        self.password = "123"
        self.email = "testcase@gmail.com"
        self.user = covid_models.User.objects.create(username=self.username, password=self.password, email=self.email)
        country_list = requests.get('https://api.covid19api.com/countries')
        for current_country in country_list.json():
            if not covid_models.Covid19APICountry.objects.filter(remote_slug=current_country["Slug"]).exists():
                covid_models.Covid19APICountry.objects.create(remote_slug=current_country["Slug"],
                                                              remote_country=current_country["Country"])
            else:
                covid_models.Covid19APICountry.objects.all().filter(remote_slug=current_country["Slug"]).update(
                    remote_slug=current_country["Slug"], remote_country=current_country["Country"])
        self.token = rest_framework.authtoken.models.Token.objects.all().filter(user=self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token[0])
        }

    def test_correct_scenario(self):
        response = self.client.post('/api/v1/subscribe/south-africa', **self.auth_headers)
        self.assertEquals(response.status_code, 201)

    def test_fake_country(self):
        response = self.client.post('/api/v1/subscribe/south-fake', **self.auth_headers)
        self.assertEquals(response.status_code, 400)

    def test_conflict_country(self):
        self.client.post('/api/v1/subscribe/south-africa', **self.auth_headers)
        response = self.client.post('/api/v1/subscribe/south-africa', **self.auth_headers)
        self.assertEquals(response.status_code, 409)


class TestPercentage(rest_framework.test.APITestCase):

    def setUp(self):
        self.username = "testcase"
        self.password = "123"
        self.email = "testcase@gmail.com"
        self.user = covid_models.User.objects.create(username=self.username, password=self.password, email=self.email)
        self.token = rest_framework.authtoken.models.Token.objects.all().filter(user=self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token[0])
        }
        country_list = requests.get('https://api.covid19api.com/countries')
        for current_country in country_list.json():
            if not covid_models.Covid19APICountry.objects.filter(remote_slug=current_country["Slug"]).exists():
                covid_models.Covid19APICountry.objects.create(remote_slug=current_country["Slug"],
                                                              remote_country=current_country["Country"])
            else:
                covid_models.Covid19APICountry.objects.all().filter(remote_slug=current_country["Slug"]).update(
                    remote_slug=current_country["Slug"], remote_country=current_country["Country"])

    def test_correct_scenario(self):
        response = self.client.get('/api/v1/percentage/deaths/active/south-africa', **self.auth_headers)
        self.assertEquals(response.status_code, 200)

    def test_incorrect_case(self):
        response = self.client.get('/api/v1/percentage/deatshs/active/bahrain', **self.auth_headers)
        self.assertEquals(response.status_code, 400)

    def test_incorrect_country(self):
        response = self.client.get('/api/v1/percentage/deaths/active/barain', **self.auth_headers)
        self.assertEquals(response.status_code, 400)

class TestTopCountries(rest_framework.test.APITestCase):

    def setUp(self):
        self.username = "testcase"
        self.password = "123"
        self.email = "testcase@gmail.com"
        self.user = covid_models.User.objects.create(username=self.username, password=self.password, email=self.email)
        self.token = rest_framework.authtoken.models.Token.objects.all().filter(user=self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token[0])
        }

    def test_correct_scenario(self):
        response = self.client.get('/api/v1/top/3/confirmed', **self.auth_headers)
        self.assertEquals(response.status_code, 200)

    def test_incorrect_case(self):
        response = self.client.get('/api/v1/top/3/fake-case', **self.auth_headers)
        self.assertEquals(response.status_code, 400)

    def test_incorrect_number(self):
        response = self.client.get('/api/v1/top/a/confirmed', **self.auth_headers)
        self.assertEquals(response.status_code, 404)

class TestByDate(rest_framework.test.APITestCase):

    def setUp(self):
        self.username = "testcase"
        self.password = "123"
        self.email = "testcase@gmail.com"
        self.user = covid_models.User.objects.create(username=self.username, password=self.password, email=self.email)
        self.token = rest_framework.authtoken.models.Token.objects.all().filter(user=self.user)
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.token[0])
        }
        self.client.post('/api/v1/subscribe/south-africa', **self.auth_headers)
        self.client.post('/api/v1/subscribe/palestine', **self.auth_headers)
        self.client.post('/api/v1/subscribe/ukraine', **self.auth_headers)

    def test_correct_scenario(self):
        response = self.client.get('/api/v1/topbydate/3/2020-05-08/2020-05-11/confirmed', **self.auth_headers)
        self.assertEquals(response.status_code, 200)

    def test_incorrect_date(self):
        response = self.client.get('/api/v1/topbydate/3/202-05-08/2020-05-11/confirmed', **self.auth_headers)
        self.assertEquals(response.status_code, 400)

    def test_ahead_date(self):
        response = self.client.get('/api/v1/topbydate/3/2020-05-11/2020-05-08/confirmed', **self.auth_headers)
        self.assertEquals(response.status_code, 400)

    def test_wrong_case(self):
        response = self.client.get('/api/v1/topbydate/3/2020-05-08/2020-05-11/fake', **self.auth_headers)
        self.assertEquals(response.status_code, 400)
