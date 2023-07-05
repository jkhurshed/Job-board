from rest_framework import serializers

from ..models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'company', 'salary']


class JobDetailSerializer(JobSerializer):

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + ['description', 'created_at']
