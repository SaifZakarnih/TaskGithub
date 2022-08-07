import requests
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django import forms


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Country(models.Model):
    cSlug = ()
    cName = ()
    y = 0
    country = requests.get('https://api.covid19api.com/countries')
    for x in country.json():
        cSlug = cSlug + (f'{x["Slug"]}',)
        cName = cName + (f'{x["Country"]}',)
    finalTuple = zip(cSlug, cName)
    countryName = ChoiceArrayField(
            models.CharField(max_length=100, choices=finalTuple),
            size=3,
        )
    userName = models.OneToOneField(User, on_delete=models.CASCADE, null=True, serialize=False)

    def __repr__(self):
        return self.__str__()


class CountryInfo(models.Model):
    country_name = models.CharField(max_length=100, primary_key=True)
    country_deaths = models.IntegerField()
    country_recovered = models.IntegerField()
    country_confirmed = models.IntegerField()
    country_actives = models.IntegerField()

    def __str__(self):
        return self.country_name