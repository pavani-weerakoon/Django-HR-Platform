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
import itertools
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
            print(request.user)
            job_questions = job.questions.all()
            print(type(job_questions))
            serializer = QuestionSerializer(job_questions, many=True)
            print(type(serializer))
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            lists = []
            value = request.data
            for dic in value:
                data_question = dic['question_type']
                data_section = dic['section']
                sec_dict = {"section_name": data_section}
                quesList = []

                for x in data_question:
                    quesList.append({"question_type": x})

                section_serializer = SectionSerializer(data=sec_dict)
                if section_serializer.is_valid(raise_exception=True):
                    section_obj = section_serializer.save()

                question_serializer = QuestionSerializer(
                    data=quesList, many=True)

                if question_serializer.is_valid(raise_exception=True):
                    quesList_obj = question_serializer.save(
                        job=job, section=section_obj)
                    lists.append(quesList_obj)

            new_list = itertools.chain(*lists)
            question_serializer = QuestionSerializer(
                new_list, many=True)

            return Response(question_serializer.data, status=status.HTTP_201_CREATED)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
