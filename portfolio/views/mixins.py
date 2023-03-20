from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.shortcuts import redirect


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class FindObjectMixin:
    redirect_when_no_object_found_url = None
    # redirect_when_no_object_found_url_kwargs = {}
    model = None

    def get_redirect_when_no_object_found_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_no_object_found_url is None:
            raise ImproperlyConfigured(
                "FindObjectMixin requires either a value for "
                "'redirect_when_no_object_found_url', or an implementation for "
                "'get_redirect_when_no_object_found_url()'."
            )
        else:
            return self.redirect_when_no_object_found_url

    def get_model(self):
        if self.model is None:
            raise ImproperlyConfigured(
                "FindObjectMixin requires either a value for "
                "'model', or an implementation for "
                "'get_model()'."
            )
        return self.model

    def dispatch(self, request, id, *args, **kwargs):
        try:
            model = self.get_model()
            model.objects.get(id=id)
        except ObjectDoesNotExist:
            url = self.get_redirect_when_no_object_found_url()
            # return redirect(url,kwargs=self.redirect_when_no_object_found_url_kwargs)
            return redirect(url)
        return super().dispatch(request, id, *args, **kwargs)
