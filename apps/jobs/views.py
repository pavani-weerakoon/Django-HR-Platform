from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.fields import flatten_choices_dict
from apps.jobs.models import Job, Company, Question
from apps.jobs.serializers import JobSerializer, QuestionSerializer, SectionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.jobs.models import Question
from apps.users.models import Candidate
from apps.jobs.service import add_cantidate_to_job, add_questions
import ast

from apps.users.serializers import CandidateSerializer, UserCandidateSerializer

# Create your views here.


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    @action(
        methods=['get', 'post'],
        detail=False,
        url_name='job_question',
        url_path='(?P<job_id>[^/.]+)/questions',
    )
    def job_question(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        if request.method == 'GET':
            job_questions = job.questions.all()
            serializer = QuestionSerializer(job_questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            questions = add_questions(request.data, job)
            serializer = QuestionSerializer(
                questions, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['get', 'post', 'delete'],
        detail=False,
        url_name='job_candidate',
        url_path='(?P<job_id>[^/.]+)/candidates',
    )
    def job_candidate(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        if request.method == 'GET':
            job_candidates = job.candidates.all()
            candidate_users = []
            for candidate in job_candidates:
                candidate_users.append(candidate.user)
            serializer = UserCandidateSerializer(candidate_users, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'POST':
            candidate_ids = request.data["candidate"]
            candidate_users = add_cantidate_to_job(candidate_ids, job)
            serializer = UserCandidateSerializer(candidate_users, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            candidate_id = request.data["candidate"]
            candidate = Candidate.objects.get(id=candidate_id)
            job.candidates.remove(candidate)
            return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
