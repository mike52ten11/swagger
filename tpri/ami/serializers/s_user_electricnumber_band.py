from rest_framework import serializers
from ..models import User, ElectricNumber,User_Banding_ElectricNumber

class UserElectricNumberBindingSerializer(serializers.Serializer):
    electricnumber = serializers.CharField(max_length=11)

    def validate_electricnumber(self, value):
        try:
            electric = ElectricNumber.objects.get(electricnumber=value)
            return electric
        except ElectricNumber.DoesNotExist:
            raise serializers.ValidationError("Electric number not found")





