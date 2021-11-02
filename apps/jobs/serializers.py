from rest_framework import serializers
from apps.jobs.models import Job, Question, Section
from apps.users.models import Company


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        exclude = ['company']


class QuestionSerializer(serializers.ModelSerializer):
    section = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = ['question_type', 'section']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['section_name']
