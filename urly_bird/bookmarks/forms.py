from django import forms
from django.contrib.auth.models import User
from bookmarks.models import Bookmark

class AddBookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('title', 'desc',)
