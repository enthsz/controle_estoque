from django.shortcuts import render
from rest_framework.decorators import api_view
from . serializers import ProductSerializer, SaleSerializer
from . models import Product, Sale
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
import decimal


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_product(request):
    product = Product.objects.all()
    if not product.exists():
        return Response({'detail': 'Voce nao tem produtos cadastrados'}, status=status.HTTP_204_NO_CONTENT)
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    data = request.data
    name = data.get('nome')
    serializer = ProductSerializer(data=request.data)

    if Product.objects.filter(nome=name).exists():
        return Response({'error': 'Produto ja existente no estoque'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail(request, product_name):
    try:
        food = Product.objects.get(nome=product_name)
        serializer = ProductSerializer(food, many=False)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, product_name):
    try:
        product = Product.objects.get(nome=product_name)
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_name):
    try:
        product = Product.objects.get(nome=product_name)
        product.delete()
        return Response({'detail': 'Produto excluido'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Esse produto nao existe'}, status=status.HTTP_400_BAD_REQUEST)



# Registrar venda e historico de venda

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_sale(request):
    data = request.data
    product_id = data.get('produto_id')
    sold = data.get('vendidos')
    profit = data.get('lucro')

    if not product_id or not sold or not profit:
        return Response({'error': 'Dados faltando'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(id=product_id)

        if product.quantidade_em_estoque >= int(sold):
            if int(sold) == 0:
                return Response({'error': 'Nao pode fazer a venda, pois voce nao adicionou nenhum item em quantidade'})
            
            product.quantidade_em_estoque -= int(sold)
            product.save()

            
            existing_sale = Sale.objects.filter(produto_id=product).first()
            if existing_sale:
                existing_sale.vendidos += int(sold)
                profit = decimal.Decimal(profit)
                existing_sale.lucro += profit
                existing_sale.save()
                sale_serializer = SaleSerializer(existing_sale)
                return Response(sale_serializer.data,status=status.HTTP_200_OK)
            else:
                sale = Sale.objects.create(produto_id=product, vendidos=sold, lucro=profit)
                sale.save()
                sale_serializer = SaleSerializer(sale)
                return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
                
            

        else:
            return Response({'error': 'Quantidade em estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def sales_history(request):
    try:
        sale = Sale.objects.all()
        serializer = SaleSerializer(sale, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Sale.DoesNotExist:
        return Response({'error': 'Venda nao realizada'}, status=status.HTTP_404_NOT_FOUND)





