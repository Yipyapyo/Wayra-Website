from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.forms.company_form import CompanyCreateForm
from portfolio.models import Company
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
import json 
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse


"""
View and Update user settings
"""
@login_required
def account_settings(request):
    current_user = request.user
    context = {
        "user":current_user,
    }
    return render(request, 'settings/account_settings.html', context)