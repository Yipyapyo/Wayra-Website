from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView
from django.core.paginator import Paginator, EmptyPage

from portfolio.forms import CreateProgrammeForm, EditProgrammeForm
from portfolio.models import Programme


class ProgrammeListView(LoginRequiredMixin, TemplateView):
    template_name = 'programmes/programme_list_page.html'

    def dashboard(request):
        '''The main dashboard page for the programme list.'''

        # Data for the each programme will be listed here.
        page_number = request.GET.get('page', 1)

        programmes = Programme.objects.all()

        paginator = Paginator(programmes, 6)

        try:
            programmes_page = paginator.page(page_number)
        except EmptyPage:
            programmes_page = []

        context = {
            "programmes": programmes_page,
        }

        return render(request, 'programmes/programme_list_page.html', context)

class ProgrammeCreateView(LoginRequiredMixin, CreateView):
    model = Programme
    form_class = CreateProgrammeForm
    template_name = 'programmes/programme_create_page.html'

    def create_programme(request):
        '''This page presents a form to create a programme'''
        if request.method == "POST":
            form = ProgrammeCreateForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('programme_list')
        else:
            form = ProgrammeCreateForm()

        return render(request, 'programmes/programme_create_page.html', {'form':form})

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

    def programme_detail(request, programme_id):
        '''This page displays information about a single programme'''
        programme = Programme.objects.get(id=programme_id)

        return render(request, 'programmes/programme_page.html', {'programme':programme})