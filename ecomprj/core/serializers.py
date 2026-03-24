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

class SwapSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    sender_id = SkillUserSerializer(source='sender', read_only=True)
    receiver_id = SkillUserSerializer(source='receiver', read_only=True)
    offered_skill_id = TinySkillSerializer(source='offered_skill', read_only=True)
    requested_skill_id = TinySkillSerializer(source='requested_skill', read_only=True)

    class Meta:
        model = Swap
        fields = ['_id', 'sender_id', 'receiver_id', 'offered_skill_id', 'requested_skill_id', 'message', 'status', 'created_at']

class CreateSwapSerializer(serializers.ModelSerializer):
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='receiver')
    offered_skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='offered_skill')
    requested_skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='requested_skill')
    
    class Meta:
        model = Swap
        fields = ['receiver_id', 'offered_skill_id', 'requested_skill_id', 'message']

class ReviewSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    class Meta:
        model = Review
        fields = ['_id', 'reviewer', 'reviewee', 'rating', 'comment', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    sender_id = SkillUserSerializer(source='sender', read_only=True)
    class Meta:
        model = Message
        fields = ['_id', 'swap', 'sender', 'sender_id', 'content', 'created_at']

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    location = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name']
        )
        UserProfile.objects.create(user=user, location=validated_data['location'])
        return user

class UserProfileSerializer(serializers.ModelSerializer):
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
