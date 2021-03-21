from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('info')
        else:
            return view_func(request, *args, **kwargs)
    return check_user

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def check_user(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("<h1>You Are not Authorized</h1>")
        return check_user
    return decorator


def admin_only(view_func):
    def check_user(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        
        if group=="admin":
            return view_func(request, *args, **kwargs)
            
        if group=="student":
            return redirect('info')

    return check_user


