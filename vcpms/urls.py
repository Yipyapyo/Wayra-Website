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
from portfolio.views import founder_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.LogInCBV.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('search_result', views.searchcomp, name='search_result'),

    path('portfolio_company/', views.portfolio_company, name='portfolio_company'),
    path('portfolio_company/<int:company_id>', views.portfolio_company, name='portfolio_company'),
    path('portfolio_company/company_create/', views.create_company, name='create_company'),
    path('portfolio_company/company_update/<int:company_id>', views.update_company, name='update_company'),
    path('portfolio_company/company_delete/<int:company_id>', views.delete_company, name='delete_company'),
    path('portfolio_company/archive/<int:company_id>', views.archive_company, name='archive_company'),
    path('portfolio_company/unarchive/<int:company_id>', views.unarchive_company, name='unarchive_company'),
    
    # Individual CRUD
    path("individual_page/individual_create/", views.individual_create, name="individual_create"),
    path("individual_page/", views.individual_page, name="individual_page"),
    path("individual_page/<int:id>/update/", views.individual_update, name='individual_update'),
    path("individual_page/<int:id>/delete/", views.individual_delete, name='individual_delete'),
    path("individual_page/founder_create/", founder_views.founder_create, name="founder_create"),
    path("individual_page/<int:id>/deleteFounder/", founder_views.founder_delete, name="founder_delete"),
    path("individual_page/<int:id>/modifyFounder/", founder_views.founder_modify, name="founder_modify"),
    path("individual_profile_page/<int:id>/", views.individual_profile, name='individual_profile'),
    path('individual_page/archive/<int:id>', views.archive_individual, name='archive_individual'),
    path('individual_page/unarchive/<int:id>', views.unarchive_individual, name='unarchive_individual'),

    # Programme CRUD
    path("programme_page/", views.ProgrammeListView.as_view(), name="programme_list"),
    path("programme_page/create/", views.ProgrammeCreateView.as_view(), name="programme_create"),
    path("programme_page/<int:id>/update/", views.ProgrammeUpdateView.as_view(), name="programme_update"),
    path("programme_page/<int:id>/delete/", views.ProgrammeDeleteView.as_view(), name="programme_delete"),
    path("programme_page/<int:id>/detail/", views.ProgrammeDetailView.as_view(), name="programme_detail"),

    # Archive views
    path("archive_page/", views.archive, name="archive_page"),
    path('archive/search', views.archive_search, name='archive_search'),

    # Settings views
    path("account_settings/", views.account_settings, name="account_settings"),
    path("account_settings/change_password", views.change_password, name="change_password"),
    path("account_settings/contact_details", views.contact_details, name="contact_details"),
    path("account_settings/upload_profile_picture", views.uplaod_profile_picture, name="uplaod_profile_picture"),
    path("account_settings/remove_profile_picture", views.remove_profile_picture, name="remove_profile_picture"),
    path("deactivate_account", views.deactivate_account, name="deactivate_account"),


    # Permissions
    path("select2/", include("django_select2.urls")),
    path("permissions/users/", views.UserListView.as_view(), name='permission_user_list'),
    path("permissions/create_user/", views.UserSignUpFormView.as_view(), name='permission_create_user'),
    path("permissions/<int:id>/edit_user/", views.UserEditFormView.as_view(), name='permission_edit_user'),
    path("permissions/<int:id>/delete_user/", views.UserDeleteView.as_view(), name='permission_delete_user'),
    path("permissions/<int:id>/reset_password/", views.UserResetPasswordView.as_view(),
         name="permission_reset_password"),
    path("permissions/group_list/", views.GroupListView.as_view(), name='permission_group_list'),
    path("permissions/create_group/", views.GroupCreateView.as_view(), name='permission_create_group'),
    path("permissions/<int:id>/edit_group/", views.GroupEditView.as_view(), name='permission_edit_group'),
    path("permissions/<int:id>/delete_group/", views.GroupDeleteView.as_view(), name='permission_delete_group'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)