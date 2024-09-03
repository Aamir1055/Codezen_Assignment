from rest_framework import permissions

class IsCustomerOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a customer to view it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is the owner of the customer object
        return obj.user == request.user
