
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def dashboard(request):
    # Only staff users may view
    if not request.user.is_staff:
        return HttpResponseForbidden('Forbidden: admin only')
    return render(request, 'custom_admin/dashboard.html', {'user': request.user})
