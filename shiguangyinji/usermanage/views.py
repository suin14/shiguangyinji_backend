import os

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CheckUsernameExistView(APIView):
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "必须填写用户名"}, status=status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(username=username).exists()
        return Response({"exists": user_exists}, status=status.HTTP_200_OK)


class CheckPhoneExistView(APIView):
    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response({"error": "必须填写手机号"}, status=status.HTTP_400_BAD_REQUEST)

        if not phone.isdigit() or len(phone) != 11:
            return Response({"error": "手机号不合法，必须为11位数字"}, status=status.HTTP_400_BAD_REQUEST)

        phone_exists = User.objects.filter(phone=phone).exists()
        return Response({"exists": phone_exists}, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "用户名和密码是必填项"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            response = super().post(request, *args, **kwargs)
            response.data["message"] = "登录成功"
            return response
        else:
            return Response({"error": "用户名或密码错误"}, status=status.HTTP_401_UNAUTHORIZED)


class CheckLoginStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"logged_in": True, "username": request.user.username}, status=200)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 登出逻辑
        return Response(status=status.HTTP_200_OK)


class GetUserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response({"error": "用户未登录"}, status=status.HTTP_401_UNAUTHORIZED)

        # 获取用户的昵称、简介、文章数和粉丝数
        user_profile = {
            "nickname": request.user.nickname,
            "introduction": request.user.introduction,
            "article_count": request.user.article,
            "fans_count": request.user.fans
        }

        return Response(user_profile, status=status.HTTP_200_OK)


class EditUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "个人资料更新成功"}, status=200)
        return Response(serializer.errors, status=400)


class GetUserAvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return Response({"error": "用户未登录"}, status=401)

        avatar_filename = request.user.avatar  # e.g., 'avatars/suin.png'

        # 构建返回的图片URL，确保你返回的URL是基于你的项目地址
        avatar_url = f"http://127.0.0.1:8000/media/{avatar_filename}"

        # 返回图片的URL
        return Response({"avatar_url": avatar_url}, status=200)


class GetUserByIdView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            avatar_filename = request.user.avatar
            avatar_url = f"http://127.0.0.1:8000/media/{avatar_filename}"
            return Response({
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
                "introduction": user.introduction,
                "article_count": user.article,
                "fans_count": user.fans,
                "avatar_url": avatar_url
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)