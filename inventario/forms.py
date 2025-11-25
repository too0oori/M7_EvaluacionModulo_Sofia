#FORMULARIOS

from django import forms
from .models import Producto, Etiqueta, Categoria, DetalleProducto, ProductoEtiqueta

class ProductoForm(forms.ModelForm):

    # Campo personalizado para etiquetas con orden
    
    etiquetas_seleccionadas = forms.ModelMultipleChoiceField(
        queryset=Etiqueta.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Etiquetas"
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Si estamos editando, cargar etiquetas actuales
            self.fields['etiquetas_seleccionadas'].initial = self.instance.etiquetas.all()


# Formset para manejar múltiples relaciones ProductoEtiqueta
ProductoEtiquetaFormSet = forms.inlineformset_factory(
    Producto,
    ProductoEtiqueta,
    fields=('etiqueta', 'orden'),
    extra=1,
    can_delete=True,
    widgets={
        'etiqueta': forms.Select(attrs={'class': 'form-control'}),
        'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
    }
)

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la etiqueta'
            }),
        }
        labels = {
            'nombre': 'Nombre',
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
        }
        labels = {
            'nombre': 'Nombre',
        }

class DetallesProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['dimension', 'peso']
        widgets = {
            'dimension': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

