from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, help_text="The natural language message from the user.")
