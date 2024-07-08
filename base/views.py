from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

def index(request):
    return HttpResponseRedirect(reverse('base:home'))

class HomePageView(generic.TemplateView):
    '''
    Home page view, still to be defined the content inside
    '''
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context