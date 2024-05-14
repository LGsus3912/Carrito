from django.urls import path
from base.vistas import productoVista as views


urlpatterns = [

    path('', views.getProductos, name='productos'),
    path('<str:pk>/', views.getProducto, name='producto'),
    path('eliminar/<str:pk>/', views.eliminarProducto, name='eliminar-producto'),
    path('actualizar/<str:pk>/', views.actualizarProducto, name='actualizar-producto'),
    path('crear', views.crearProducto, name='crear-producto'),
    path('subir', views.subirImagen, name='subir-imagen'),
    path('calificar/<str:pk>/', views.crearRevisado, name='calificar'),  
]