from rest_framework import serializers
from translate.models import Translation
from django.contrib.auth.models import User

class TranslationSerializer(serializers.ModelSerializer):
    source_text = serializers.CharField()
    target_text = serializers.CharField()
    source_lang = serializers.CharField()
    target_lang = serializers.CharField()
    date_time = serializers.DateTimeField()
    
    class Meta:
        model = Translation
        fields = [
            'source_text', 
            'target_text', 
            'source_lang', 
            'target_lang',
            'date_time'
        ]

    def create(self, validated_data):
        return Translation.objects.create(**validated_data)

class LanguageSerializer(serializers.Serializer):
    None

