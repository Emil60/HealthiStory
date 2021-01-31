from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, CustomPasswordChangeForm, AskTheExpertForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .models import City, District, Town, Question
from django.utils.translation import ugettext_lazy as _


def user_register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            print(form.errors)
            return render(request, 'account/register.html', {'form': form})
    else:
        return render(request, 'account/register.html', {'form': form})


def user_login(request):
    # Log user in
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('profile')
            else:
                #messages.success(request, _('Wrong password or User ID'))
                return render(request, 'account/login.html', {'form': form})
        else:
            form = UserLoginForm()
            return render(request, 'account/login.html', {'form': form})
    return redirect('home')


def user_logout(request):
    # Logout user
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('home')


def user_account(request):
    if request.user.is_authenticated:
        return render(request, 'account/account.html')
    else:
        return redirect('login')


def user_account_edit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
            else:
                print(form.errors)
                return render(request, 'account/editAccount.html', {'form': form})
        else:
            form = UserUpdateForm(instance=request.user)
            return render(request, 'account/editAccount.html', {'form': form})
    else:
        return redirect('login')


def user_password_change(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                return render(request, 'account/change_password.html', {'form': form})
        else:
            form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form': form})
    else:
        return redirect('login')


def user_ask_expert(request):
    """
        Handle question asking from a user perspective
    """
    questions = Question.objects.filter(asked_by=request.user)
    if request.method == "POST":
        form = AskTheExpertForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.asked_by = request.user
            obj.save()
            messages.success(request, _("We got your message"))
            return render(request, 'account/ask_the_expert.html', {"form": form, "questions": questions})
        else:
            messages.error(request, _("Something went wrong please try again"))
            return render(request, 'account/ask_the_expert.html', {"form": form, "questions": questions})
    else:
        form = AskTheExpertForm()
        return render(request, 'account/ask_the_expert.html', {"form": form, "questions": questions })


def user_reports(request):
    return HttpResponse('<h1>Soon available...</h1>')


def load_cities(request):
    cities = City.objects.filter(country_id=1)
    return render(request, 'account/city_dropdown_list_options.html', {'cities': cities})


def load_districts(request):
    city = request.GET.get('city')
    districts = District.objects.filter(city_id=city)
    return render(request, 'account/city_dropdown_list_options.html', {'districts': districts})


def load_towns(request):
    district = request.GET.get('district')
    towns = Town.objects.filter(district_id=district)
    return render(request, 'account/city_dropdown_list_options.html', {'towns': towns})

