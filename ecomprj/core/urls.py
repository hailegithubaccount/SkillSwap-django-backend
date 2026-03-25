from django.urls import path
from . import views

urlpatterns = [
    path('auth/register', views.RegisterView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/profile', views.ProfileView.as_view(), name='profile'),
    # path('auth/upload-image', views.UploadImageView.as_view(), name='upload_image'),
    # path('skills', views.SkillListCreateView.as_view(), name='skills'),
    # path('swaps', views.SwapListCreateView.as_view(), name='swaps'),
    # path('swaps/user/<int:user_id>', views.UserSwapsView.as_view(), name='user_swaps'),
    # path('swaps/<int:pk>/status', views.SwapStatusUpdateView.as_view(), name='swap_status'),
    # path('reviews', views.ReviewCreateView.as_view(), name='reviews'),
    # path('messages/<int:swap_id>', views.MessageListView.as_view(), name='message_list'),
    # path('messages', views.MessageCreateView.as_view(), name='message_create'),
]
