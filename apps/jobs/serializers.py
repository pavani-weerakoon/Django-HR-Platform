from rest_framework import serializers
from apps.jobs.models import Job, Question, Section
from apps.users.models import Company


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['role', 'salary']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question_type', 'section']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['section_name']
