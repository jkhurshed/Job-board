from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class CategoryDetailSerializer(CategorySerializer):

    class Meta(CategorySerializer.Meta):
        pass
