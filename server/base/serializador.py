from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Producto, Pedido, ArticuloPedido, Direccion, Revisado
from rest_framework_simplejwt.tokens import RefreshToken

class ProductoSerializado(serializers.ModelSerializer):
    revisados = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'
        
    def get_revisados(self, obj):
        revisados = obj.revisado_set.all()
        serializer = RevisadoSerializado(revisados, many=True)
        return serializer.data
        
class UserSerializado(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin']
        
    def get_name (self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
    
    def get__id (self, obj): 
        return obj.id
    
    def get_isAdmin (self, obj): 
        return obj.is_staff
    
class UserSerializadoConToken(UserSerializado):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin', 'token']
        
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    
class DireccionSerializado(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'
        
class ArticuloPedidoSerializado(serializers.ModelSerializer):
    class Meta:
        model = ArticuloPedido
        fields = '__all__'
        
class PedidoSerializado(serializers.ModelSerializer):
    articulosPedidos = serializers.SerializerMethodField(read_only=True)
    direccion = serializers.SerializerMethodField(read_only=True)
    usuario = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Pedido
        fields = '__all__'
        
    def get_articulosPedidos(self, obj):
        items = obj.articulopedido_set.all()
        serializer = ArticuloPedidoSerializado(items, many=True)
        return serializer.data
    
    def get_direccion(self, obj):
        try:
            direccion = obj.direccion
            serializer = DireccionSerializado(direccion, many=False)
            return serializer.data
        except:
            direccion = False
            return direccion
        
    def get_usuario(self, obj):
        usuario = obj.usuario
        serializer = UserSerializado(usuario, many=False)
        return serializer.data
    
class RevisadoSerializado(serializers.ModelSerializer):
    class Meta:
        model = Revisado
        fields = '__all__'
        
