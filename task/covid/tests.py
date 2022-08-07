from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):

    # Perfect scenario! #200
    def test_registration_correct(self):

        data = {"username": "testcase", "password": "123", "email": "testcase@gmail.com"}
        response = self.client.post("/api/register/", data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # Missing Password! #400
    def test_registration_missing_data(self):

        data = {"username": "testcase2", "email": "testcase@gmail.com"}
        response = self.client.post("/api/register/", data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Incorrect email! #400
    def test_registration_incorrect_email(self):

        data = {"username": "testcase", "password": "123", "email": "testcase@"}
        response = self.client.post("/api/register/", data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)