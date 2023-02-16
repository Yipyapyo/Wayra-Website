from django.contrib.auth.mixins import LoginRequiredMixin
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


class ProgrammeUpdateView(LoginRequiredMixin, UpdateView):
    model = Programme
    form_class = EditProgrammeForm
    http_method_names = ['get','post']
    template_name = 'programme_update_page.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')

    def get_initial(self):
        instance = self.get_object()
        initial = super().get_initial()
        initial['partners'] = [partner.id for partner in instance.partners.all()]
        initial['participants'] = [participant.id for participant in instance.participants.all()]
        initial['coaches_mentors'] = [participant.id for participant in instance.coaches_mentors.all()]
        return initial


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programme_delete_page.html'
    pk_url_kwarg = 'id'


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programme_page.html'
    pk_url_kwarg = 'id'
