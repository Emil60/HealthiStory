# Generated by Django 3.1.3 on 2020-11-17 17:29

import account.managers
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(null=True, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='City')),
                ('phone_code', models.IntegerField(verbose_name='Phone code')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='District')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.city')),
            ],
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hood', models.CharField(max_length=255, verbose_name='Neighborhood')),
                ('name', models.CharField(max_length=255, verbose_name='Town/Village')),
                ('postal_code', models.CharField(max_length=255, verbose_name='Postal code')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.district')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.country'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=30, null=True, verbose_name='Name')),
                ('surname', models.CharField(max_length=30, null=True, verbose_name='Surname')),
                ('birthdate', models.DateField(null=True, verbose_name='Birthdate')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email address')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone')),
                ('passport', models.CharField(max_length=255, null=True, unique=True, verbose_name='User ID(Citizen ID or E-mail or Mobile number)')),
                ('card_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Card number')),
                ('language', models.CharField(choices=[('EN', 'English'), ('RU', 'Russian'), ('TR', 'Turkish'), ('AZ', 'Azerbaijan')], default='EN', max_length=50, null=True, verbose_name='Language')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='F', max_length=50, null=True, verbose_name='Gender')),
                ('height', models.IntegerField(null=True, verbose_name='Height(cm)')),
                ('blood_group', models.CharField(blank=True, choices=[('A RH+', 'A RH+'), ('A RH-', 'A RH-'), ('AB RH+', 'AB RH+'), ('AB RH-', 'AB RH-'), ('B RH+', 'B RH+'), ('B RH-', 'B RH-'), ('0 RH+', '0 RH+'), ('0 RH-', '0 RH-')], default='A RH+', max_length=50, null=True, verbose_name='Blood Group')),
                ('city2', models.CharField(blank=True, max_length=50, null=True, verbose_name='City*')),
                ('physical_activity', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=50, null=True, verbose_name='Physical Activity')),
                ('smoking', models.CharField(blank=True, choices=[('Non-smoker', 'Non-smoker'), ('Ex-smoker', 'Ex-smoker'), ('Light-smoker', 'Light smoker (less than 10)'), ('Moderate-smoker', 'Moderate smoker (10 to 19)'), ('Heavy-smoker', 'Heavy smoker (20 or over)')], default='Non-smoker', max_length=50, null=True, verbose_name='Smoking')),
                ('diabets', models.CharField(blank=True, choices=[('None', 'None'), ('Type 1', 'Type 1'), ('Type 2', 'Type 2')], default='None', max_length=50, null=True, verbose_name='Diabets')),
                ('ethnicity', models.CharField(choices=[('White', 'White or not stated'), ('Indian', 'Indian'), ('Pakistani', 'Pakistani'), ('Bangladeshi', 'Bangladeshi'), ('Asian', 'Other Asian'), ('Caribbean', 'Black Caribbean'), ('African', 'Black African'), ('Chinese', 'Chinese'), ('Others', 'Others')], default='White', max_length=50, null=True, verbose_name='Ethnicity')),
                ('angina_or_heart_attack', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='ANGINA OR HEART ATTACK IN A 1ST DEGREE RELATIVE &lt;60?')),
                ('menopause', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='Menopause')),
                ('kidney_disease', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='Kidney Disease')),
                ('atrial_fibrillation', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='Arterial Fibrillation')),
                ('pressure_treatment', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='DO YOU GETTING PRESSURE TREATMENT?')),
                ('rheumatoid_arthritis', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, null=True, verbose_name='Rheumatoid Arthritis')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.country')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.district')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('town', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.town')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
    ]
