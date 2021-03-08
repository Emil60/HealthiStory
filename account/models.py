from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from . import choices as c
from django.utils import translation
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class Country(models.Model):
    name_tr = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True)
    name_az = models.CharField(max_length=255, null=True)
    name_ru = models.CharField(max_length=255, null=True)

    def __str__(self):
        lang = translation.get_language()
        if lang == 'az':
            return self.name_az
        elif lang == 'ru':
            return self.name_ru
        elif lang == 'tr':
            return self.name_tr
        else:
            return self.name_en


class City(models.Model):
    code = models.IntegerField(verbose_name=_('Code'), null=True)
    name = models.CharField(verbose_name=_('City'), max_length=255)
    phone_code = models.IntegerField(verbose_name=_('Phone code'))
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(verbose_name=_('District'), max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Town(models.Model):
    hood = models.CharField(verbose_name=_('Neighborhood'), max_length=255)
    name = models.CharField(verbose_name=_('Town/Village'), max_length=255)
    postal_code = models.CharField(verbose_name=_('Postal code'), max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser):
    is_regular_user = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    username = models.CharField(_('User ID'), max_length=255, unique=True, null=True)
    first_name = models.CharField(_('Name'), max_length=30, blank=False, null=True)
    last_name = models.CharField(_('Surname'), max_length=30, blank=False, null=True)
    birthdate = models.DateField(_('Birthdate'), blank=False, null=True)
    email = models.EmailField(_('Email address'), unique=False, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"User ID:{self.username}"


class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="regular_user_profile")
    card_number = models.CharField(_('Card number'), max_length=20, blank=True, null=True, unique=True)
    language = models.CharField(choices=c.LANGUAGE_CHOICES, default=c.ENGLISH_LANG, max_length=50, null=True, verbose_name=_("Language"))
    gender = models.CharField(choices=c.GENDER_CHOICES, default=c.FEMALE_GENDER, max_length=50, null=True, verbose_name=_("Gender"))
    height = models.IntegerField(null=True, verbose_name=_("Height(cm)"))
    blood_group = models.CharField(choices=c.BLOOD_GROUP_CHOICES, default=c.A_PLUS, max_length=50, blank=True, null=True, verbose_name=_("Blood Group"))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Country'))
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    city2 = models.CharField(_('City*'), max_length=50, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('District'))
    town = models.ForeignKey(Town, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Town/Village'))
    physical_activity = models.CharField(_('Physical Activity'), choices=c.PHYSICAL_ACTIVITY_CHOICES, default=c.ACTIVITY_LOW, max_length=50, null=True)
    smoking = models.CharField(_('Smoking'), choices=c.SMOKING_CHOICES, default=c.SMOKER_NON, max_length=50, null=True, blank=True)
    diabets = models.CharField(_('Diabets'), choices=c.DIABETS_CHOICES, default=c.DIABET_TYPE_NONE, max_length=50, null=True, blank=True)
    ethnicity = models.CharField(_('Ethnicity'), choices=c.ETHNICITY_CHOICES, default=c.ETHNICITY_WHITE, max_length=50, null=True)
    angina_or_heart_attack = models.BooleanField(choices=c.BOOL_CHOICES, null=True, default=False, verbose_name=_("ANGINA OR HEART ATTACK IN A 1ST DEGREE RELATIVE &lt;60?"))
    menopause = models.BooleanField(_('Menopause'), choices=c.BOOL_CHOICES, null=True, default=False)
    kidney_disease = models.BooleanField(_('Kidney Disease'), choices=c.BOOL_CHOICES, null=True, default=False)
    atrial_fibrillation = models.BooleanField(_('Arterial Fibrillation'), choices=c.BOOL_CHOICES, null=True, default=False)
    pressure_treatment = models.BooleanField(choices=c.BOOL_CHOICES, null=True, default=False, verbose_name=_("DO YOU GETTING PRESSURE TREATMENT?"))
    rheumatoid_arthritis = models.BooleanField(_('Rheumatoid Arthritis'), choices=c.BOOL_CHOICES, null=True, default=False)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.user.email], **kwargs)

    def __str__(self):
        return f"Doctor ID: {self.user.username}"


class DoctorCategory(models.Model):
    cat_code = models.CharField(max_length=100, blank=False, null=True)
    cat_name = models.CharField(max_length=150, blank=False, null=True)
    language = models.CharField(choices=c.LANGUAGE_CHOICES, blank=False, max_length=100, null=True)

    def __str__(self):
        return self.cat_name


class DoctorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="doctor_profile")
    category = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE, null=True)
    organisation = models.CharField(max_length=250, null=True)
    certificates = models.CharField(max_length=250, null=True)
    image = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"Doctor ID: {self.user.username}"


class OperatorUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator_user')
    organisation = models.CharField(max_length=250)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_doctor:
        DoctorUser.objects.get_or_create(user=instance)
    else:
        RegularUser.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_doctor:
        instance.doctor_profile.save()
    else:
        RegularUser.objects.get_or_create(user=instance)


class Question(models.Model):
    theme = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(verbose_name=_("Message"), blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    asked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(verbose_name=_("Answer"), blank=False, null=False)
    answer_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.theme

