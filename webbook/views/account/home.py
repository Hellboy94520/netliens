from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from ...models import User, Announcement, Category, Localisation
from ...forms import PublicUserForm, SignUpForm, send_mail as SendEmail

from ..common import decorators as my_decorators


# -----------------------------
# View
# -----------------------------
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    """
        View to manage account
    """



# -----------------------------
@method_decorator(login_required, name='dispatch')
class UpdateView(TemplateView):
    """
        View to update account
    """
    form_class = PublicUserForm

    def get(self, request, *args, **kwargs):
        form = PublicUserForm(instance=request.user)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = PublicUserForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            user = form.save()
            return redirect('/')
        return render(request, self.template_name, locals())


# -----------------------------
@method_decorator(login_required, name='dispatch')
class AnnouncementView(TemplateView):
    """
        View to manage announcement
    """
    def get_nl_tab(self, request):
        nl_status = [ [ 0, request.user.nl0-Announcement.objects.filter(owner=request.user, nl=0).count(), request.user.nl0 ],
            [ 1, request.user.nl1-Announcement.objects.filter(owner=request.user, nl=1).count(), request.user.nl1 ],
            [ 2, request.user.nl2-Announcement.objects.filter(owner=request.user, nl=2).count(), request.user.nl2 ],
            [ 3, request.user.nl3-Announcement.objects.filter(owner=request.user, nl=3).count(), request.user.nl3 ],
            [ 4, request.user.nl4-Announcement.objects.filter(owner=request.user, nl=4).count(), request.user.nl4 ],
            [ 5, request.user.nl5-Announcement.objects.filter(owner=request.user, nl=5).count(), request.user.nl5 ],
            [ 6, request.user.nl6-Announcement.objects.filter(owner=request.user, nl=6).count(), request.user.nl6 ],
            [ 7, request.user.nl7-Announcement.objects.filter(owner=request.user, nl=7).count(), request.user.nl7 ],
        ]
        return nl_status

    def get(self, request, *args, **kwargs):
        nl_status = self.get_nl_tab(request)
        return render(request, self.template_name, locals())

# -----------------------------
from ...forms import AnnouncementUserSettingForm
@method_decorator(login_required, name='dispatch')
@method_decorator(my_decorators.user_has_nl, name='dispatch')
class AnnouncementCreationView(FormView):
    """
        View to create an announcement
    """
    form_class = AnnouncementUserSettingForm

    def get_form_kwargs(self):
        kwargs = super(AnnouncementCreationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        announcement = form.save(user=self.request.user)
        self.success_url = self.success_url.replace("<str:announcement_url>", announcement.url)
        return super(AnnouncementCreationView, self).form_valid(form)


# -----------------------------
from ...forms import AnnouncementUserDataForm
@method_decorator(login_required, name='dispatch')
@method_decorator(my_decorators.owner_required, name='dispatch')
class AnnouncementDataView(FormView):
    """
        View to create an announcement with it data
    """
    form_class = AnnouncementUserDataForm

    def get(self, request, *args, **kwargs):
        print("get !!")
        return super(AnnouncementDataView, self).get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        l_announcement = get_object_or_404(Announcement, url=kwargs['announcement_url'])
        form = self.get_form()
        if form.is_valid(l_announcement):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        l_announcement = form.save()
        return super(AnnouncementDataView, self).form_valid(form)

# -----------------------------
# from ..forms import AnnouncementUserDataForm
# @method_decorator(login_required, name='dispatch')
# class AnnouncementUpdateView(FormView):
#     """
#         View to create an announcement
#     """
#     form_class = AnnouncementLanguageForm

    # def _get_env(self, *args, **kwargs):
    #     return get_object_or_404(Announcement, url=kwargs['announcement_url'])

    # def get(self, request, *args, **kwargs):
    #     super(AnnouncementUpdateView, self).get(request, args, kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super(AnnouncementCreationView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

# -----------------------------
@method_decorator(login_required, name='dispatch')
class AnnouncementPurchaseView(TemplateView):
    """
        View to buy NL
    """
    pass

