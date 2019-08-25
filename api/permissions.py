from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization

class IsAdminUserOrReadOnly(permissions.BasePermission):
    message = 'Only administrators are allowed to write data.'
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else: # Check permissions for write request
            if request.user.is_anonymous():
                return False
            else:
                return request.user.is_superuser


class IsEmployeeUser(permissions.BasePermission):
    """
        Custom permission to deny all non-employees that are logged in.
    """
    message = 'Only employees are allowed to access data.'
    def has_permission(self, request, view):
        # Reject Anonymous users.
        if request.user.is_anonymous():
            return False
        
        # Find employee object for the user
        try:
            Employee.objects.get(user__id=request.user.id)
            return True
        except Employee.DoesNotExist:
            return False

class DenyListingForNonEmployees(permissions.BasePermission):
    """
        Custom permission to deny all non-employees that are logged in.
        """
    message = 'Only employees are allowed to access data.'
    def has_permission(self, request, view):
        # Reject Anonymous users.
        if request.user.is_anonymous():
            return False
        
        # Find employee object for the user
        try:
            Employee.objects.get(user__id=request.user.id)
            return True
        except Employee.DoesNotExist:
            pass
                
        try:
            customer = Customer.objects.get(user=request.user)
            if request.method is 'GET':
                return False
            else:
                return True
        except Exception as e:
            return False


class UserBelongsToCustomerOrEmployee(permissions.BasePermission):
    """
        Object-level permission to allow Customers / Employees to access the
        User object only if they belong to it.
    """
    message = 'You are not owner of this object'
    def has_object_permission(self, request, view, obj):
        # Fetch the User
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return False # If no user account exists, then deny permission.

        # Confirm it belongs to Employee.
        try:
            employee = Employee.objects.get(user__id=request.user.id)
            
            # Instance must have an attribute named `organization`.
            return obj.id == employee.user.id
        except Exception as e:
            pass

        # Confirm it belongs to Customer.
        try:
            customer = Customer.objects.get(user=request.user)
            return obj.id == customer.user.id
        except Exception as e:
            return False


class IsEmployeeUserOrReadOnly(permissions.BasePermission):
    """
        Custom permission to deny all non-employees from performing writing
        actions and allow all read-only actions instead. 
    """
    message = 'Only employees are allowed to access data.'
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            # Check permissions for read-only request
            if request.method in permissions.SAFE_METHODS:
                # Note: Non-authenticated users are allowed to perform
                #       'read-only' actions on the data.
                return True
            else: # Check permissions for write request
                return False
        
        # Find employee object for the user
        try:
            Employee.objects.get(user__id=request.user.id)
            return True
        except Employee.DoesNotExist:
            return False


class BelongsToEmployee(permissions.BasePermission):
    """
        Object-level permission to only allow employees who own the object
        are thus given permission to access the employee.
    """
    message = 'Only employees who belong to the same organization are able to access data.'
    def has_object_permission(self, request, view, obj):
        try:
            employee = Employee.objects.get(user__id=request.user.id)
        
            # Instance must have an attribute named `organization`.
            return obj.employee == employee
        except Employee.DoesNotExist:
            return False

class BelongsToOrganization(permissions.BasePermission):
    """
        Object-level permission to only allow employees who belong to the
        organization (of the object) be able to access/modify the object.
        If an employee from a different organization tries to access the object
        then permission denied will occure.
    """
    message = 'Only employees who belong to the same organization are able to access data.'
    def has_object_permission(self, request, view, obj):
        employee = Employee.objects.get(user__id=request.user.id)
        
        # Instance must have an attribute named `organization`.
        return obj.organization == employee.organization

class BelongsToCompanyPolicy(permissions.BasePermission):
    """
        - (1) Must be authenticated user
        - (2a) Customer is owner of organization and of the object
        - (2b) OR Employee belongs to the organization of object
    """
    message = 'You must be authenticated as the owner of the organization or an employee of the organization.'
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False # Must be authenticated
        
        # Organizational Owners always have overriding authority of the organization.
        try:
            organization = Organization.objects.get(administrator__id=request.user.id)
            if organization is not None:
                return obj.organization == organization
        except Organization.DoesNotExist:
            pass
        
        # OR Employee belongs to organization
        try:
            employee = Employee.objects.get(user__id=request.user.id)
            return obj.organization == employee.organization
        except Employee.DoesNotExist:
            return False


class BelongsToOrganizationOwnerOrReadOnly(permissions.BasePermission):
    """
        Object-level permission to only allow owners of the organization
        to be able to write to it, else it's readable to everyone else.
    """
    message = 'Only employees who are owners of the organization are able to write data.'
    def has_object_permission(self, request, view, obj):
        # Check permissions for read-only request
        if request.method in permissions.SAFE_METHODS:
            return True # Anyone can ead object.
        else: # Check permissions for write request
            # Do not allow write for users who have not logged on.
            if request.user.is_anonymous():
                return False
        try:
            employee = Employee.objects.get(user__id=request.user.id)
            return obj.org_id == employee.organization_id and obj.administrator == employee.user
        except Employee.DoesNotExist:
            return False


class BelongsToCustomerOrIsEmployeeUser(permissions.BasePermission):
    """
        Object-level permission to only allow customers who own the object
        be able to access/modify the object OR the logged in user is an
        employee.
    """
    message = 'Only employees or customer who own this object are able to access the data.'
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False
        
        try:
            Employee.objects.get(user__id=request.user.id)
            return True
        except Employee.DoesNotExist:
            pass

        try:
            # Key Idea:
            #     The Customer and User object both need to have matching
            #     email accounts for the permissions to work properly.
            #     Therefore whenever the email gets updated, both Customer
            #     and User object NEED to have these values changed to match.
            #
            customer = Customer.objects.get(email=request.user.email)
            return obj.customer_id == customer.customer_id
        except Customer.DoesNotExist:
            return False


class BelongsToOrganizationOrReadOnly(permissions.BasePermission):
    """
        Object-level permission to only allow employees who belong to the
        organization (of the object) be able to access/modify the object.
        If an employee from a different organization tries to access the object
        then permission will only be granted for read-only actions.
    """
    message = 'Only employees who belong to the same organization are able to write data.'
    def has_object_permission(self, request, view, obj):
        # Check permissions for read-only request
        if request.method in permissions.SAFE_METHODS:
            return True # Anyone can ead object.
        else: # Check permissions for write request
            # Do not allow write for users who have not logged on.
            if request.user.is_anonymous():
                return False

        try:
            employee = Employee.objects.get(user__id=request.user.id)
        
            # Instance must have an attribute named `organization`.
            return obj.organization == employee.organization
        except Employee.DoesNotExist:
            return False

class AnonymousWriteAndIsEmployeeRead(permissions.BasePermission):
    """
        Custom permission to deny all non-employees from reading actions and 
        allow all write-only actions for anonymous users.
    """
    message = 'Only anonymous users are able to write and authenticated users are allowed to read.'
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            # Check permissions for read-only request
            if request.method in permissions.SAFE_METHODS:
                # Note: Non-authenticated users are forbidden from reading.
                return False
            else:
                return True
        
        # Find employee object for the user
        try:
            Employee.objects.get(user__id=request.user.id)
            return True
        except Employee.DoesNotExist:
            return False
