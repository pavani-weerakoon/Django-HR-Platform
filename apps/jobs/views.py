from django.db.models.query import QuerySet
from django.shortcuts import render
from apps.jobs.models import Job, Company, Question
from apps.jobs.serializers import JobSerializer, QuestionSerializer, SectionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.jobs.models import Section, Question
import ast

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
            data_question = request.data['question_type']
            data_section = request.data['section']

            sec_dict = {"section_name": data_section}
            ques_dict = {"question_type": data_question}

            section_serializer = SectionSerializer(data=sec_dict)
            if section_serializer.is_valid(raise_exception=True):
                section_obj = section_serializer.save()

            question_serializer = QuestionSerializer(data=ques_dict)
            if question_serializer.is_valid(raise_exception=True):
                question_serializer.save(job=job, section=section_obj)

            return Response(question_serializer.data, status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
