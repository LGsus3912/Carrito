from django.urls import path
from base.vistas import pedidoVista as views


urlpatterns = [
    path('anadir/', views.añadirArticuloPedido, name="anadir-articulo-pedido"),
    path( 'mispedidos/', views.getMisPedidos, name='mispedidos'),
    path('<str:pk>/', views.getPedidoId, name="pedido"),
    path('<str:pk>/pagar/', views.pagarPedido, name="pagar-pedido"),
    path('', views.getPedidos, name="pedidos"),
    path('<str:pk>/entregar/', views.actualizarEntrega, name="entregar-pedido"),
    
]