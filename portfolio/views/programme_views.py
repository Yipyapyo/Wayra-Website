from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string
import logging
from django.http import HttpResponse
import json
from portfolio.forms import CreateProgrammeForm, EditProgrammeForm
from portfolio.models import Programme
from vcpms import settings


def search_programme(request):
    if request.method == "GET":

        searched = request.GET['searchresult']

        if (searched == ""):
            search_result = {}
        else:
            search_result = Programme.objects.filter(name__contains=searched).values()

        search_results_table_html = render_to_string('programmes/search/search_results_table.html', {
            'search_results': list(search_result), 'searched': searched})

        return HttpResponse(search_results_table_html)

    elif request.method == "POST":
        page_number = request.POST.get('page', 1)
        searched = request.POST['searchresult']
        if (searched == ""):
            return redirect('programme_list')
        else:
            programmes = Programme.objects.filter(name__contains=searched).values()

        paginator = Paginator(programmes, 6)
        try:
            programmes_page = paginator.page(page_number)
        except EmptyPage:
            programmes_page = []

        return render(request, 'programmes/programme_list_page.html',
                      {"programmes": programmes_page, "searched": searched})

    else:
        return HttpResponse("Request method is not a GET")


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
        return reverse('programme_list')


class ProgrammeUpdateView(LoginRequiredMixin, UpdateView):
    model = Programme
    form_class = EditProgrammeForm
    http_method_names = ['get', 'post']
    template_name = 'programmes/programme_update_page.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')

    def get_initial(self):
        return model_to_dict(self.get_object())


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programmes/programme_delete_page.html'
    http_method_names = ['get', 'post']
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programmes/programme_page.html'
    pk_url_kwarg = 'id'
