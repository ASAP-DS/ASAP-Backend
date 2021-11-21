from rest_framework import serializers

from search_job.models import SearchJobPost, CommentSearchJob
from users.models import Profile, Job
from users.serializers import ProfileSerializer, JobSerializer


class SortPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchJobPost
        #workHours = model.workHours(model)
        fields = ['id', 'profile', 'title', 'jobs',  'start_date', 'end_date',
                  'start_time', 'end_time', 'created_at', 'content']

    # def get_workHours(self, object):
    #     end_time = object.end_time
    #     start_time = object.start_time
    #     hours = end_time.hour - start_time.hour
    #     minutes = end_time.minute - start_time.minute
    #     minutes_to_hours = minutes / 60.0
    #     return hours + minutes_to_hours


class SearchJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchJobPost
        fields = ['id', 'profile', 'title', 'jobs', 'start_date', 'end_date',
                  'start_time', 'end_time', 'created_at', 'content']

    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        # self.fields['jobs'] = JobSerializer(read_only=True)
        return super(SearchJobPostSerializer, self).to_representation(instance)


class CommentSearchJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSearchJob
        fields = "__all__"


class CommentPostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(style={'input_type': 'post_id'})
    profile_id = serializers.IntegerField(style={'input_type': 'profile_id'})
    content = serializers.CharField(max_length=None, style={'input_type': 'profile_id'})
    is_anon = serializers.BooleanField(style={'input_type': 'is_anon'})
