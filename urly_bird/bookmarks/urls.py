"""urly_bird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from bookmarks import views as bm_views

urlpatterns = [
    url(r'^$', bm_views.AllBookmarksView.as_view(), name="all_bookmarks"),
    url(r'^(?P<bm_id>\d+)$', bm_views.ShowBookmarkDetailView.as_view(), name="show_bookmark"),
    url(r'^add$', bm_views.AddBookmarkView.as_view(), name="add_bookmark"),
    url(r'^update/(?P<bm_id>\d*)$', bm_views.BookmarkUpdate.as_view(), name="update_bookmark"),
    url(r'^delete/(?P<bm_id>\d+)$', bm_views.BookmarkDelete.as_view(), name='delete_bookmark'),

]
