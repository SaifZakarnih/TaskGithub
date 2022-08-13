import django.contrib.postgres.fields
import django.db.models
import django.contrib.auth.models
import shortuuidfield
import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(django.contrib.auth.models.AbstractUser):
    pass


class Covid19APICountry(django.db.models.Model):
    uuid = shortuuidfield.ShortUUIDField(primary_key=True)
    remote_slug = django.db.models.CharField(max_length=100)
    remote_country = django.db.models.CharField(max_length=100)

    def __str__(self):
        return str(self.remote_country)


class Covid19APICountryUserAttribution(django.db.models.Model):
    user = django.db.models.ForeignKey(User, on_delete=django.db.models.CASCADE)
    covid_19_api_country = django.db.models.ForeignKey(Covid19APICountry, on_delete=django.db.models.CASCADE)
    attributed_on = django.db.models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        unique_together = ('user', 'covid_19_api_country')

    def __str__(self):
        user_name = str(self.user)
        country = str(self.covid_19_api_country)
        display_value = user_name + ": " + country
        return display_value


class CountryStatusDay(django.db.models.Model):
    covid_19_country = django.db.models.ForeignKey(Covid19APICountry, on_delete=django.db.models.CASCADE)
    day = django.db.models.DateField()
    count_cases_confirmed = django.db.models.IntegerField()
    count_cases_recovered = django.db.models.IntegerField()
    count_cases_deaths = django.db.models.IntegerField()
    count_cases_active = django.db.models.IntegerField()

    class Meta:
        unique_together = ('covid_19_country', 'day')

    def __str__(self):
        country = str(self.covid_19_country)
        day = str(self.day)
        display_value = country + ": " + day
        return display_value


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
