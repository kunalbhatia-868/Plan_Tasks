from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView,LogoutView, redirect_to_login
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
# Create your views here.


class Login(LoginView):
    template_name='auth/login.html'
    fields='__all__'
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class Logout(LogoutView):
    next_page='login'   


class Register(FormView):
    template_name='auth/register.html'
    form_class=UserCreationForm
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        user=form.save()
        if user:
            login(self.request,user)
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)

