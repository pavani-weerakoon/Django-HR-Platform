from rest_framework import serializers
from apps.jobs.models import Job, Question, Section
from apps.users.models import Company


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        exclude = ['company']


class QuestionSerializer(serializers.ModelSerializer):
    section = serializers.CharField(read_only=True)
    # question_type = question_typeSerializer(many=True, required=False)

    class Meta:
        model = Question
        exclude = ['job']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['section_name']
