from api import views as api_views
from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'bookmarks', api_views.BookmarkViewSet, base_name='bookmark')
router.register(r'users', api_views.UserViewSet, base_name='user')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^bookmarks/(?P<pk>\d+)/click', api_views.ClickListCreateView.as_view(), name="create_click"),
    url(r'^users/(?P<pk>\d+)', api_views.ProfileRetrieveUpdateView.as_view(), name="profile_detail")
    ]