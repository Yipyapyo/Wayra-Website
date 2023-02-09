from django.shortcuts import redirect, render
from django.views import View


from portfolio.forms import LogInForm
from django.contrib import messages
from django.contrib.auth import login, logout

from portfolio.views.mixins import LoginProhibitedMixin
from vcpms import settings


# Create your views here.
class LogInCBV(View, LoginProhibitedMixin):
    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request, *args, **kwargs):
        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request, *args, **kwargs):
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        # creates a log in form in the variable form with the user's input
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""
        form = LogInForm()
        return render(self.request, 'login.html', {'form': form, 'next': self.next})


def log_out(request):
    logout(request)
    return redirect('login')
