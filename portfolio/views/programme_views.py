from django.contrib.auth.mixins import LoginRequiredMixin
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
    template_name = 'programme_update_page.html'
    pk_url_kwarg = 'id'

    def get_initial(self):
        initial = super().get_initial()
        initial['partners'] = [1]
        initial['participants'] = [2]
        initial['coaches_mentors'] = [1]
        return initial


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programme_delete_page.html'
    pk_url_kwarg = 'id'


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programme_page.html'
    pk_url_kwarg = 'id'
