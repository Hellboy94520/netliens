from django.shortcuts import redirect, get_object_or_404
from django.http import Http404

from ...models import Announcement


def user_has_nl(function):
    """
        Decorator used to check if an user has NL to use or not.
        If not, return to purchase page
    """
    def wrap(request, *args, **kwargs):
        if not request.user:
            return redirect('/account/')
        # TODO: To move into model
        # if (request.user.nl0 - Announcement.objects.filter(owner=request.user, nl=0).count()) > 0 or \
        # (request.user.nl1 - Announcement.objects.filter(owner=request.user, nl=1).count()) > 0 or \
        # (request.user.nl2 - Announcement.objects.filter(owner=request.user, nl=2).count()) > 0 or \
        # (request.user.nl3 - Announcement.objects.filter(owner=request.user, nl=3).count()) > 0 or \
        # (request.user.nl4 - Announcement.objects.filter(owner=request.user, nl=4).count()) > 0 or \
        # (request.user.nl5 - Announcement.objects.filter(owner=request.user, nl=5).count()) > 0 or \
        # (request.user.nl6 - Announcement.objects.filter(owner=request.user, nl=6).count()) > 0 or \
        # (request.user.nl7 - Announcement.objects.filter(owner=request.user, nl=7).count()) > 0:
        #     return function(request, *args, **kwargs)
        # else:
        return redirect('/account/announcement/purchase/')
    wrap.__doc__ = function.__doc__
    return wrap

def logout_required(function):
    """
        Decorator used to allow only non-authentificate user
        If not, return to account
    """
    def wrap(request, *args, **kwargs):
        if request.user:
            return function(request, *args, **kwargs)
        else:
            return redirect('/account/')
    wrap.__doc__ = function.__doc__
    return wrap

def owner_required(function):
    """
        Decorator used to check if user is owner of announcement.
        If not, return 404 page
    """
    def wrap(request, *args, **kwargs):
        l_annoucement = get_object_or_404(Announcement, url=kwargs['announcement_url'])
        if l_annoucement.owner == request.user:
            return function(request, *args, **kwargs)
        else:
            raise Http404()
    wrap.__doc__ = function.__doc__
    return wrap
