from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

"""Archive views"""
@login_required
def archive(request):
    '''This ius the archive page. ONLY VIEWED BY ADMINS'''

    return render(request, 'archive/archive_page.html')

