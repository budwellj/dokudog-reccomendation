from rest_framework import serializers
from .models import Work, Theme

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['name']

class WorkSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)  # Use the ThemeSerializer for the themes field
    class Meta:
        model = Work
        fields = '__all__'
