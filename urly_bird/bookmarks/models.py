from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids

# Create your models here.

class Bookmark(models.Model):
    user = models.ForeignKey(User)
    desc = models.CharField(max_length=255, null=True, blank=True)
    marked_at = models.DateTimeField()
    title = models.CharField(max_length=255)

    # def get_absolute_url(self):
    #     return reverse('show_update', kwargs={"update_id": self.id})

    def __str__(self):
        return "{}".format(self.title)

    #def get_hash_dict(self):



class Click(models.Model):
    user_id = models.ForeignKey(User)
    bookmark = models.ForeignKey(Bookmark)
    time = models.DateTimeField()

    def __str__(self):
        return "{}: {}".format(self.bookmark, self.time)


# def generate_bookmark_data:
#     def create_hash_dict(self):
#
#         hashids = Hashids()
