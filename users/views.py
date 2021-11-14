import json
from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from rest_framework.views import APIView

from users.models import User, Profile, Job
from users.serializers import ProfileSerializer, RecommSerializer, JobSerializer, JobsSetSerializer, LoginSerializer


def main(request):
    return render(
        request,
        'users/main.html',
    )


class ProfileList(APIView):
    # 회원 조회
    def get(self, request):
        # 모든 profile 불러옴. ORM은 .all() 사용
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    # 회원 가입
    @csrf_exempt
    def post(self, request):
        data = request.data
        # serializer = ProfileSerializer(data=request.data, partial=True)
        serializer = ProfileSerializer(data=data, partial=True)
        # jobs = serializer.data['jobs']  # list 형태?
        # recomms = serializer.data['recomms'] # list형태?
        if serializer.is_valid(raise_exception=ValueError):
            serializer.validate(data)
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt  #모야이건...했더니 계속 function object has no attribute 'as_view'에러
class ProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return (
                Profile.objects.get(pk=pk)
            )
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # 회원 정보 수정
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Join(APIView):
#     def post(self, request):  #근데 굳이 이렇게 말고..def join

# 일단 지금 추천수 (추천한 사람 id랑 추천받은 사람 id 받아오면. 그걸 recomm테이블에 추가 ) 이미 추천해있는지 확인하고 ㅇㅇ
# 같은url일 필요가..있..

@api_view(['POST', 'GET'])
def recomm(request):
    if request.method == 'POST':
        serializer = RecommSerializer(data=request.data)
        if serializer.is_valid():
            # from_prof_id = serializer.data['related_user_id']  # 여기서 KeyError..
            to_prof_id = serializer.data['to_prof_id']
            p1 = Profile.objects.get(
                related_user_id=serializer.data['related_user_id'])  # Profile matching query does not exist.
            p2 = Profile.objects.get(related_user_id=to_prof_id)
            if p1.already_clicked(to_prof_id):
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                p1.click_recomms.add(p2)
                return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


    else:  # GET
        # serializer = RecommSerializer(data=request.data)
        # if serializer.is_valid():
        return Response(status=status.HTTP_200_OK)


# 그냥 serializer안쓰면 안되나..?

@api_view(['PUT', 'GET'])
def job(request):
    if request.method == 'PUT':
        serializer = JobsSetSerializer(data=request.data)
        if serializer.is_valid():
            jobs_list = serializer.data['jobs_list']
            related_user_id = serializer.data['related_user_id']
            profile = Profile.objects.get(pk=related_user_id)
            # jobs_now_list = profile.jobs.all().values_list('id', flat=True)
            profile.jobs.clear()  # 지금 회원 jobs다 지우기.. (이게맞을까..?)
            for job_id in jobs_list:  # 받아온 job id 리스트 순회
                # 현재 회원의 jobs에 없을 때 (추가해주기)  # 이제 지웠으니까 당연히 없음
                # if job_id not in jobs_now_list:
                profile.jobs.add(Job.objects.get(pk=job_id))
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:  # GET
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def login(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login_ID = serializer.data['login_ID']
            login_PW = serializer.data['login_PW']
            if login_ID in User.objects.all().values_list('login_ID', flat=True):
                user = User.objects.get(login_ID=login_ID)
                user_id = user.pk
                if user.login_PW == login_PW:  # 패스워드 확인
                    return Response(user_id, status=status.HTTP_200_OK)  # 로그인 성공
                else:
                    return HttpResponse(status=401)  # # 패스워드 불일치

            else:  # id 존재 X
                return HttpResponse(status=400)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    else: # 'get'
        return Response(status=status.HTTP_200_OK)


class JobList(APIView):
    # 모든 직종 조회
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)