from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Skill, Swap, Review, Message

class SkillUserSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    name = serializers.CharField(source='first_name', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['_id', 'name', 'profile_image']

    def get_profile_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_image:
            return obj.profile.profile_image.url
        return None

class TinySkillSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    class Meta:
        model = Skill
        fields = ['_id', 'title']

class SkillSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    user_id = SkillUserSerializer(source='user', read_only=True)

    class Meta:
        model = Skill
        fields = ['_id', 'user_id', 'title', 'description', 'category', 'type', 'created_at']


    _id = serializers.ReadOnlyField(source='id')
    name = serializers.CharField(source='first_name', read_only=True)
    email = serializers.CharField(read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'location', 'profile_image']

    def get_profile_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_image:
            return obj.profile.profile_image.url
        return None
