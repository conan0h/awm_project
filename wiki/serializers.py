# wikipedia/serializers.py
from rest_framework import serializers
from .models import WikipediaArticle

class WikipediaArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikipediaArticle
        fields = '__all__'
