from django.db import models


# Create your models here.

#post_id (pk), prof_id(fk), title(char30), hourly_pay(int),
# start_date, end_date, start_time, end_time, created_at, updated_at,
# content(text)
class GetStaffPost(models.Model):
    prof_id = models.ForeignKey()
    title = models.CharField(max_length=30)
    content = models.TextField(default='content')
