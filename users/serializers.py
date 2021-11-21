from abc import ABC
# read_onlu 이거 input에는 포함되지 않고 output에만 보여줌. read_only가 포함되면 serializer가 무시함
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, Profile, Job


class LoginSerializer(serializers.Serializer):
    login_ID = serializers.CharField(max_length=20, style={'input_type': 'login_ID'})
    login_PW = serializers.CharField(max_length=20, style={'input_type': 'login_PW'})


class JobsSetSerializer(serializers.Serializer):
    # 기존의 job도 새로운 job도 다 보내줘 (원래있던 job안쓰면 삭제되는거!....음....
    jobs_list = serializers.ListField(
        child=serializers.IntegerField(),
        style={'input_type': 'jobs_list'}
    )
    related_user_id = serializers.IntegerField(style={'input_type': 'related_user_id'})


class JobSerializer(serializers.ModelSerializer):  # ProfileSerializer의 nested_field로 사용  + 모든 직종 조회 view에서 사용
    class Meta:
        model = Job
        fields = ['id', 'job_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_nm', 'login_ID', 'login_PW', 'age', 'gender', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    related_user = UserSerializer(read_only=True)
    jobs = JobSerializer(required=False, many=True, allow_null=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['related_user_id', 'nickname', 'introduction', 'jobs', 'recomms_cnt', 'related_user']

    def create(self, validated_data):
        related_user_data = validated_data.pop('related_user')
        related_user = User.objects.create(**related_user_data)
        jobs_data = validated_data.pop('jobs')
        # job_dic = {'job_name': j.job_name}
        profile = Profile.objects.create(**validated_data,
                                         related_user=related_user)  # Direct assignment to the forward side of a many-to-many set is prohibited. Use jobs.set() instead.
        profile.jobs.add(Job.objects.get(pk=1))
        # for job_data in jobs_data:
        #     job, is_job_created = Job.objects.get_or_create(jobs_data)
        #     if is_job_created:
        #         job.save()
        #     profile.jobs.add(job_data)
        return profile

    def validate(self, data):  # data 는 APIView의 request.data  , jobs필드는 받지 않고 create하고 싶어서
        if data.get('jobs', None) is None:
            j = Job.objects.get(pk=1)  # 없어도됨 view에 validate사용한거 수정 귀찮아서 냅둔거ㅓ..
        # aa = str(a)
        # data.get['jobs'] == a # 'builtin_function_or_method' object is not subscriptable
        # data.get['jobs'] += {"id":a, "job_name": n}
        # data['jobs'] = [22]
        # if data.get('click_recomms', None) == None:
        #     self_id = Profile.objects.all().count() + 1 # 이거 완전 안되네 생각해보니까!오류나면 3번 다음이 막7이잔ㅇ하
        #     #data.get['click_recomms']= [self_id]
        #     data.get['click_recomms'] = [self.id]
        return data


# 글고 받아온 두 아이디 비교하고 추가하고 그걸 view에서 해주는거잖아 post겠네 인스턴스추가니까
class RecommSerializer(serializers.Serializer):
    to_prof_id = serializers.IntegerField(style={'input_type': 'to_prof_id'})
    related_user_id = serializers.IntegerField(style={'input_type': 'related_user_id'})

    # class Meta:
    #     model = None
    # 지금 로그인되어있는 prof_id 랑   추천 누르려는 상대의 prof_id
    #    fields = ['related_user', 'to_prof_id']
