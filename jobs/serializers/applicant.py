from rest_framework import serializers

from ..models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ['id', 'name', 'skill']


class ApplicantDetailSerializer(ApplicantSerializer):

    class Meta(ApplicantSerializer.Meta):
        fields = ApplicantSerializer.Meta.fields + ['user']
