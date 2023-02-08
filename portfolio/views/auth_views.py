from django.shortcuts import redirect, render
from portfolio.forms import LogInForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def log_in(request):
    #if user isn't student, they are admin user so are sent to the admin dashboard
    if request.method == 'POST':
        form = LogInForm(request.POST)
        #creates a log in form in the variable form with the user's input
        if form.is_valid():
            username = form.cleaned_data.get('email') #gets email address from the form
            password = form.cleaned_data.get('password') #gets password from the form
            user = authenticate(username = username, password = password)
            if user is not None: #if the user exists
                login(request, user)
                redirect_url = request.POST.get('next') or 'dashboard' #directs to admin dashboard
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "Invalid credentials")
    form = LogInForm()
    next = request.GET.get('next') or ''
    return render(request, 'login.html', {'form':form, 'next':next})