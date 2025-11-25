from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F, Count
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Etiqueta, DetalleProducto
from .forms import ProductoForm, CategoriaForm, EtiquetaForm
from django.db.models import DecimalField, ExpressionWrapper, F
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'index.html')


def lista_productos(request):
    productos = Producto.objects.all()

    # filtros
    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria')
    min_precio = request.GET.get('min_precio')

    if busqueda:
        productos = productos.filter(Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda))

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if min_precio:
        try:
            min_val = float(min_precio)
            productos = productos.filter(precio__gte=min_val)
        except ValueError:
            pass

    productos = productos.exclude(precio=0)

    productos = productos.annotate(
        num_etiquetas=Count('etiquetas'),
        precio_con_iva=ExpressionWrapper(
            F('precio') * Decimal('1.19'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    # raw SQL: ejemplo de promedio global
    stats_raw = None
    try:
        qs = list(Producto.objects.raw('SELECT 1 as id, AVG(precio) as promedio FROM productos_producto'))
        if qs:
            stats_raw = qs[0]
    except Exception:
        stats_raw = None

    categorias = Categoria.objects.all()

    context = {
        'productos': productos,
        'categorias': categorias,
        'busqueda_actual': busqueda,
        'categoria_actual': categoria_id,
        'min_precio_actual': min_precio,
        'stats_raw': stats_raw,
    }
    return render(request, 'productos/lista.html', context)

@login_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            # Guardar producto sin relaciones M2M
            producto = form.save(commit=False)
            producto.save()

            # Guardar las etiquetas (M2M)
            form.save_m2m()

            return redirect('lista_productos')

    else:
        form = ProductoForm()

    return render(request, "productos/crear.html", {"form": form})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/detalle.html', {'producto': producto})

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    # precargar los valores de detalle al form
    detalle = getattr(producto, 'detalle', None)

    initial = {}
    if detalle:
        initial['dimension'] = detalle.dimension
        initial['peso'] = detalle.peso

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            prod = form.save()
            form.save_m2m()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto, initial=initial)

    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})

# CATEGORIAS

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/formulario.html', {'form': form})

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/formulario.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'categorias/eliminar.html', {'categoria': categoria})

# ETIQUETAS

@login_required
def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'etiquetas/lista.html', {'etiquetas': etiquetas})

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm()
    return render(request, 'etiquetas/formulario.html', {'form': form})

@login_required
def editar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'etiquetas/formulario.html', {'form': form, 'etiqueta': etiqueta})

@login_required
def eliminar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    if request.method == 'POST':
        etiqueta.delete()
        return redirect('lista_etiquetas')
    return render(request, 'etiquetas/eliminar.html', {'etiqueta': etiqueta})

# LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lista_productos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect("register")

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
        return redirect("login")

    return render(request, "register.html")