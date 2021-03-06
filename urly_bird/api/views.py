from bookmarks.models import Bookmark, Click
from users.models import Profile
from api.permissions import IsOwnerOrReadOnly, MakeNewUser
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, filters
from api.serializers import ClickSerializer, UserSerializer, BookmarkSerializer, ProfileSerializer
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
import django_filters


class BookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(name="title", lookup_type="icontains")
    desc = django_filters.CharFilter(name="desc", lookup_type="icontains")
    user = django_filters.CharFilter(name="user", lookup_type="exact")

    class Meta:
        model = Bookmark
        fields = ['title', 'desc', 'user']


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all().annotate(click_count=Count('clicks'))
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BookmarkFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (MakeNewUser,)

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.request.user.id)
        return queryset


class ClickListCreateView(generics.ListCreateAPIView):
    serializer_class = ClickSerializer

    def initial(self, request, *args, **kwargs):
        self.bookmark = Bookmark.objects.get(pk=kwargs['pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return Click.objects.filter(bookmark__id=self.kwargs['pk'])

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(user_id=self.request.user, bookmark=self.bookmark)
        else:
            serializer.save(user_id=User.objects.filter(username='Anonymous')[0], bookmark=self.bookmark)


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



