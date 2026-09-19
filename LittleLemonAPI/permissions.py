from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.is_superuser or request.user.groups.filter(name="Manager").exists()
    
class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.groups.filter(name="Delivery crew").exists()

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        # Allow read-only (GET, HEAD, OPTIONS) for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True 
        # Require Manager or Superuser status for write operations (POST, PUT, DELETE)
        return request.user.is_superuser or request.user.groups.filter(name="Manager").exists()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
            if not (request.user and request.user.is_authenticated):
                return False
            return request.user.groups.filter(name="Customer").exists()