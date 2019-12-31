from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import UwpathApp, CourseInfo, Coreqs, Prereqs, Antireqs, Requirements
from .serializer import AppSerializer, CourseInfoSerializer, CoreqsSerializer, AntireqsSerializer, PrereqsSerializer, RequirementsSerializer


# Create your views here.

def index(request):
    return render(request, 'index.html')

class AllApp(APIView):
    queryset = UwpathApp.objects.all()
    serializer_class = AppSerializer

    def post(self, request, format=None):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppView(APIView):
    def get(self, request, pk, format=None):
        try:
            app = UwpathApp.objects.get(pk=pk)
            serializer = AppSerializer(app)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        app = UwpathApp.objects.get(pk=pk)
        app.delete()
        return Response(status=status.HTTP_200_OK)

class Course_Info_API(APIView):
    def get(self, request, pk, format=None):
        try:
            app = CourseInfo.objects.get(pk=pk)
            serializer = CourseInfoSerializer(app)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object(self, request, pk, format=None):
        try:
            app = CourseInfo.objects.get(pk=pk)
            return app
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Course_Info_List(APIView):
    def get(self, request, format=None):
        list = CourseInfo.objects.all()[:10]
        serializer = CourseInfoSerializer(list, many=True)
        return Response(serializer.data)

class Coreqs_API(APIView):
    def get(self, request, pk, format=None):
        try:
            app = Coreqs.objects.get(pk=pk)
            serializer = CoreqsSerializer(app)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object(self, request, pk, format=None):
        try:
            app = Coreqs.objects.get(pk=pk)
            return app
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Coreqs_List(APIView):
    def get(self, request, format=None):
        list = Coreqs.objects.all()[:10]
        serializer = CoreqsSerializer(list, many=True)
        return Response(serializer.data)

class Prereqs_API(APIView):
    def get(self, request, pk, format=None):
        try:
            #if no primary key, then default go by id
            app = Prereqs.objects.get(pk=pk)
            serializer = PrereqsSerializer(app)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object(self, request, pk, format=None):
        try:
            app = Prereqs.objects.get(pk=pk)
            return app
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Prereqs_List(APIView):
    def get(self, request, format=None):
        list = Prereqs.objects.all()[:10]
        serializer = PrereqsSerializer(list, many=True)
        return Response(serializer.data)


class Antireqs_API(APIView):
    def get(self, request, pk, format=None):
        try:
            app = Antireqs.objects.get(pk=pk)
            serializer = AntireqsSerializer(app)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object(self, request, pk, format=None):
        try:
            app = Antireqs.objects.get(pk=pk)
            return app
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Antireqs_List(APIView):
    def get(self, request, format=None):
        list = Antireqs.objects.all()[:10]
        serializer = AntireqsSerializer(list, many=True)
        return Response(serializer.data)

class Requirements_API(APIView):
    def get(self, request, pk, format=None):
        try:
            app = Requirements.objects.get(pk=pk)
            serializer = RequirementsSerializer(app)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object(self, request, pk, format=None):
        try:
            app = Requirements.objects.get(pk=pk)
            return app
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Requirements_List(APIView):
    def get(self, request, format=None):
        list = Requirements.objects.all()[:10]
        serializer = RequirementsSerializer(list, many=True)
        return Response(serializer.data)