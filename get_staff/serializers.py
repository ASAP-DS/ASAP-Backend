from rest_framework import serializers

from get_staff.models import GetStaffPost
from users.models import Profile, Job
from users.serializers import ProfileSerializer, JobSerializer


class GetStaffPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetStaffPost
        fields = ['id', 'profile', 'title', 'jobs', 'hourly_pay', 'start_date', 'end_date',
                  'start_time', 'end_time', 'created_at', 'content']


    def to_representation(self, instance):
        self.fields['profile'] = ProfileSerializer(read_only=True)
        #self.fields['jobs'] = JobSerializer(read_only=True)
        return super(GetStaffPostSerializer, self).to_representation(instance)

#
# class GetStaffPostSerializer(serializers.ModelSerializer):
#     # 다대다 , 그 다시 ㅇㅇ
#     # profile = serializers.PrimaryKeyRelatedField(read_only=True)
#     # jobs = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
#
#     profile = ProfileSerializer()
#     jobs = JobSerializer(required=False, many=True, allow_null=True)
#
#     # profile = ProfileSerializer(source='pk', read_only=True)
#     # jobs = JobSerializer(source='pk', required=False, many=True, allow_null=True, read_only=True)
#     # profile = serializers.ReadOnlyField(source='profile.pk')
#     # jobs = serializers.ReadOnlyField(source='jobs.pk')
#     # profile = serializers.SlugRelatedField(slug_field=str(Profile.pk), read_only=True)
#     # jobs = serializers.SlugRelatedField(slug_field=str(Job.pk), read_only=True)
#
#     class Meta:
#         model = GetStaffPost
#         fields = ['id', 'profile', 'title', 'jobs', 'hourly_pay', 'start_date', 'end_date',
#                    'start_time', 'end_time', 'created_at', 'content']
#         #fields = "__all__"
#
#     # def to_representation(self, instance):
#     #     response = super().to_representation(instance)
#     #     response['profile'] = ProfileSerializer(instance.profile).data
#     #     return response
#
#     def create(self, validated_data):  # profile, jobs4
#         profile_data = validated_data.pop('profile')
#         jobs_data = validated_data.pop('jobs')  # list?
#
#         # post = GetStaffPost.objects.create(
#         #     profile=Profile.objects.get(pk=validated_data['profile']),
#         #     title=validated_data['title'],
#         #     hourly_pay=validated_data['hourly_pay'],
#         #     start_date=validated_data['start_date'],
#         #     start_titme=validated_data['start_time'],
#         #     end_date=validated_data['end_date'],
#         #     end_time=validated_data['end_time'],
#         #     content=validated_data['content'],
#         # )
#         post = GetStaffPost.create(**validated_data)
#         for job in jobs_data:
#             post.jobs.add(Job.objects.get(pk=job))
#         post.save()
#         return post
#
#         # profile_data = validated_data.pop('profile')
#         # profile_id = profile_data
#         # profile = Profile.objects.get(pk=profile_id)
#         # jobs_data = validated_data.pop('jobs') # list?
#         # post = GetStaffPost.objects.create(**validated_data,
#         #                                  profile=profile)  # Direct assignment to the forward side of a many-to-many set is prohibited. Use jobs.set() instead.
#         # for job_data in jobs_data:
#         #     post.jobs.add(Job.objects.get(pk=job_data))
#
