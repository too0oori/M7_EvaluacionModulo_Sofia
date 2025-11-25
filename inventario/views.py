from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, DetalleProducto, ProductoEtiqueta
from .forms import ProductoForm, EtiquetaForm, DetallesProductoForm, CategoriaForm, ProductoEtiquetaFormSet
from .models import Etiqueta, Categoria, DetalleProducto, Producto
from django.db.models import Q

#vista de inicio
def index(request):

    context = {
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_etiquetas': Etiqueta.objects.count(),
    }

    return render(request, 'index.html', context)

#vista de productos
def lista_productos(request):

    productos = Producto.objects.select_related('categoria').prefetch_related('etiquetas')
    
    # Filtros
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    
    categorias = Categoria.objects.all()

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'categorias': categorias
    })


def detalle_producto(request, id):

    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/detalle.html', {'producto': producto})


def crear_producto(request):

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        detalles_form = DetallesProductoForm(request.POST)
        
        if producto_form.is_valid() and detalles_form.is_valid():
            
            # Guardar el Producto primero (para obtener su ID)
            producto = producto_form.save()
            
            # - Guardar Detalles solo si hay datos
            # - Verifica si al menos uno de los campos tiene valor

            if detalles_form.cleaned_data.get('peso') or detalles_form.cleaned_data.get('dimensiones'): 

                detalles = detalles_form.save(commit=False)  # No guardar ahora
                detalles.producto = producto  # Asignar el producto recién creado
                detalles.save()  # Guardar los detalles
            
            # Guardar Etiquetas usando through 

            etiquetas_seleccionadas = producto_form.cleaned_data.get('etiquetas_seleccionadas')

            if etiquetas_seleccionadas:
                for orden, etiqueta in enumerate(etiquetas_seleccionadas, start=1):
                    ProductoEtiqueta.objects.create(
                        producto=producto,
                        etiqueta=etiqueta,
                        orden=orden
                    )
            
            messages.success(request, 'Producto creado exitosamente')
            return redirect('detalle_producto', id=producto.id)
        
        else:
            # Mensaje de errores
            messages.error(request, 'Por favor corrige los errores del formulario')
    else:
        producto_form = ProductoForm()
        detalles_form = DetallesProductoForm()
    
    return render(request, 'productos/crear.html', {
        'producto_form': producto_form,
        'detalles_form': detalles_form
    })


def editar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    # Manejo de excepciones para obtener detalles si existen

    try:
        detalles = producto.detalles

    except DetalleProducto.DoesNotExist:   # Si detalles no existen, asignar None
        detalles = None
    
    if request.method == 'POST':

        producto_form = ProductoForm(request.POST, instance=producto)
        
        # Formulario de detalles (existente o nuevo)
        if detalles:
            detalles_form = DetallesProductoForm(request.POST, instance=detalles)
        else:
            detalles_form = DetallesProductoForm(request.POST)
        
        # Formset de etiquetas
        etiquetas_formset = ProductoEtiquetaFormSet(request.POST, instance=producto)
        
        if producto_form.is_valid() and detalles_form.is_valid() and etiquetas_formset.is_valid():
            
            # Guardar producto
            producto_form.save()
            
            # Guardar o crear detalles SOLO si hay datos
            if detalles_form.cleaned_data.get('peso') or detalles_form.cleaned_data.get('dimensiones'):

                if not detalles:

                    # Crear nuevos detalles si no existen

                    detalles = detalles_form.save(commit=False)
                    detalles.producto = producto
                    detalles.save()

                else:

                    # Actualizar detalles existentes
                    detalles_form.save()

            elif detalles:

                # Si ya existían detalles pero ahora están vacíos, eliminarlos

                if not detalles_form.cleaned_data.get('peso') and not detalles_form.cleaned_data.get('dimensiones'):
                    detalles.delete()
            
            # Guardar etiquetas
            etiquetas_formset.save()
            
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('detalle_producto', id=producto.id)
        

        else:
            messages.error(request, 'Por favor corrige los errores del formulario') # Mensaje de errores

    else:
        producto_form = ProductoForm(instance=producto)
        detalles_form = DetallesProductoForm(instance=detalles) if detalles else DetallesProductoForm()
        etiquetas_formset = ProductoEtiquetaFormSet(instance=producto)
    
    return render(request, 'producto/editar.html', {
        'producto': producto,
        'producto_form': producto_form,
        'detalles_form': detalles_form,
        'etiquetas_formset': etiquetas_formset
    })



def eliminar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':

        nombre_producto = producto.nombre
        producto.delete()  # Esto también eliminará DetallesProducto por CASCADE definida en modelo
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente')
        return redirect('lista_productos')
    
    return render(request, 'producto/eliminar.html', {'producto': producto})

#vista de etiquetas

def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'etiquetas/lista.html', {'etiquetas': etiquetas})


def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta creada exitosamente')
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm()
    
    return render(request, 'etiquetas/formulario.html', {'form': form, 'accion': 'Crear'})


def editar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta actualizada exitosamente')
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm(instance=etiqueta)
    
    return render(request, 'etiquetas/formulario.html', {
        'form': form,
        'accion': 'Editar',
        'etiqueta': etiqueta
    })


def eliminar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    
    if request.method == 'POST':
        etiqueta.delete()
        messages.success(request, 'Etiqueta eliminada exitosamente')
        return redirect('lista_etiquetas')
    
    return render(request, 'etiquetas/eliminar.html', {'etiqueta': etiqueta})


#vista de categorias

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria
from .forms import CategoriaForm


def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})


def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    
    return render(request, 'categorias/formulario.html', {'form': form, 'accion': 'Crear'})


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'categorias/formulario.html', {
        'form': form, 
        'accion': 'Editar',
        'categoria': categoria
    })


def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('lista_categorias')
    
    return render(request, 'categorias/eliminar.html', {'categoria': categoria})