from django.db import models

# Create your models here.
#El modelo Producto debe tener campos como nombre, descripción, precio y una relación con el modelo Categoría.

class Producto (models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='productos')
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
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='detalle')
    dimension = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalles de {self.producto.nombre}"
    
class ProductoEtiqueta(models.Model):


    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        related_name='producto_etiquetas'
    )

    etiqueta = models.ForeignKey(
        Etiqueta, 
        on_delete=models.CASCADE,
        related_name='producto_etiquetas'
    )
    
    # Campos adicionales de la relación
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    # Campo de orden para prioridad de las etiquetas
    orden = models.PositiveIntegerField(
        default= 1,
        help_text="Orden de prioridad de la etiqueta (1 = más importante)"
    )
    
    class Meta:
        verbose_name = "Producto-Etiqueta"
        verbose_name_plural = "Productos-Etiquetas"
        unique_together = ('producto', 'etiqueta') # Evita duplicados cuando se asigne una etiqueta a un producto
        ordering = ['orden', 'fecha_asignacion']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.etiqueta.nombre}"