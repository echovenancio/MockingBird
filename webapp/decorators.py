from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def login_verified(view):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_verified:
            return redirect('app:signup-confirmation')
        return view(request, *args, **kwargs)
    return _wrapped_view
