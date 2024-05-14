from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Producto, Revisado
from base.serializador import ProductoSerializado
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower

@api_view(['GET'])
def getProductos(request):
    search = request.query_params.get('buscar')
    if search == None:
        search = ''
    productos = Producto.objects.filter(nombre__icontains=search)
    if productos.count() == 0:
        productos = Producto.objects.filter(categoria__icontains=search)
    print(productos)
    page = request.query_params.get('page')
    print(page) 
    paginator = Paginator(productos, 8)
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)
        
    if page == None:
        page = 1
        
    page = int(page)
    
    serializador = ProductoSerializado(productos, many=True)
    return Response({'productos': serializador.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getProducto(request, pk):
    producto = Producto.objects.get(pk=pk)
    serializador = ProductoSerializado(producto)
    return Response(serializador.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def eliminarProducto(request, pk):
    producto = Producto.objects.get(id=pk)
    producto.delete()
    return Response('Producto eliminado')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def crearProducto(request):
    user = request.user
    producto = Producto.objects.create(
        usuario = user,
        nombre='Nombre',
        precio=0,
        marca='Marca',
        descripcion='Descripcion',
        cantidad=0,
        categoria='Categoria',
    )
    serializer = ProductoSerializado(producto, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def actualizarProducto(request, pk):
    data = request.data
    producto = Producto.objects.get(id=pk)
    producto.nombre = data['nombre']
    producto.precio = data['precio']
    producto.marca = data['marca']
    producto.descripcion = data['descripcion']
    producto.cantidad = data['cantidad']
    producto.categoria = data['categoria']
    producto.save()
    serializador = ProductoSerializado(producto, many=False)
    return Response(serializador.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def subirImagen(request):
    data = request.data
    producto_id = data['id']
    producto = Producto.objects.get(id=producto_id)
    producto.imagen = request.FILES.get('imagen')
    producto.save()
    return Response('Imagen subida')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crearRevisado(request, pk):
    user = request.user
    producto = Producto.objects.get(id=pk)
    data = request.data
    
    yaRevisado = producto.revisado_set.filter(usuario=user).exists()
    if yaRevisado:
        content = {'detail': 'Producto ya revisado'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    elif data['calificacion'] == 0:
        content = {'detail': 'La calificación no puede ser 0'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        revisado = Revisado.objects.create(
            usuario=user,
            producto=producto,
            nombre=user.first_name,
            calificacion=data['calificacion'],
            comentario=data['comentario'],
            fechaCreacion=datetime.now()
        )
        
        revisados = producto.revisado_set.all()
        producto.cantCalificaciones = len(revisados)
        
        total = 0
        for i in revisados:
            total += i.calificacion
            
        producto.calificacion = total / len(revisados)
        producto.save()
        return Response('Revisión creada')
    

    
