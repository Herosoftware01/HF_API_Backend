from rest_framework import serializers
from .models import GridSetting,TrsMaildtls

class GridSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridSetting
        fields = ['id', 'name', 'data','user']


class TrsMaildtlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrsMaildtls
        fields = '__all__'