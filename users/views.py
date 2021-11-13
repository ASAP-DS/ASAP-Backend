import json
from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from rest_framework.views import APIView

from users.models import User, Profile
from users.serializers import ProfileSerializer


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


#@csrf_exempt  #모야이건...했더니 계속 function object has no attribute 'as_view'에러
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
#