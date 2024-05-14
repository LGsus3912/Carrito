from django.urls import path
from base.vistas import userVista as views


urlpatterns = [
    path('', views.getUsuarios, name='usuarios'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('perfil/', views.getPerfilUser, name='perfil'),
    path('registro/', views.registroUsuario, name='registro'),
    path('perfil/actualizar/', views.updatePerfilUser, name='perfil-actualizar'),
    path ('eliminar/<str:pk>/', views.eliminarUser, name='eliminar-usuario'),
    path('actualizar/<str:pk>/', views.actualizarUsuario, name='actualizar-usuario'),
    path('<str:pk>/', views.getUsuarioPorId, name='usuario'),
]