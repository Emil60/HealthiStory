from django.contrib import admin
from .models import User, Country, City, District, Town, Answer, Question, RegularUser, DoctorUser


admin.site.register(User)
admin.site.register(RegularUser)
admin.site.register(DoctorUser)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Town)
admin.site.register(Answer)
admin.site.register(Question)