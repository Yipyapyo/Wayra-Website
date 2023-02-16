from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView

from portfolio.forms import ProgrammeForm
from portfolio.models import Programme


class ProgrammeListView(LoginRequiredMixin, TemplateView):
    template_name = 'programme_list_page.html'


class ProgrammeCreateView(LoginRequiredMixin, CreateView):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'programme_create_page.html'


class ProgrammeUpdateView(LoginRequiredMixin, UpdateView):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'programme_update_page.html'
    pk_url_kwarg = 'id'


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programme_delete_page.html'
    pk_url_kwarg = 'id'


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programme_page.html'
    pk_url_kwarg = 'id'
