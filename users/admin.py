from django.contrib import admin

# Register your models here.
from users.models import User, Profile, Job

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Job)
