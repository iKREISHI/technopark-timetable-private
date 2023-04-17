from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserRegisterForm


# Create your views here.
class Register(View):
    template_name = "users/register.html"
    context = {
        'title': 'Регистрация пользователя',
        'form': UserRegisterForm
    }

    def get(self, request):

        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, self.context)
