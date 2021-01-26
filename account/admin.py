from django.contrib import admin
from .models import User, Country, City, District, Town, Answer, Question


admin.site.register(User)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Town)
admin.site.register(Answer)
admin.site.register(Question)