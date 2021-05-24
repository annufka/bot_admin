from django.core import serializers

from cabinet.models import Directory


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Directory
        fields = '__all__'