from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, Profile, Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['job_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone_nm', 'login_ID', 'login_PW', 'age', 'gender', 'password']



class ProfileSerializer(serializers.ModelSerializer):
    related_user = UserSerializer(read_only=True)  # read_only=True 이거 안했더니 오류났음..뭐였더라. explicit .. .create() 어쩌고
    jobs = JobSerializer(source='get_jobs', required=False, many=True, allow_null=True)

    class Meta:
        model = Profile
        fields = ['related_user_id','nickname', 'introduction', 'jobs', 'recomms_cnt', 'related_user']


# 회원가입
# 회원가입 시 보낼 정보 -> id, pw, name, age, gender, phone_nm, nickname, introduction
class JoinSerializer(serializers.ModelSerializer):
    related_user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['related_user', 'nickname', 'introduction']