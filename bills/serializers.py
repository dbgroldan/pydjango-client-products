from rest_framework import serializers
from bills.models import Bill


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'
