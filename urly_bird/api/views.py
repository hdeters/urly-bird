from bookmarks.models import Bookmark, Click
from api.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions, generics
from api.serializers import ClickSerializer, UserSerializer, BookmarkSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from django.contrib.auth.models import User


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ClickViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ClickCreateView(generics.CreateAPIView):
    serializer_class = ClickSerializer

    def perform_create(self, serializer):
        # bookmark = serializer.data['bookmark']
        bookmark = Bookmark.objects.filter(pk=self.kwargs['pk'])[0]
        if self.request.user.is_authenticated():
            serializer.save(user_id=self.request.user, bookmark=bookmark)
        else:
            serializer.save(user_id=User.objects.filter(username='Anonymous')[0], bookmark=bookmark)
