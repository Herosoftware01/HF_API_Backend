from rest_framework import serializers

from .models import QcAdminMistake,Unit, Line

class QcAdminMistakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QcAdminMistake
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'