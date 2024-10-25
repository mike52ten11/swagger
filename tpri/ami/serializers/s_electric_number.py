


from rest_framework import serializers
from ..models import ElectricNumber

class ElectricNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricNumber
        fields = ['electricnumber', 'name']

class ElectricNumber_Update_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricNumber
        fields = ['electricnumber', 'name']
        extra_kwargs = {
            'electricnumber': {
                'validators': []  # 移除 UniqueValidator 用於更新操作
            }
        }        