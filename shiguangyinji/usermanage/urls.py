from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, CheckUsernameExistView, CheckPhoneExistView, LoginView, CheckLoginStatusView, \
    LogoutView, GetUserProfileView, EditUserProfileView, GetUserAvatarView, GetUserByIdView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-username/', CheckUsernameExistView.as_view(), name='check-username-exist'),
    path('check-phone/', CheckPhoneExistView.as_view(), name='check-phone-exist'),
    path('login/', LoginView.as_view(), name='login'),
    path('check-login/', CheckLoginStatusView.as_view(), name='check-login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("get-profile/", GetUserProfileView.as_view(), name="get_profile"),
    path('edit-profile/', EditUserProfileView.as_view(), name='edit-profile'),
    path('get-avatar/', GetUserAvatarView.as_view(), name='get_user_avatar'),
    path('user/<int:user_id>/', GetUserByIdView.as_view(), name='get_user_by_id'),
]
