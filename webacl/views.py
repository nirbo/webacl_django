from django.shortcuts import render
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'webacl/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LoginSuccessView(TemplateView):
    template_name = 'webacl/login_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LoginFailureView(TemplateView):
    template_name = 'webacl/login_failure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
