from django.contrib import admin
from django.urls import path, include
from inventario import views as inventario_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
    

        # Autenticación
    path('login/', inventario_views.login_view, name='login'),
    path('logout/', inventario_views.logout_view, name='logout'),
    path('register/', inventario_views.register_view, name='register'),
]
