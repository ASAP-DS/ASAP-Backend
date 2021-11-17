from django.contrib import admin

# Register your models here.
from get_staff.models import GetStaffPost, CommentGetStaff

admin.site.register(GetStaffPost)
admin.site.register(CommentGetStaff)