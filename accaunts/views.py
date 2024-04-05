from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Profile
from django.views.generic.base import View
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required






# Create your views here.

def user_login(request):
    global context
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(request,
                                username=data['username'],
                                password=data['password']
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqiyatli kirildi")
                else:
                    return HttpResponse("Profil faol emas")
            else:
                return HttpResponse("Login yoki parol xato")

    else:
        form = LoginForm()
        context = {
            'form':form
        }
    return render(request, 'registration/login.html', context)
@login_required
def dashboard_view(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    context = {
        "user": user,
        'profile': profile_info
    }

    return render(request, 'pages/user_profile.html', context)
#


# def dashboard_view(request):
#     user = request.user
#     if user.is_authenticated:
#         profile_info = Profile.objects.filter(user=user)
#         context = {
#             "user": user,
#             'profile': profile_info
#         }
#         return render(request, 'pages/user_profile.html', context)
#     else:
#         # Foydalanuvchi avtentifikatsiyadan o'tmagan bo'lsa, shu sahifaga o'tkazish orqali foydalanuvchini autentifikatsiya qilishga yo'naltirish
#         return redirect('login')  # login URL nomini qo'shing


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user": new_user
            }
            return render(request, 'accaunt/register_done.html', context)

    else:
        user_form = UserRegistrationForm()
        context = {
            "user_form": user_form
        }
        return render(request, 'accaunt/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accaunt/register.html'

class SignUpView2(View):

    def get(self, request):
        user_form = UserRegistrationForm()
        print(user_form)
        context = {
            "user_form": user_form
        }
        return render(request, 'accaunt/register_done.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            context = {
                'new_user': new_user
            }
            return render(request, 'accaunt/register.html', context)

@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accaunt/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


class EditUserView(View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'accaunt/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')









