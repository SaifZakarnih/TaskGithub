# THIS CODE IS STILL NOT EDITED!!!


# import sys
# from unittest import TestCase
# from django.contrib.auth.models import User
# from django.core.management import call_command
# from django.http import Http404
# from rest_framework.reverse import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from knox.models import AuthToken
# from django.test import Client
# from .serializers import CountrySerializer
# from covid.management.commands import showcases
# from .models import Country
#
#
# class TestAddCountry(APITestCase):
#
#     serializer_class = CountrySerializer
#
#     def setUp(self):
#         self.username = "testuser"
#         self.password = "123"
#         self.email = "testuser@gmail.com"
#         self.user = User.objects.create_user(self.username, self.email, self.password)
#
#     # Perfect Scenario! #200
#     def test_add_correct_country(self):
#         token = AuthToken.objects.create(self.user)[1]
#         self.client = Client(HTTP_AUTHORIZATION='Token ' + token)
#         response = self.client.post('/api/add/', {"countryName": ['south-africa']})
#         self.assertEquals(response.status_code, 200)
#
#     # 1 More country over the limit! #400
#     def test_add_4_countries(self):
#         token = AuthToken.objects.create(self.user)[1]
#         self.client = Client(HTTP_AUTHORIZATION='Token ' + token)
#         response = self.client.post('/api/add/', {"countryName": ['south-africa', 'gabon', 'united-states', 'ukraine']})
#         self.assertEquals(response.status_code, 400)
#
#     # Fake country! #400
#     def test_add_fake_country(self):
#         token = AuthToken.objects.create(self.user)[1]
#         self.client = Client(HTTP_AUTHORIZATION='Token ' + token)
#         response = self.client.post('/api/add/', {"countryName": ['fake_country_name']})
#         self.assertEquals(response.status_code, 400)
#
#
# class TestCustomCommand(TestCase):
#
#     def setUp(self):
#         self.username = "testuser"
#         self.password = "123"
#         self.email = "testuser@gmail.com"
#         self.user = User.objects.create_user(self.username, self.email, self.password)
#         self.c = Country.objects.create(userName=self.user, countryName=["south-africa"])
#         self.c.save()
#         self.success = False
#
#     # Perfect scenario #200
#     def test_correct_command(self):
#         var = call_command('showcases', 'testuser')
#         self.assertIn('Country', var)
