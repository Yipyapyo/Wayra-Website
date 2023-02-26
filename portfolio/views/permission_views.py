from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, FormView

from portfolio.forms import UserCreationForm, CreateGroupForm
from portfolio.models import User
from vcpms import settings


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'permissions/permission_list_page.html'
    http_method_names = ['get']
    context_object_name = 'users'
    paginate_by = settings.ADMINS_USERS_PER_PAGE

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class UserSignUpFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'permissions/user_create.html'
    http_method_names = ['get', 'post']
    form_class = UserCreationForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('permission_user_list')


class GroupCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'permissions/permission_form_page.html'
    http_method_names = ['get', 'post']
    form_class = CreateGroupForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_success_url(self):
        return reverse('permission_user_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'permissions/user_delete.html'
    http_method_names = ['get', 'post']
    model = User
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = self.get_object().id
        return context

    def get_success_url(self):
        return reverse('permission_user_list')
