#FORMULARIOS

from django import forms
from .models import Producto, Etiqueta, Categoria, DetalleProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'etiquetas']


class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['producto', 'dimension', 'peso']