from rest_framework import serializers
from .models import Product, Sale
from django.utils import timezone

class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        
        value = timezone.localtime(value)
        return value.strftime('%d-%m-%Y %H:%M:%S')



class ProductSerializer(serializers.ModelSerializer):
    data_criada = CustomDateTimeField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id','nome','quantidade_em_estoque','preco_de_compra','preco_de_venda','data_criada']


class SaleSerializer(serializers.ModelSerializer):
    data_venda = CustomDateTimeField(required=False, allow_null=True)

    class Meta:
        model = Sale
        fields = ['produto_id','quantidade', 'data_venda']