import json
from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from rest_framework.views import APIView

from users.models import User, Profile
from users.serializers import ProfileSerializer, RecommSerializer


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
        #serializer = ProfileSerializer(data=request.data, partial=True)
        serializer = ProfileSerializer(data=data,partial=True)
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
            p1 = Profile.objects.get(related_user_id=serializer.data['related_user_id'])  # Profile matching query does not exist.
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