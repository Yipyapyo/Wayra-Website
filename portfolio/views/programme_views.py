from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView
from django.core.paginator import Paginator, EmptyPage

from portfolio.forms import CreateProgrammeForm, EditProgrammeForm
from portfolio.models import Programme
from vcpms import settings


class ProgrammeListView(LoginRequiredMixin, ListView):
    template_name = 'programmes/programme_list_page.html'
    context_object_name = 'programmes'
    paginate_by = settings.ITEM_ON_PAGE

    def get_queryset(self):
        return Programme.objects.all()


class ProgrammeCreateView(LoginRequiredMixin, CreateView):
    model = Programme
    form_class = CreateProgrammeForm
    template_name = 'programmes/programme_create_page.html'

    def get_success_url(self):
        return reverse('programmes/programme_list_page.html')


class ProgrammeUpdateView(LoginRequiredMixin, UpdateView):
    model = Programme
    form_class = EditProgrammeForm
    http_method_names = ['get', 'post']
    template_name = 'programmes/programme_update_page.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programmes/programme_list')

    def get_initial(self):
        return model_to_dict(self.get_object())


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programmes/programme_delete_page.html'
    http_method_names = ['get', 'post']
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programmes/programme_list')


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programmes/programme_page.html'
    pk_url_kwarg = 'id'
