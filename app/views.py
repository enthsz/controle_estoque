from django.shortcuts import render
from rest_framework.decorators import api_view
from . serializers import ProductSerializer, SaleSerializer
from . models import Product, Sale
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


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
    serializer = ProductSerializer(data=request.data)
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
        return Response({'error': 'Produto nao existente'}, status=status.HTTP_400_BAD_REQUEST)



#############


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_sale(request):
    data = request.data
    product_id = data['produto_id']
    quantidade = data['quantidade']

    if 'produto_id' not in data or 'quantidade' not in data:
        return Response({'error': 'Dados faltando'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(id=product_id)

        if product.quantidade_em_estoque >= int(quantidade):
            if int(quantidade) == 0:
                return Response({'error': 'Nao pode fazer a venda, pois voce nao adicionou item nenhum'})
            product.quantidade_em_estoque -= int(quantidade)
            product.save()

            existing_sale = Sale.objects.filter(produto_id=product_id).first()
            if existing_sale:
                existing_sale.quantidade += int(quantidade)
                existing_sale.save()
                sale_serializer = SaleSerializer(existing_sale)
                return Response(sale_serializer.data,status=status.HTTP_200_OK)
            else:
                sale = Sale.objects.create(produto_id=product_id, quantidade=quantidade)
                sale.save()
                sale_serializer = SaleSerializer(sale)
                return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Quantidade em estoque insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_history(request):
    try:
        sale = Sale.objects.all()
        serializer = SaleSerializer(sale, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Sale.DoesNotExist:
        return Response({'error': 'Venda nao realizada'}, status=status.HTTP_404_NOT_FOUND)





