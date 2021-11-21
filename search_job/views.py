from django.http import Http404, JsonResponse, HttpResponse

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response  # 이거 됨
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from search_job.models import SearchJobPost, CommentSearchJob
from search_job.serializers import SearchJobPostSerializer, CommentSearchJobSerializer, CommentPostSerializer
from users.models import Profile


# class GetStaffPostViewSet(viewsets.ModelViewSet):
#     queryset = GetStaffPost.objects.all()
#     serializer_class = GetStaffPostSerializer
#
#     def perform_create(self, serializer):
#         serializer.save()
#





class SearchJobPostList(APIView):
    def get(self, request):
        posts = SearchJobPost.objects.all()
        serializer = SearchJobPostSerializer(posts, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SearchJobPostSerializer(data=data)
        # profile_id = serializer.data['profile']
        # profile = Profile.objects.get(pk=profile_id)
        # jobs_ids = serializer.data['jobs']  # list 형태?
        if serializer.is_valid(raise_exception=ValueError):
            post = serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt  #모야이건...했더니 계속 function object has no attribute 'as_view'에러
class SearchJobPostDetail(APIView):
    def get_object(self, pk):
        try:
            return (
                SearchJobPost.objects.get(pk=pk)
            )
        except SearchJobPost.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = SearchJobPostSerializer(post)
        return Response(serializer.data)


class CommentSearchJobList(APIView):
    def get(self, request, pk):
        comments = CommentSearchJob.objects.filter(post = pk)
        serializer = CommentSearchJobSerializer(comments, many=True)
        return Response(serializer.data)


# @csrf_exempt  #모야이건...했더니 계속 function object has no attribute 'as_view'에러
class CommentSearchJobDetail(APIView):
    def get_object(self, pk, pk2):
        try:
            return (
                CommentSearchJob.objects.get(post=pk, pk=pk2)
            )
        except CommentSearchJob.DoesNotExist:
            raise Http404

    def get(self, request, pk, pk2):
        comment = self.get_object(pk, pk2)
        serializer = CommentSearchJobSerializer(comment)
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
            if post_id in SearchJobPost.objects.all().values_list('pk', flat=True):
                post = SearchJobPost.objects.get(pk=post_id)
                profile = Profile.objects.get(pk=profile_id)
                CommentSearchJob.objects.create(content=content, is_anon=is_anon, post=post, profile=profile)
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