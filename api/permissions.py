from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import SAFE_METHODS

from . import models


ADMIN = 'admin'
MODERATOR = 'moderator'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.user.role:
            return request.user.role == ADMIN or request.user.is_staff


class IsAdminWithSafe(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.user.role:
            return request.user.role == ADMIN or request.user.is_staff


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role:
            return request.user.role == MODERATOR
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role in [MODERATOR, ADMIN]:
            return True
        return obj.author == request.user
