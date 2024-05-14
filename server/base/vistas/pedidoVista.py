from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import Producto, Pedido, ArticuloPedido, Direccion
from base.serializador import ProductoSerializado, PedidoSerializado, ArticuloPedidoSerializado, DireccionSerializado
from rest_framework import status
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def añadirArticuloPedido(request):
    user = request.user
    data = request.data
    articuloPedido = data['pedidoItems']
    if articuloPedido and len(articuloPedido) == 0:
        return Response({'detalle': 'No hay articulos en el pedido'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        pedido = Pedido.objects.create(
            usuario=user,
            metodoDePago=data['metodoPago'],
            precioEnvio=data['precioEnvio'],
            precioTotal=data['precioTotal']
        )
        direccion = Direccion.objects.create(
            pedido=pedido,
            direccion=data['direccionEnvio']['direccion'],
            ciudad=data['direccionEnvio']['ciudad'],
            cp=data['direccionEnvio']['cp'],
            pais=data['direccionEnvio']['pais'],            
        )
        for i in articuloPedido:
            producto = Producto.objects.get(id=i['producto'])
            item = ArticuloPedido.objects.create(
                producto=producto,
                pedido=pedido,
                nombre=producto.nombre,
                cantidad=i['cant'],
                precio=i['precio'],
                imagen=producto.imagen.url
            )
            producto.cantidad -= item.cantidad
            producto.save()
        serializer = PedidoSerializado(pedido, many=False)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPedidoId(request, pk):
    user = request.user
    try:
        pedido = Pedido.objects.get(id=pk)
        if user.is_staff or pedido.usuario == user:
            serializer = PedidoSerializado(pedido, many=False)
            return Response(serializer.data)
        else:
            return Response({'detalle': 'No tienes permiso para ver este pedido'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detalle': 'Pedido no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])   
def pagarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.completado = True
    pedido.fechaPago = datetime.now()
    pedido.save()
    return Response('El pedido ha sido pagado')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMisPedidos(request):
    user = request.user
    pedidos = user.pedido_set.all()
    serializer = PedidoSerializado(pedidos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPedidos(request):
    pedidos = Pedido.objects.all()
    serializer = PedidoSerializado(pedidos, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def actualizarEntrega(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.entregado = True
    pedido.fechaEntrega = datetime.now()
    pedido.save()
    return Response('Pedido entregado')