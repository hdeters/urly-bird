from django.contrib import admin
from .models import Bookmark, Click

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'marked_at', 'hash_id', 'get_tags']

class ClickAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'bookmark', 'time']

# Register your models here.

admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Click, ClickAdmin)
