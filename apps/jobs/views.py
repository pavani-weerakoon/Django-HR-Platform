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
import ast

from apps.users.serializers import CandidateSerializer

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
            all_questions = []

            for dic in request.data:
                data_question = dic['question_type']
                data_section = dic['section']
                sec_dict = {"section_name": data_section}
                questions = []

                for x in data_question:
                    questions.append({"question_type": x})

                section_serializer = SectionSerializer(data=sec_dict)
                if section_serializer.is_valid(raise_exception=True):
                    sections = section_serializer.save()

                question_serializer = QuestionSerializer(
                    data=questions, many=True)
                if question_serializer.is_valid(raise_exception=True):
                    ques = question_serializer.save(
                        job=job, section=sections)
                    all_questions.append(ques)

            flat_list = []
            for sublist in all_questions:
                for item in sublist:
                    flat_list.append(item)
            serializer = QuestionSerializer(
                flat_list, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_name='job_candidate',
        url_path='(?P<job_id>[^/.]+)/candidates',
    )
    def job_candidate(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        if request.method == 'POST':
            candidate_id = request.data["candidate"]
            candidate = Candidate.objects.get(id=candidate_id)
            job.candidates.add(candidate)
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'delete':
            candidate_id = request.data["candidate"]
            candidate = Candidate.objects.get(id=candidate_id)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
