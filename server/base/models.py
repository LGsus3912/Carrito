from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100, null = True, blank = True)
    imagen = models.ImageField(null=True, blank=True, default='../static/image/fotoDefault.png')
    marca = models.CharField(max_length=100, null = True, blank = True)
    categoria = models.CharField(max_length=100, null = True, blank = True)
    descripcion = models.TextField(null=True, blank=True)
    calificacion = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    cantCalificaciones = models.IntegerField(null=True, blank=True, default=0)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True , default=0)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    id=models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return self.nombre
    

    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    metodoDePago = models.CharField(max_length=100, null = True, blank = True)
    precioEnvio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    precioTotal = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    fechaPedido = models.DateTimeField(auto_now_add=True)
    fechaPago = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    completado = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    fechaEntrega = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    id=models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.fechaPedido)
    
class Direccion(models.Model):
    pedido=models.OneToOneField(Pedido, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.CharField(max_length=100, null = True, blank = True)
    ciudad = models.CharField(max_length=100, null = True, blank = True)
    cp = models.CharField(max_length=100, null = True, blank = True)
    pais = models.CharField(max_length=100, null = True, blank = True)
    precioEnvio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    id=models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.direccion)

class ArticuloPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100, null = True, blank = True)
    cantidad = models.IntegerField(null=True, blank=True, default=0)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    imagen = models.CharField(max_length=100, null = True, blank = True)
    id=models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.nombre)
    
class Revisado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100, null = True, blank = True)
    calificacion = models.IntegerField(null=True, blank=True, default=0)
    comentario = models.TextField(null=True, blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    id=models.AutoField(primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.calificacion)
    


