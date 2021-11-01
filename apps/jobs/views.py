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
from apps.jobs.service import get_question_for_job
from apps.jobs.models import Section

# Create your views here.


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    @action(
        methods=['get', 'post'],
        detail=False,
        url_name='question',
        url_path='(?P<job_id>[^/.]+)/questions',
    )
    def job_question(self, request, job_id):

        if request.method == 'GET':
            job = get_object_or_404(Job, pk=job_id)
            job_question = get_question_for_job(job)
            serializer = QuestionSerializer(job_question, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            job_request = request.data
            data_question = job_request['question_type']
            data_section = job_request['section']
            section_serializer = SectionSerializer(data=data_section)
            if(section_serializer.is_valid(raise_exception=True)):
                section_obj = section_serializer.save()

            question_serializer = QuestionSerializer(data=data_question)
            if(question_serializer.is_valid(raise_exception=True)):
                question_serializer.save(job=job_id, section=section_obj)

            return Response(question_serializer.data, satus=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
