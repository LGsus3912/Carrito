from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.serializador import UserSerializado, UserSerializadoConToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializador = UserSerializadoConToken(self.user).data
        for k, v in serializador.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer







@api_view(['POST'])
def registroUsuario(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializador = UserSerializadoConToken(user, many=False)
        return Response(serializador.data)
    except:
        mensaje = {'detail': 'Este correo ya está registrado'}
        return Response(mensaje, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePerfilUser(request):
    user = request.user
    serializador = UserSerializadoConToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializador.data)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPerfilUser(request):
    user = request.user
    serializador = UserSerializado(user, many=False)
    return Response(serializador.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsuarios(request):
    Usuarios = User.objects.all()
    serializador = UserSerializado(Usuarios, many=True)
    return Response(serializador.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def eliminarUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response('Usuario eliminado')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsuarioPorId(request, pk):
    user = User.objects.get(id=pk)
    serializador = UserSerializado(user, many=False)
    return Response(serializador.data)




@api_view(['PUT'])
@permission_classes([IsAdminUser])
def actualizarUsuario(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']
    user.save()
    serializador = UserSerializado(user, many=False)

    return Response(serializador.data)