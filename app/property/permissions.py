from rest_framework import permissions

class IsReviewOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self,request,view):
        """Allow all authenticated users to view the reviews and retrieve individual review"""
        if view.action in ['list','retrieve']:
            return request.user.is_authenticated

        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner of the review
        return obj.user == request.user
