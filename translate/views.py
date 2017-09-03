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

# from persmissions import IsOwnerOrReadOnly

# Create your views here.
def input(request):
    html_var = 'f string'
    return render(request, "input.html", { "html_var" : html_var })

def base(request):
    return render(request, "base.html")

# Create your views here.
def result(request):
    html_var = 'f string'
    return render(request, "result.html", { "html_var" : html_var })

API_KEY = 'trnsl.1.1.20170902T190110Z.7ef50fbe6569ffd2.627f39cfa989999b2e20ed73921e10747ecc38cc'

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LanguageSerializer


    def list(self, request, format=None):
        
        # print(request.data)

        params = urllib.parse.urlencode({
            'key': API_KEY, 
            'ui': 'en'
        })

        url = "https://translate.yandex.net/api/v1.5/tr.json/getLangs?%s" % params
        print(url)
        f = urllib.request.urlopen(url)
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')

        data = json.loads(data)
        return Response(data)

    def get_queryset(self):
        return None

    


# Supports all operations on an endpoint
class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    print('look here')
    # permission_classes = (IsOwnerOrReadOnly,)
    # @list_route(methods=['post','get'])
    # def list(self, request, pk=None):   
    #     data = serializer_class(queryset)
    #     # data = 'Hello There'
    #     # print('this is happening')
    #     return Response(data)

    # var url = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs?'
    
    # key=<API key>
    #  & [ui=<language code>]
    #  & [callback=<name of the callback function>]


    def create(self, request):
        print(request)
        source_text = request.data['source_text']
        target_lang = request.data['target_lang']
        print(request.data)

        params = urllib.parse.urlencode({
            'key': API_KEY, 
            'text': source_text, 
            'lang': target_lang
        })
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?%s' % params 
        print(url)
        f = urllib.request.urlopen(url)
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        print(data)

        data = json.loads(data)

        lang = data['lang'].split('-')
        target_text = data['text'][0]
        source_lang = lang[0]

        print(source_text, target_text, source_lang, target_lang)

        record = Translation.objects.create(
            source_text=source_text,
            target_text=target_text,
            source_lang=source_lang,
            target_lang=target_lang
        )

        serializer = TranslationSerializer(record)
        json_data = JSONRenderer().render(serializer.data)
        return Response(json_data)
        record.save()
        

        
        print('data')
        # http = HttpRequest()
        # http.method = 'GET'
        # http.content_params['key'] = API_KEY
        # http.content_params['text'] = source_text
        # http.content_params['lang'] = 'ru'
        return Response(record)

    # # Get called before object is saved to database
    # def pre_save(self, obj):
    #     obj.owner = self.request.user
