# jobs/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Admin can do everything. Everyone else can only read."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAuthenticatedOrPostOnly(BasePermission):
    """Anyone can POST. Only admin can do other actions."""

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff


class IsJobOwner(BasePermission):
    """
    Object-level permission.

    has_permission  = runs BEFORE the view, checks general access
    has_object_permission = runs AFTER the object is fetched,
                            checks if user can touch THIS specific object
    """

    def has_permission(self, request, view):
        # User must at least be logged in

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj = the specific Job instance being accessed.
        This runs when you call self.get_object() in the view.
        """

        # For write actions, user must be the creator
        return obj.created_by == request.user
        #              ↑
        #    Compare the job's creator with the request user
        #    Only passes if they are the same person

class IsJobOwnerOrAdmin(BasePermission):
    """
    Object-level permission.

    has_permission  = runs BEFORE the view, checks general access
    has_object_permission = runs AFTER the object is fetched,
                            checks if user can touch THIS specific object
    """

    def has_permission(self, request, view):
        # User must at least be logged in
        # Guests should not reach object level checks at all
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj = the specific Job instance being accessed.
        This runs when you call self.get_object() in the view.
        """
        # Admin can do anything
        if request.user.is_staff:
            return True

        # Read requests are fine for everyone
        if request.method in SAFE_METHODS:
            return True

        # For write actions, user must be the creator
        return obj.created_by == request.user
        #              ↑
        #    Compare the job's creator with the request user
        #    Only passes if they are the same person