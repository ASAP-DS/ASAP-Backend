from django.http import Http404, JsonResponse

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response  # 이거 됨
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from search_job.models import SearchJobPost
from search_job.serializers import SearchJobPostSerializer
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

    # def put(self, request, pk):
    #     profile = self.get_object(pk)
    #     serializer = ProfileSerializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
