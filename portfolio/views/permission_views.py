from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.urls import reverse
from django.views.generic import ListView, UpdateView, CreateView

from portfolio.forms import UserCreationForm, CreateGroupForm
from portfolio.models import User
from vcpms import settings


class UserListView(LoginRequiredMixin, ListView):
    template_name = 'permissions/permission_list_page.html'
    http_method_names = ['get']
    context_object_name = 'users'
    paginate_by = settings.ADMINS_USERS_PER_PAGE

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class UserSignUpFormView(LoginRequiredMixin, CreateView):
    template_name = 'permissions/user_create.html'
    http_method_names = ['get', 'post']
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('permission_list')


class GroupCreateView(LoginRequiredMixin, CreateView):
    template_name = 'permissions/permission_form_page.html'
    http_method_names = ['get', 'post']
    form_class = CreateGroupForm

    def get_success_url(self):
        return reverse('permission_list')
