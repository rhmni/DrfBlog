from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            return obj.author == request.user
