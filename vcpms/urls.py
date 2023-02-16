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
from django.urls import path
from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.LogInCBV.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('search_result', views.searchcomp, name='search_result'),
    path('portfolio_company/', views.portfolio_company, name='portfolio_company'),

    # Individual CRUD
    path("individual_page/individual_create/", views.individual_create, name="individual_create"),
    path("individual_page/", views.individual_page, name="individual_page"),
    path("individual_page/<int:id>/update/", views.individual_update, name='individual_update'),
    path("individual_page/<int:id>/delete/", views.individual_delete, name='individual_delete'),

    # Programme CRUD
    path("programme_page/", views.ProgrammeListView.as_view(), name="programme_list"),
    path("programme_page/create/", views.ProgrammeCreateView.as_view(), name="programme_create"),
    path("programme_page/<int:id>/update/", views.ProgrammeUpdateView.as_view(), name="programme_update"),
    path("programme_page/<int:id>/delete/", views.ProgrammeDeleteView.as_view(), name="programme_delete"),
    path("programme_page/<int:id>/detail/", views.ProgrammeDetailView.as_view(), name="programme_detail"),

]
