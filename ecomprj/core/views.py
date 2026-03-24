# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import UserProfile, Skill, Swap, Review, Message
# from .serializers import (
#     RegisterSerializer, UserProfileSerializer, SkillSerializer,
#     SwapSerializer, CreateSwapSerializer, ReviewSerializer, MessageSerializer
# )

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'token': str(refresh.access_token),
#                 'user': UserProfileSerializer(user).data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(username=email, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'token': str(refresh.access_token),
#                 'user': UserProfileSerializer(user).data
#             })
#         return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(UserProfileSerializer(request.user).data)

# class UploadImageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user_profile = request.user.profile
#         if 'image' in request.FILES:
#             user_profile.profile_image = request.FILES['image']
#             user_profile.save()
#             return Response({
#                 'message': 'Image uploaded successfully',
#                 'user': UserProfileSerializer(request.user).data
#             })
#         return Response({'message': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

# class SkillListCreateView(generics.ListCreateAPIView):
#     serializer_class = SkillSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user_id = self.request.query_params.get('user_id')
#         queryset = Skill.objects.all().order_by('-created_at')
#         if user_id:
#             queryset = queryset.filter(user_id=user_id)
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({'skills': serializer.data})

# class SwapListCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = CreateSwapSerializer(data=request.data)
#         if serializer.is_valid():
#             swap = serializer.save(sender=request.user)
#             return Response(SwapSerializer(swap).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserSwapsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         swaps = Swap.objects.filter(sender_id=user_id) | Swap.objects.filter(receiver_id=user_id)
#         swaps = swaps.order_by('-created_at')
#         return Response({'swaps': SwapSerializer(swaps, many=True).data})

# class SwapStatusUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         try:
#             swap = Swap.objects.get(pk=pk)
#         except Swap.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
            
#         status_val = request.data.get('status')
#         if status_val in ['accepted', 'rejected', 'completed']:
#             swap.status = status_val
#             swap.save()
#             return Response(SwapSerializer(swap).data)
#         return Response({'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

# class ReviewCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         reviewee_id = request.data.get('reviewee_id')
#         rating = request.data.get('rating', 5)
#         comment = request.data.get('comment', '')
        
#         if not reviewee_id:
#             return Response({'message': 'reviewee_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
#         review = Review.objects.create(
#             reviewer=request.user,
#             reviewee_id=reviewee_id,
#             rating=rating,
#             comment=comment
#         )
#         return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

# class MessageListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, swap_id):
#         messages = Message.objects.filter(swap_id=swap_id).order_by('created_at')
#         return Response(MessageSerializer(messages, many=True).data)

# class MessageCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         swap_id = request.data.get('swap_id')
#         content = request.data.get('content')
#         if swap_id and content:
#             msg = Message.objects.create(swap_id=swap_id, sender=request.user, content=content)
#             return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)
#         return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)