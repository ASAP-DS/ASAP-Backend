from rest_framework import serializers

from users.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_nm', 'login_ID', 'login_PW', 'age', 'gender']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['nickname', 'introduction', 'jobs', 'click_recomms', 'user']

    def create(self, validated_data):
        users_data = validated_data.pop('user')
        profile = Profile.object.crete(**validated_data)
        for user_data in users_data:
            User.objects.create(profile=profile, **user_data)
        return profile

# class ProfileDetailSerializer(serializers.ModelSerializer):
#     user_ = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Profile
#         fields = ['nickname', 'introduction', 'jobs', 'click_recomms', 'user_']
