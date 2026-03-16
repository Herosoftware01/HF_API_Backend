from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import GridSetting
from .serializers import GridSettingSerializer
from rest_framework.permissions import IsAuthenticated  # optional

class GridSettingViewSet(viewsets.ModelViewSet):
    queryset = GridSetting.objects.all()
    serializer_class = GridSettingSerializer