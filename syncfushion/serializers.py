from rest_framework import serializers
from .models import GridSetting

class GridSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridSetting
        fields = ['id', 'name', 'data', 'user']