from django import forms
from .models import Producto, Etiqueta, Categoria, DetalleProducto

class ProductoForm(forms.ModelForm):
    # Campos extras para DetalleProducto
    dimension = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 20x30x15 cm'}),
        label='Dimensiones'
    )
    peso = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
        label='Peso (kg)'
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'etiquetas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'etiquetas': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'categoria': 'Categoría',
            'etiquetas': 'Etiquetas',
        }

    def save(self, commit=True):
        # Guardar el producto primero
        producto = super().save(commit=commit)

        # Solo crear/actualizar detalle si el producto está guardado
        if commit:
            dim = self.cleaned_data.get('dimension', '').strip()
            peso = self.cleaned_data.get('peso')

            if dim or peso:
                DetalleProducto.objects.update_or_create(
                    producto=producto,
                    defaults={'dimension': dim, 'peso': peso if peso is not None else None}
                )

        return producto

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la etiqueta'})}
        labels = {'nombre': 'Nombre'}

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'})}
        labels = {'nombre': 'Nombre'}
