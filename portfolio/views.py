from django.shortcuts import render, redirect

# Create your views here.
def dashboard(request):
    '''The main dashboard page of the website.'''
    counter = {1,2,3,4,5,6,7,8,9}
    return render(request, 'main_dashboard.html', {'counter':counter})