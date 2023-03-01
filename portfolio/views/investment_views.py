from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from portfolio.forms import InvestmentForm
from portfolio.models import Investment


class InvestmentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'investment/investment_create.html'
    model = Investment
    form_class = InvestmentForm
    http_method_names = ['get','post']


    def dispatch(self, request, company_id, *args, **kwargs):
        self.company_id = company_id
        return super().dispatch(request, company_id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        return context

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})


class InvestmentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'investment/investment_update.html'
    model = Investment
    form_class = InvestmentForm
    pk_url_kwarg = 'id'
    http_method_names = ['get','post']


    def dispatch(self, request, company_id, id, *args, **kwargs):
        self.company_id = company_id
        return super().dispatch(request, company_id, id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        return context

    def get_initial(self):
        return model_to_dict(self.get_object())

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})


class InvestmentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'investment/investment_delete.html'
    model = Investment
    form_class = InvestmentForm
    pk_url_kwarg = 'id'
    http_method_names = ['get','post']

    def dispatch(self, request, company_id, id, *args, **kwargs):
        self.company_id = company_id
        return super().dispatch(request, company_id, id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        return context

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})
