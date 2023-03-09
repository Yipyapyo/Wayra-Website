from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView

from portfolio.forms import InvestmentForm
from portfolio.models.investment_model import ContractRight
from vcpms import settings


class ContractRightsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'investment/contract_rights/contract_right_list.html'
    paginate_by = settings.ITEM_ON_PAGE
    context_object_name = 'contract_rights'
    http_method_names = ['get']

    def dispatch(self, request, investment_id, *args, **kwargs):
        self.investment_id = investment_id
        return super().dispatch(request, investment_id, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_id'] = self.investment_id
        return context

    def get_queryset(self):
        return ContractRight.objects.filter(investment_id=self.investment_id).order_by('id')


class ContractRightCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'investment/contract_rights/contract_right_create.html'
    model = ContractRight
    pk_url_kwarg = 'id'
    form_class = InvestmentForm # Temporary placeholder
    # form_class = ContractRightForm
    http_method_names = ['get', 'post']

    def dispatch(self, request, investment_id, *args, **kwargs):
        self.investment_id = investment_id
        return super().dispatch(request, investment_id, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('contract_right_list', kwargs={'investment_id': self.investment_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_id'] = self.investment_id
        return context


class ContractRightDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'investment/contract_rights/contract_right_delete.html'
    http_method_names = ['get', 'post']
    model = ContractRight
    pk_url_kwarg = 'id'

    def dispatch(self, request, id, *args, **kwargs):
        try:
            right = ContractRight.objects.get(id=id)
            self.investment = right.investment
        except ObjectDoesNotExist:
            return redirect('dashboard')
        return super().dispatch(request, id, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('contract_right_list', kwargs={'investment_id': self.investment.id})
