from rest_framework import permissions
from bookmarks.models import Click
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif type(obj) == Click:
            return request.user == obj.user_id
        elif type(obj) == User:
            return request.user == obj
        else:
            return request.user == obj.user