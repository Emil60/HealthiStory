from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, CustomPasswordChangeForm, AskTheExpertForm, CustomPasswordResetForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .models import City, District, Town, Question, User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def password_reset_request(request):
    if request.method == "POST":
        domain = request.headers['Host']
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(passport=data))
            # You can use more than one way like this for resetting the password.
            # ...filter(Q(email=data) | Q(username=data))
            # but with this you may need to change the password_reset form as well.
            if associated_users.exists():
                for user in associated_users:
                    subject = _("Password Reset Requested")
                    email_template_name = "account/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Interface',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse(_('Invalid header found.'))
                    return redirect("password_reset_done")
    password_reset_form = CustomPasswordResetForm()
    return render(request=request, template_name="account/password_reset_form.html",
                  context={"form": password_reset_form})


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

