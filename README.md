# ProductManager  
Sistema de Gestion de Productos con Django, PostgreSQL y Bootstrap

ProductManager es una aplicacion web desarrollada en Django cuyo objetivo es gestionar productos, categorias, etiquetas y detalles asociados.  
Incluye autenticacion de usuarios, operaciones CRUD completas, consultas avanzadas con ORM, uso de PostgreSQL y una interfaz totalmente construida con Bootstrap.

Este proyecto fue desarrollado como evaluacion del Módulo 7 del Bootcamp de Desarrollo Full Stack Python de Skillnest.

---

## 🚀 Caracteristicas principales

### 🔹 CRUD completo
- Productos  
- Categorias  
- Etiquetas  
- Detalle de producto (relacion Uno a Uno)

### 🔹 Relaciones entre modelos
- **Muchos a Uno**: Producto → Categoria  
- **Muchos a Muchos**: Producto ↔ Etiquetas  
- **Uno a Uno**: Producto → DetalleProducto (dimensiones, peso)

### 🔹 Autenticacion
- Login  
- Logout  
- Registro de usuarios  
- Restriccion de vistas con `@login_required`  
- Gestion independiente por usuario (cada usuario ve solo sus productos)

### 🔹 Consultas con el ORM
- Filtros con `filter()`  
- Exclusiones con `exclude()`  
- Busquedas avanzadas (`Q`)  
- Anotaciones: cantidad de etiquetas, precio con IVA  
- Raw SQL para estadisticas globales

### 🔹 Seguridad
- Proteccion CSRF  
- Middleware de Django  
- Restriccion de acciones a usuarios autenticados  
- Uso de Django Auth en combinacion con vistas personalizadas

### 🔹 Frontend
- Templates basados en Bootstrap 5  
- Formularios limpios  
- Confirmaciones de eliminacion  
- Listados con tablas responsive  
- Alertas de feedback (mensajes)

---

## 📦 Tecnologias utilizadas

- **Python 3.12**  
- **Django 5.2**  
- **PostgreSQL**  
- **Bootstrap 5**  
- **HTML5 / CSS3**

---

## 🛠 Instalacion y configuracion

### 1. Clonar repositorio
```bash
git clone https://github.com/too0oori/M7_EvaluacionModulo_Sofia.git
cd ProductManager
```

### 2. Crear entorno virtual
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL
```sql
CREATE DATABASE productmanager;
```

Configurar en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'productmanager',
        'USER': 'postgres',
        'PASSWORD': 'TU_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Ejecutar servidor
```bash
python manage.py runserver
```

---

## 📁 Estructura del proyecto

```
ProductManager/
│
├── inventario/              # App principal
│   ├── models.py            # Modelos: Producto, Categoria, Etiqueta, DetalleProducto
│   ├── views.py             # Vistas basadas en funciones (FBV)
│   ├── forms.py             # Formularios ModelForm
│   ├── urls.py              # Rutas de la app
│   └── templates/           # Templates HTML con Bootstrap
│
├── ProductManager/          # Configuracion del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── manage.py
```

---

## 🧠 Decisiones de diseño

### 🔵 Por que usar vistas basadas en funciones (FBV)?

1. **Claridad para aprendizaje**  
   Las FBV muestran explicitamente cada paso (obtener datos, validar, guardar, redirigir).  
   Ideal para comprender la logica completa del flujo.

2. **Control total del proceso**  
   Facilita operaciones complejas como:  
   - manejo de `commit=False`  
   - guardado de modelo principal y detalles  
   - relaciones M2M  
   - manejo de multiples formularios en una sola vista  

3. **Debugging mas claro**  
   Es mas facil leer y entender una funcion que una clase generica con metodos ocultos.

4. **Alineado con la pauta del modulo**  
   El proyecto pide comprender CRUD “desde cero”, lo cual se muestra mejor con FBV.

---

### 🔵 Por que una sola app (“inventario”)?

1. **Simplificacion para el modulo**  
   Todas las funcionalidades pertenecen al mismo dominio: productos y su gestion.

2. **Evita sobre-arquitectura**  
   Dividir el proyecto en varias apps pequeñas (productos, categorias, usuarios, filtros) no aportaria valor aqui.

3. **Orden coherente**  
   Tener todos los modelos relacionados en una misma app facilita aprendizaje y mantenibilidad.

4. **Escalable**  
   Si se agregan nuevas funciones (reportes, facturacion), pueden crearse nuevas apps mas adelante sin romper nada.

---

## 🔗 Rutas implementadas

### Inicio
- `/`

### Productos
- `/productos/`
- `/productos/crear/`
- `/productos/<id>/`
- `/productos/<id>/editar/`
- `/productos/<id>/eliminar/`

### Categorias
- `/categorias/`
- `/categorias/crear/`
- `/categorias/<id>/editar/`
- `/categorias/<id>/eliminar/`

### Etiquetas
- `/etiquetas/`
- `/etiquetas/crear/`
- `/etiquetas/<id>/editar/`
- `/etiquetas/<id>/eliminar/`

### Autenticacion
- `/login/`
- `/logout/`
- `/register/`

---

## 📊 Consultas ORM utilizadas

- `filter()`
- `exclude()`
- `Q` para busquedas avanzadas
- `annotate()` y `Count()`
- `ExpressionWrapper()` para precio con IVA
- Raw SQL con `raw()` para estadisticas

---

## 🔒 Seguridad

- Proteccion CSRF  
- Restriccion con `login_required`  
- Middleware de autenticacion  
- Aislamiento por usuario (cada usuario ve solo sus productos)

---

## 📸 Capturas

### Lista de productos
![Lista de productos](screenshots/lista_productos.jpg)

### Login
![Login](screenshots/login.jpg)

### Crear producto
![Crear producto](screenshots/crear_producto.jpg)

---

## ✅ Conclusión

ProductManager es un sistema completo que demuestra dominio de:

✔ Modelos y relaciones avanzadas  
✔ Migraciones y PostgreSQL  
✔ CRUD profesional con Django  
✔ Formularios ModelForm personalizados  
✔ Raw SQL y filtros ORM  
✔ Autenticacion con vistas personalizadas  
✔ Diseño responsivo con Bootstrap  
✔ Arquitectura clara y mantenible  

---

## 📄 Licencia
Proyecto academico. Libre para estudio y aprendizaje.

