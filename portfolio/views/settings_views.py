from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.forms import ChangePasswordForm
from portfolio.models import User
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
import json 
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout


"""
View and Update user settings
"""
@login_required
def account_settings(request):
    current_user = request.user
    change_password_form = ChangePasswordForm(user=current_user)
    context = {
        "user":current_user,
        "change_password_form":change_password_form,
    }
    return render(request, 'settings/account_settings.html', context)

@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            #Change the user's password
            form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, form.user)

            messages.add_message(request, messages.SUCCESS, "Password Updated Successfully!")
            return redirect('account_settings')
        else:
            messages.add_message(request, messages.ERROR, "Unable to change your password!")
            current_user = request.user
            context = {
                "user":current_user,
                "change_password_form":form,
            }
            return render(request, 'settings/account_settings.html', context)
    else:
        return HttpResponse("404, Unable to make this call")

@login_required
def deactivate_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.add_message(request, messages.SUCCESS, "Account successfully deactivated!")
    return redirect('login')