from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids
from faker import Factory
import random

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    desc = models.CharField(max_length=255, null=True, blank=True)
    marked_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    url = models.URLField(null=True)
    hash_id = models.CharField(max_length=150, null=True)
    tags = models.ManyToManyField(Tag)

    # def get_absolute_url(self):
    #     return reverse('show_update', kwargs={"update_id": self.id})

    def __str__(self):
        return "{}".format(self.title)

    @property
    def get_tags(self):
        return [tag.name for tag in self.tags.all()]


class Click(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True)
    bookmark = models.ForeignKey(Bookmark)
    time = models.DateTimeField()

    def __str__(self):
        return "{}: {}".format(self.bookmark, self.time)


def create_bookmarks():
    fake = Factory.create()
    hashids = Hashids(salt='saltstring')
    for user in User.objects.all():
        for _ in range(35):
            description = fake.text(max_nb_chars=120)
            time = fake.date_time_between(start_date="-90d", end_date="now")
            title = fake.color_name()
            url = fake.url()
            new_bm = Bookmark(user=user, desc=description, marked_at=time, title=title, url=url)
            new_bm.save()
            hash = hashids.encode(new_bm.id)
            new_bm.hash_id = hash
            new_bm.save()


def create_clicks():
    fake = Factory.create()
    for bookmark in Bookmark.objects.all():
        num_clicks = random.randint(10,60)
        for _ in range(num_clicks):
            user_id = User.objects.order_by('?').first()
            bm = bookmark
            time = fake.date_time_between(start_date=bookmark.marked_at, end_date="now")
            new_click = Click(user_id=user_id, bookmark=bm, time=time)
            new_click.save()

def create_tags():
    topics = ['sports', 'cooking', 'running', 'reading', 'TV', 'movies', 'programming', 'swimming', 'crafting',
              'DIY', 'hiking', 'camping', 'traveling', 'jobs', 'animals', 'history', 'math', 'science', 'languages',
              'baking', 'woodworking', 'music', 'singing', 'events', 'beer', 'food', 'sightseeing']
    for topic in topics:
        new_top = Tag(name = topic)
        new_top.save()
    for bookmark in Bookmark.objects.all():
        num_topics = random.randint(1,4)
        tags = list(Tag.objects.all().order_by('?')[:num_topics])
        bookmark.tags = tags
        bookmark.save()
