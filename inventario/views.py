from django.shortcuts import render
from models import Producto, Etiqueta, Categoria, DetalleProducto

def index(request):
    productos = Producto.objects.all()
    etiquetas = Etiqueta.objects.all()
    categorias = Categoria.objects.all()
    detalles = DetalleProducto.objects.all()
    return render(request, 'index.html', {'productos': productos, 'etiquetas': etiquetas, 'categorias': categorias, 'detalles': detalles})

# Vistas para productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    detalles = DetalleProducto.objects.filter(producto=producto)
    return render(request, 'detalle_producto.html', {'producto': producto, 'detalles': detalles})

def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        categoria_id = request.POST['categoria']
        etiquetas = request.POST.getlist('etiquetas')

        producto = Producto.objects.create(nombre=nombre, descripcion=descripcion, precio=precio, categoria_id=categoria_id)
        producto.etiquetas.set(etiquetas)

        return render(request, 'detalle_producto.html', {'producto': producto})
    else:
        categorias = Categoria.objects.all()
        etiquetas = Etiqueta.objects.all()
        return render(request, 'crear_producto.html', {'categorias': categorias, 'etiquetas': etiquetas})
    
def editar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.categoria_id = request.POST['categoria']
        producto.etiquetas.clear()
        producto.etiquetas.set(request.POST.getlist('etiquetas'))
        producto.save()
        return render(request, 'detalle_producto.html', {'producto': producto})
    else:
        categorias = Categoria.objects.all()
        etiquetas = Etiqueta.objects.all()
        return render(request, 'editar_producto.html', {'producto': producto, 'categorias': categorias, 'etiquetas': etiquetas})
    

def eliminar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return render(request, 'eliminar_producto.html', {'producto': producto})

#Vistas para categorias

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        Categoria.objects.create(nombre=nombre)
        return render(request, 'crear_categoria.html', {'categorias': Categoria.objects.all()})
    else:
        return render(request, 'crear_categoria.html', {'categorias': Categoria.objects.all()})

def eliminar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    categoria.delete()
    return render(request, 'eliminar_categoria.html', {'categoria': categoria})

def editar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']
        categoria.save()
        return render(request, 'editar_categoria.html', {'categoria': categoria})
    else:
        return render(request, 'editar_categoria.html', {'categoria': categoria})
    
#Vistas para etiquetas

def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'lista_etiquetas.html', {'etiquetas': etiquetas})

def crear_etiqueta(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        Etiqueta.objects.create(nombre=nombre)
        return render(request, 'crear_etiqueta.html', {'etiquetas': Etiqueta.objects.all()})
    else:
        return render(request, 'crear_etiqueta.html', {'etiquetas': Etiqueta.objects.all()})
    
def eliminar_etiqueta(request, etiqueta_id):
    etiqueta = Etiqueta.objects.get(id=etiqueta_id)
    etiqueta.delete()
    return render(request, 'eliminar_etiqueta.html', {'etiqueta': etiqueta})

def editar_etiqueta(request, etiqueta_id):
    etiqueta = Etiqueta.objects.get(id=etiqueta_id)
    if request.method == 'POST':
        etiqueta.nombre = request.POST['nombre']
        etiqueta.save()
        return render(request, 'editar_etiqueta.html', {'etiqueta': etiqueta})
    else:
        return render(request, 'editar_etiqueta.html', {'etiqueta': etiqueta})
    
