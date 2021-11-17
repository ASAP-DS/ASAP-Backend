from django.db import models

# Create your models here.

# post_id (pk), prof_id(fk), title(char30), hourly_pay(int),
# start_date, end_date, start_time, end_time, created_at, updated_at,
# content(text)
from django.utils import timezone
from django.utils.datetime_safe import datetime, date
from django.utils.timezone import now

from users.models import Profile, Job


# 제목, 경력(jobs), 근무 가능 날짜, 근무 가능 시간
class SearchJobPost(models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)  # default=1 -> pk=1
    title = models.CharField(max_length=30)
    jobs = models.ManyToManyField(Job, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    # updated_at.. ( 게시글 수정 기능 우선 없음) 있어야하긴하는데.. 글 수정안되는 커뮤니티가 있나..?
    content = models.TextField(default='content')

    class Meta:
        ordering = ['-created_at']  # 기본 정렬 - 최신순

    def __str__(self):
        return f'{self.pk}: {self.title} - {self.profile.nickname}'


class CommentSearchJob(models.Model):
    post = models.ForeignKey(SearchJobPost, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    is_anon = models.BooleanField()  # 익명이면 True

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.pk} : {self.profile} - Anonymous {self.is_anon}'
