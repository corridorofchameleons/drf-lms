from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
