from rest_framework import serializers

from ..models import Skill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['id', 'user', 'title', 'description', 'proficiency_level']
