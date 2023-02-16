from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView

from portfolio.forms import CreateProgrammeForm, EditProgrammeForm
from portfolio.models import Programme


class ProgrammeListView(LoginRequiredMixin, TemplateView):
    template_name = 'programme_list_page.html'


class ProgrammeCreateView(LoginRequiredMixin, CreateView):
    model = Programme
    form_class = CreateProgrammeForm
    template_name = 'programme_create_page.html'

    def get_success_url(self):
        return reverse('programme_list')


class ProgrammeUpdateView(LoginRequiredMixin, UpdateView):
    model = Programme
    form_class = EditProgrammeForm
    http_method_names = ['get', 'post']
    template_name = 'programme_update_page.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')

    def get_initial(self):
        return model_to_dict(self.get_object())


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programme_delete_page.html'
    http_method_names = ['get', 'post']
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programme_page.html'
    pk_url_kwarg = 'id'
