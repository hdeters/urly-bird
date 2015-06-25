from django.db import models
from django.contrib.auth.models import User
from bookmarks.models import Bookmark, Click
from faker import Factory
import random

# Create your models here.

class Profile(models.Model):
    location = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    interests = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return str(self.user)


def delete_data():
    Click.objects.all().delete()
    Bookmark.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()


def create_profiles():
    fake = Factory.create()
    topics = ['sports', 'cooking', 'running', 'reading', 'TV', 'movies', 'programming', 'swimming', 'crafting',
              'DIY', 'hiking', 'camping', 'traveling', 'jobs', 'animals', 'history', 'math', 'science', 'languages',
              'baking', 'woodworking', 'music', 'singing', 'events', 'beer', 'food', 'sightseeing']
    for user in User.objects.all():
        a = random.randint(18, 100)
        loc = fake.state()
        activity = random.choice(topics)
        new_profile = Profile(location=loc, age=a, interests=activity, user=user)
        new_profile.save()


def create_users():
    fake = Factory.create()
    for _ in range(100):
        user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password')
        user.save()
