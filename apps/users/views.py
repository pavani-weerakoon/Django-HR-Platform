from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from apps.jobs.models import Experience
from apps.users.serializers import ExperienceSerializer

from apps.users.permissions import AnonWriteOnly, NotAllowed
from apps.users.serializers import AuthRegisterSerializer, UserSerializer, PasswordChangeSerializer, \
    ProfileUpdateSerializer, UserRequestResetPasswordSerializer, UserResetPasswordSerializer, CandidateSerializer
from apps.users.models import User, UserType, Candidate
from apps.users.services import request_password_reset, create_candidate_user
from project import settings
from rest_framework import viewsets


class AuthViewSet(ViewSet):
    def get_permissions(self):
        if (self.action == 'register' and settings.SELF_REGISTER) or self.action == 'request_password_reset':
            permission_classes = [AnonWriteOnly]
        elif self.action == 'change_password':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [NotAllowed]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = AuthRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response()

    @action(methods=['post'], detail=False, url_path='request-password-reset')
    def request_password_reset(self, request):
        serializer = UserRequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = get_object_or_404(User, email=request.data['email'])
                request_password_reset(user)
            except Http404:
                pass
            finally:
                message = 'Password reset link has been sent to the registered email address.'
            return Response(message, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='reset-password')
    def reset_password(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def filter_queryset(self, queryset):
        return queryset.filter(Q(is_active=True) & ~Q(role=UserType.ADMIN))

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method == 'get':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            serializer = ProfileUpdateSerializer(
                data=request.data, instance=request.user, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return serializer.data


class CandidateViewSet(viewsets.ViewSet):

    def create(self, request):
        candidate_user = create_candidate_user(request.data, request)
        serializer = CandidateSerializer(candidate_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        user_candidates = User.objects.filter(
            company=request.user.company, user_type=UserType.CANDIDATE)
        _user_candidates = []
        for user_candidate in user_candidates:
            _user_candidates.append(user_candidate.candidate)

        serializer = CandidateSerializer(_user_candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['get', 'post', 'delete'],
        detail=False,
        url_name='candidate_experience',
        url_path='(?P<candidate_id>[^/.]+)/experiences',
    )
    def candidate_experience(self, request, candidate_id):
        candidate = get_object_or_404(Candidate, pk=candidate_id)

        if request.method == 'GET':
            candidate_experience = candidate.experiences.all()
            serializer = ExperienceSerializer(candidate_experience, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            serializer = ExperienceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(candidate=candidate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            experience_id = request.data['experience_id']
            experience = Experience.objects.get(id=experience_id)
            experience.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
