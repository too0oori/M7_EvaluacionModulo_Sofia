from django.db import models

# Create your models here.
#El modelo Producto debe tener campos como nombre, descripción, precio y una relación con el modelo Categoría.

class Producto (models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    etiquetas = models.ManyToManyField('Etiqueta')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre
    
class Categoria (models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre
    
class Etiqueta (models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.nombre

class DetalleProducto (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    dimension = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.producto