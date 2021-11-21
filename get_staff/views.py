from django.http import Http404, JsonResponse, HttpResponse

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response  # 이거 됨
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from get_staff.models import GetStaffPost, CommentGetStaff
from get_staff.serializers import GetStaffPostSerializer, CommentGetStaffSerializer, CommentPostSerializer, \
    SortPostSerializer
from users.models import Profile



@api_view(['GET'])
def sort_high_pay(request): # 시급 높은순으로
    posts = GetStaffPost.objects.all().order_by('-hourly_pay')
    serializer = SortPostSerializer(posts, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def sort_high_pay(request): # 시급 높은순으로
#     posts = GetStaffPost.objects.all().order_by('-hourly_pay')
#     serializer = GetStaffPostSerializer(posts, many=True)
#     return Response(serializer.data)

class GetStaffPostList(APIView):
    def get(self, request):
        posts = GetStaffPost.objects.all()
        serializer = GetStaffPostSerializer(posts, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GetStaffPostSerializer(data=data)
        if serializer.is_valid(raise_exception=ValueError):
            post = serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt  #모야이건...했더니 계속 function object has no attribute 'as_view'에러
class GetStaffPostDetail(APIView):
    def get_object(self, pk):
        try:
            return (
                GetStaffPost.objects.get(pk=pk)
            )
        except GetStaffPost.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = GetStaffPostSerializer(post)
        return Response(serializer.data)


class CommentGetStaffList(APIView):
    def get(self, request, pk):
        comments = CommentGetStaff.objects.filter(post = pk)
        serializer = CommentGetStaffSerializer(comments, many=True)
        return Response(serializer.data)

    # @csrf_exempt
    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     serializer = GetStaffPostSerializer(data=data)
    #     # profile_id = serializer.data['profile']
    #     # profile = Profile.objects.get(pk=profile_id)
    #     # jobs_ids = serializer.data['jobs']  # list 형태?
    #     if serializer.is_valid(raise_exception=ValueError):
    #         post = serializer.save()
    #         return Response(serializer.data, status.HTTP_201_CREATED)
    #     return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt  #모야이건...했더니 계속 function object has no attribute 'as_view'에러
class CommentGetStaffDetail(APIView):
    def get_object(self, pk, pk2):
        try:
            return (
                CommentGetStaff.objects.get(post=pk, pk=pk2)
            )
        except CommentGetStaff.DoesNotExist:
            raise Http404

    def get(self, request, pk, pk2):
        comment = self.get_object(pk, pk2)
        serializer = CommentGetStaffSerializer(comment)
        return Response(serializer.data)




@api_view(['POST', 'GET'])
def add_comment(request):
    if request.method == "POST":
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.data['post_id']
            profile_id = serializer.data['profile_id']
            content = serializer.data['content']
            is_anon = serializer.data['is_anon']
            if post_id in GetStaffPost.objects.all().values_list('pk', flat=True):
                post = GetStaffPost.objects.get(pk=post_id)
                profile = Profile.objects.get(pk=profile_id)
                CommentGetStaff.objects.create(content=content, is_anon=is_anon, post=post, profile=profile)
                data = {
                    "post_id": post_id,
                    "profile_id": profile_id,
                    "content": content,
                    "is_anon": is_anon
                }
                return Response(data, status=status.HTTP_200_OK)
            else:  # 존재하는 게시글 없음
                return HttpResponse(status=400)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    else: # 'get'
        return Response(status=status.HTTP_200_OK)