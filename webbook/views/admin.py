from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.views import View
# from django.contrib.auth.decorators import login_required

#TODO: Lock with admin only
class HomeView(View):
    """
        HomeView for Admin
    """
    template_name = "admin/homepage.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())
    
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())
