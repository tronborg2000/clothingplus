from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from drf_yasg.utils import swagger_auto_schema
# Create your views here.
from rest_framework import status, permissions, views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers import CustomTokenObtainPairSerializer, GetFullUserSerializer, UserSerializerWithToken


class RegisterView(APIView):
    # authentication_classes = [AllowAny]
    permission_classes = [AllowAny]
    serializer_class = UserSerializerWithToken

    @swagger_auto_schema(
        request_body=UserSerializerWithToken,
        # responses={
        #     201: 'User registration successful',
        #     400: 'Bad request',
        # }
    )
    def post(self, request, *args, **kwargs):
        print('post')
        error_result = {}

        serializer = UserSerializerWithToken(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            print(access_token)

            output = "Successfully accounts created."
            content = {'status': True, 'message': output}
            return Response(content, status=status.HTTP_200_OK)
        content = {'status': False, 'message': serializer.errors, 'result': error_result}
        return Response(content, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed as e:
            # Handle the authentication failed exception
            error_message = 'Invalid email or password.'
            return self.custom_error_response(error_message)

        return self.process_response(response)

    def process_response(self, response):
        res = response.data

        if response.status_code == 200 and 'access' in res:
            email = self.request.data.get('email')
            user = User.objects.filter(email=email).first()

            if user:
                if not user.check_password(self.request.data.get('password')):
                    error_message = 'Invalid email or password.'
                    return self.custom_error_response(error_message)

                serializer = GetFullUserSerializer(user, context={'request': self.request})
                res['user'] = serializer.data
            else:
                error_message = 'Invalid email or password.'
                return self.custom_error_response(error_message)

        return Response(res)

    def custom_error_response(self, error_message):
        return Response({
            'status': False,
            'message': error_message,
            'result': {}
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return Response(status=204)


