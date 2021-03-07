from django.contrib.auth import password_validation
from . import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.utils.translation import ugettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('User ID')}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'),
               'id': 'passwordlogin'}))


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ('birthdate', 'username', 'password', 'first_name', 'last_name', 'email', 'phone')
        widgets = {
            'password': forms.PasswordInput,
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError(
                _("You have to enter one of EMAIL, PHONE or Citizen ID into the User ID field")
            )
        if password != confirm_password:
            raise forms.ValidationError(
                _("Your passwords do not match")
            )
        if password:
            if len(password) < 6:
                raise forms.ValidationError(
                    _("Your passwords must be at least 6 characters")
                )



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'phone')


class RegularUserUpdateForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label=None, label=_('Country'))
    district = forms.ModelChoiceField(queryset=None, empty_label=None, label=_('District'))
    town = forms.ModelChoiceField(queryset=None, empty_label=None, label=_('Town/Village'))
    city = forms.ModelChoiceField(queryset=None, empty_label=None, label=_('City'))

    class Meta:
        model = models.RegularUser
        widgets = {
            'angina_or_heart_attack': forms.RadioSelect,
            'menopause': forms.RadioSelect,
            'kidney_disease': forms.RadioSelect,
            'atrial_fibrillation': forms.RadioSelect,
            'pressure_treatment': forms.RadioSelect,
            'rheumatoid_arthritis': forms.RadioSelect,
        }
        fields = [
            'language', 'gender', 'height', 'blood_group', 'country', 'city', 'city2',
            'district', 'town', 'physical_activity', 'smoking',
            'diabets', 'ethnicity', 'angina_or_heart_attack', 'menopause',
            'kidney_disease', 'atrial_fibrillation', 'pressure_treatment', 'rheumatoid_arthritis'
        ]

    def clean(self):
        cleaned_data = super(RegularUserUpdateForm, self).clean()
        country = cleaned_data.get('country')
        city = cleaned_data.get('city')
        city2 = cleaned_data.get('city2')
        district = cleaned_data.get('district')
        town = cleaned_data.get('town')

        if country == models.Country.objects.get(pk=1):
            if not city:
                raise forms.ValidationError("City is required")
            elif not district:
                raise forms.ValidationError("District is required")
            elif not town:
                raise forms.ValidationError("Town is required")
        else:
            if not city2:
                raise forms.ValidationError("City is required")

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['country'] == models.Country.objects.get(id=1):
            user.city2 = None
        else:
            user.city = None
            user.district = None
            user.town = None

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = models.City.objects.none()
        self.fields['district'].queryset = models.District.objects.none()
        self.fields['town'].queryset = models.Town.objects.none()
        t = models.Country.objects.get(pk=1)

        if 'country' in self.data:
            try:
                self.fields['city'].queryset = models.City.objects.filter(country_id=1)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.country == t:
                self.fields['city'].queryset = models.City.objects.filter(country_id=1)
            else:
                pass

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['district'].queryset = models.District.objects.filter(city_id=city_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.country == t:
                self.fields['district'].queryset = self.instance.city.district_set.order_by('name')
            else:
                pass

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['town'].queryset = models.Town.objects.filter(district_id=district_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.country == t:
                self.fields['town'].queryset = self.instance.district.town_set.order_by('name')
            else:
                pass


class RegularUserProfileForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label=None, label=_('Country'))
    district = forms.ModelChoiceField(queryset=None, empty_label=None, label=_('District'))
    town = forms.ModelChoiceField(queryset=None, empty_label=None, label=_('Town/Village'))
    city = forms.ModelChoiceField(queryset=None, empty_label=None, label=_('City'))

    class Meta:
        model = models.RegularUser
        widgets = {
            'angina_or_heart_attack': forms.RadioSelect,
            'menopause': forms.RadioSelect,
            'kidney_disease': forms.RadioSelect,
            'atrial_fibrillation': forms.RadioSelect,
            'pressure_treatment': forms.RadioSelect,
            'rheumatoid_arthritis': forms.RadioSelect,
        }
        fields = [
            'language', 'gender', 'height', 'blood_group',
            'country', 'city', 'city2', 'physical_activity', 'smoking', 'diabets',
            'ethnicity', 'angina_or_heart_attack', 'menopause', 'kidney_disease',
            'atrial_fibrillation', 'pressure_treatment', 'rheumatoid_arthritis',
            'district', 'town'
        ]

    def clean(self):
        cleaned_data = super(RegularUserProfileForm, self).clean()
        country = cleaned_data.get('country')
        city = cleaned_data.get('city')
        city2 = cleaned_data.get('city2')
        district = cleaned_data.get('district')
        town = cleaned_data.get('town')

        if country == models.Country.objects.get(id=1):
            if not city:
                raise forms.ValidationError(_("City is required"))
            elif not district:
                raise forms.ValidationError(_("District is required"))
            elif not town:
                raise forms.ValidationError(_("Town is required"))
        else:
            if not city2:
                raise forms.ValidationError(_("City is required"))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)

        if self.cleaned_data['country'] == models.Country.objects.get(id=1):
            user.city2 = None
        else:
            user.city = None
            user.district = None
            user.town = None

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = models.City.objects.none()
        self.fields['district'].queryset = models.District.objects.none()
        self.fields['town'].queryset = models.Town.objects.none()
        t = models.Country.objects.get(pk=1)

        if 'country' in self.data:
            try:
                self.fields['city'].queryset = models.City.objects.filter(country_id=1)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.country == t:
                self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
            else:
                pass

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['district'].queryset = models.District.objects.filter(city_id=city_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.country == t:
                self.fields['district'].queryset = self.instance.city.district_set.order_by('name')
            else:
                pass

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['town'].queryset = models.Town.objects.filter(district_id=district_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            if self.instance.country == t:
                self.fields['town'].queryset = self.instance.district.town_set.order_by('name')
            else:
                pass


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'confirm_password'}),
    )


class AskTheExpertForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['theme', 'text']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label=_('User ID'))
