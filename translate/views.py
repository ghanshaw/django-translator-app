from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from translate.serializers import TranslationSerializer, LanguageSerializer
from rest_framework import viewsets
from translate.models import Translation
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
import urllib
import json
from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView

API_KEY = 'trnsl.1.1.20170902T190110Z.7ef50fbe6569ffd2.627f39cfa989999b2e20ed73921e10747ecc38cc'

def base(request):
    return render(request, "base.html")

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LanguageSerializer

    # Get list of supported languages
    def list(self, request, format=None):
        # Parameters for GET request
        params = urllib.parse.urlencode({
            'key': API_KEY, 
            'ui': 'en'
        })

        # Construct URL
        url = "https://translate.yandex.net/api/v1.5/tr.json/getLangs?%s" % params

        # Interpret response
        f = urllib.request.urlopen(url)
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        if not data:
            Response(500)
        # Deserialize data
        data = json.loads(data)

        # Return languages to client
        return Response(data)

    def get_queryset(self):
        return None

    


# Supports all operations on an endpoint
class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    
    # Customize POST method
    def create(self, request):
        # Get relevant data from request
        source_text = request.data['source_text']
        target_lang = request.data['target_lang']
    
        # Get params for GET request
        params = urllib.parse.urlencode({
            'key': API_KEY, 
            'text': source_text, 
            'lang': target_lang
        })

        # Construct URL
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?%s' % params 
        
        # Perform GET request to Yandex, decode result
        f = urllib.request.urlopen(url)
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        
        # Respond with error if request failed
        if not data:
            Response(500)
        
        # Deserialize data
        data = json.loads(data)

        # Aquire record values
        lang = data['lang'].split('-')
        target_text = data['text'][0]
        source_lang = lang[0]

        # Save translation to database
        record = Translation.objects.create(
            source_text=source_text,
            target_text=target_text,
            source_lang=source_lang,
            target_lang=target_lang
        )

        # Serialize and return data to client
        serializer = TranslationSerializer(record)
        json_data = JSONRenderer().render(serializer.data)
        return Response(json_data)