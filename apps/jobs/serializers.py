from rest_framework import serializers
from apps.jobs.models import Job
from apps.users.models import Company


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['role', 'salary']
