"""vcpms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.LogInCBV.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('search_result', views.searchcomp, name='search_result'),
    path('portfolio_company/<int:company_id>', views.portfolio_company, name='portfolio_company'),
    path('portfolio_company/company_create/', views.create_company, name='create_company'),
    path('portfolio_company/company_update/<int:company_id>', views.update_company, name='update_company'),
    path('portfolio_company/company_delete/<int:company_id>', views.delete_company, name='delete_company'),
    path("individual_page/individual_create/", views.individual_create, name="individual_create"),
    path("individual_page/", views.individual_page, name="individual_page"),
    path("individual_page/<int:id>/update/", views.individual_update, name='individual_update'),
    path("individual_page/<int:id>/delete/", views.individual_delete, name='individual_delete'),

    # Permissions
    path("select2/", include("django_select2.urls")),
    path("permissions/users/", views.UserListView.as_view(), name='permission_user_list'),
    path("permissions/create_user/", views.UserSignUpFormView.as_view(), name='permission_create_user'),
    path("permissions/create_group/", views.GroupCreateView.as_view(), name='permission_create_group'),
    path("permissions/<int:id>/delete_user/", views.UserDeleteView.as_view(), name='permission_delete_user'),
    path("permissions/group_list/", views.GroupListView.as_view(), name='permission_group_list'),
    path("permissions/<int:id>/edit_group/", views.GroupEditView.as_view(), name='permission_edit_group'),
    path("permissions/<int:id>/delete_group/", views.GroupDeleteView.as_view(), name='permission_delete_group'),
    path("permissions/<int:id>/edit_user/", views.UserEditFormView.as_view(), name='permission_edit_user')

]
