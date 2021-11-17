from django.contrib import admin

# Register your models here.
from search_job.models import SearchJobPost, CommentSearchJob

admin.site.register(SearchJobPost)
admin.site.register(CommentSearchJob)