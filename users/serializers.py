from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, Profile, Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_name']



#
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_nm', 'login_ID', 'login_PW', 'age', 'gender', 'password']



class ProfileSerializer(serializers.ModelSerializer):
    related_user = UserSerializer(read_only=True)  # read_only=True 이거 안했더니 오류났음..뭐였더라. explicit .. .create() 어쩌고
    jobs = JobSerializer(source='get_jobs', required=False, many=True, allow_null=True)
    # def to_internal_value(self, data):
    #     # related_user_pk = data.get('related_user')
    #     related_user = data.get('related_user')
    #     internal_data = super().to_internal_value(data)
    #     try:
    #         #related_user = User.objects.get(pk=related_user_pk)
    #         related_user = User.objects.get(pk=related_user)
    #     except User.DoesNotExist:
    #         raise ValidationError(
    #             {'related_user' : ['Invalid related_user primary key']},
    #             code='invalid',
    #         )
    #     internal_data['related_user'] = related_user
    #     return internal_data

    class Meta:
        model = Profile
        fields = ['nickname', 'introduction', 'jobs', 'click_recomms', 'related_user']
       # depth=1
         # fields = ['nickname', 'introduction', 'jobs', 'click_recomms', 'related_user','phone_nm'
         #          , 'login_ID', 'login_PW', 'age', 'gender']
        # extra_kwargs = {
        #     'related_user' : {'source': 'related_user', 'write_only': True}
    #     # }
     #   def get_nested_field(self,model):
    # def __init__(self, *args, **kwargs):
    #     super(ProfileSerializer, self).__init__(*args,**kwargs)
    #     self.fields['nickname', 'introduction',  'related_user'].

    def create(self, validated_data):
        #request = self.context.get('request')
        related_user_data = validated_data.pop('related_user')
        related_user = User.objects.create(**related_user_data)
        jobs_data = validated_data.pop('jobs')
        jobs = Job.objects.create(**jobs_data)
        #related_user = UserSerializer.create(UserSerializer(), validated_data=related_user_data)
        #profile = Profile.objects.create(**validated_data)
        #related_user = User.objects.create(**related_user_data)
       # p_items = validated_data
       #  jobs = self.initial_data.get("jobs",[]) # list
       #  validated_data = list(zip(validated_data.keys(), validated_data.values())) #dict->list
       #  validated_data = validated_data + jobs
       #  validated_data = dict(validated_data)
        #validated_data #dict
        profile = Profile.objects.create(**validated_data, jobss=jobs, related_user=related_user)
        return profile
        # profile, created = Profile.objects.update_or_create(related_user=related_user,
        #                                                     nickname=validated_data.pop('nickname'),
        #                                                     introduction=validated_data.pop('introduction')
        #                                                     )
        #profile = Profile.objects.create(related_user=related_user, **validated_data)



       # Profile.objects.create(related_user=related_user_data)

        ##related_user = self.context['request'].user
        #profile = Profile.objects.create(related_user = related_user, **validated_data)
        #return profile


        # related_user_data = validated_data.pop('related_user') #User에 해당하는 데이터 pop으로 빼고
        # related_user = User.objects.create(related_user_data)
        # profile = Profile.objects.create(related_user, **validated_data)
        # #User.objects.create(profile=profile, **related_user_data)
        # # for user_data in users_data:
        # #     User.objects.create(profile=profile, **user_data)
        # return profile
    #??