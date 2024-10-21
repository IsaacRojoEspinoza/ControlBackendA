from django.contrib import admin
from django.urls import path, include
from Concentrado import views, userView
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas para registro y autenticación
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    # Comprobación del token
    path('api/check/', views.check_user, name='check_token'),

    # Rutas para el usuario
    path('api/user/', userView.userViewSet.as_view(), name='user_view_set'),

    # Rutas para las entidades, revisiones, estatus y control de materiales
    path('api/entidad/', views.entidadApi, name='entidad_api'),
    path('api/revision/', views.revisionApi, name='revision_api'),
    path('api/estatus/', views.estatusApi, name='estatus_api'),
    path('api/control-materiales/', views.controlMaterialesApi, name='control_materiales_api'),
]
