from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

def allowed_roles(allowed_roles_list=[]):
    """
    Decorator to restrict view access based on user roles.
    Expects a list of strings, e.g., ['admin', 'shopkeeper']
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # 1. Ensure the user is logged in
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('login')
            
            # 2. Check if the user's role is in the permitted list
            if request.user.role in allowed_roles_list:
                return view_func(request, *args, **kwargs)
            else:
                # Return an explicit HTTP 403 Forbidden error
                return HttpResponseForbidden("You are not authorized to view this page.")
        return wrapper_func
    return decorator