# 10tendencias - E-commerce de Productos Personalizables

## Descripción

**10tendencias** es una tienda online desarrollada en Django para la venta de productos personalizables con frases motivacionales. El objetivo es ofrecer una experiencia de compra moderna, intuitiva y visualmente atractiva, permitiendo a los usuarios elegir productos, personalizarlos y finalizar su compra de manera sencilla.

## Funcionalidades principales

- **Catálogo de productos**: Visualización de 10 productos personalizables (tazas, camisetas, hoodies, medias, gorras, agendas, bolsos, termos, macetas, mochilas) con descripción, imagen y botón de personalización.
- **Detalle de producto**: Página moderna con hero section, selección de frases motivacionales y personalización.
- **Carrito de compras**: Carrito funcional y responsivo, con contador de ítems, resumen, eliminación de productos y acceso al checkout.
- **Checkout**: Proceso de compra moderno, con formulario validado, selección dinámica de país, provincia y ciudad (incluye todas las provincias y principales ciudades de Ecuador), resumen del pedido y soporte para cupones de descuento.
- **Cupones de descuento**: Aplicación de cupones (ejemplo: "10DENCIAS" con 10% de descuento), visualización del descuento y total actualizado.
- **Pedido exitoso**: Página de confirmación con resumen del pedido y diseño consistente.
- **Gestión de sesión**: El carrito se almacena en la sesión del usuario para persistencia entre páginas.
- **Panel de administración**: Gestión de productos, frases, pedidos y datos de facturación desde el admin de Django.

## Patrones de diseño aplicados (con ejemplos)

- **MTV (Modelo-Template-Vista)**: Separación clara entre modelos (`models.py`), vistas (`views.py`) y templates (`templates/store/`).
  - *Ejemplo*: El modelo `Producto` define la estructura de los productos, la vista `catalogo` prepara los datos y el template `catalogo.html` los muestra.
- **Service Layer (Capa de Servicios)**: Lógica de negocio centralizada en servicios como `PedidoService` (`services.py`).
  - *Ejemplo*: `PedidoService` se encarga de crear pedidos, separando la lógica de negocio de las vistas.
- **Form Object**: Formularios personalizados para validación y procesamiento de datos de usuario (`forms.py`).
  - *Ejemplo*: `CheckoutForm` encapsula la validación de los datos de facturación y el cupón.
- **Factory**: Uso de `ValidatorFactory` (`validators.py`) para obtener validadores de identificación según el país.
  - *Ejemplo*: En `CheckoutForm`, se llama a `ValidatorFactory.get_validator(pais)` para obtener el validador adecuado. Esto permite agregar nuevos validadores fácilmente y ayuda a cumplir el principio OCP.
- **Strategy**: Validadores de identificación implementan diferentes estrategias según el país (`validators.py`).
  - *Ejemplo*: `EcuadorianIDValidator` y `ColombianIDValidator` implementan el método `validate` con reglas distintas, y el formulario usa la estrategia adecuada según el país.
- **Template Method**: Herencia de plantillas base (`base.html`) para mantener una estructura y diseño consistentes.
  - *Ejemplo*: `checkout.html` y `catalogo.html` extienden `base.html` y redefinen bloques específicos.
- **Repository (implícito)**: Acceso a datos a través del ORM de Django.
  - *Ejemplo*: `Producto.objects.all()` en las vistas permite acceder a los productos sin preocuparse por la lógica de acceso a datos.
- **Session Pattern**: Gestión del carrito y otros datos temporales en la sesión del usuario.
  - *Ejemplo*: El carrito se almacena y recupera usando `request.session['cart']` en las vistas.

## Principios SOLID implementados (con ejemplos)

- **SRP (Single Responsibility Principle)**: Cada clase y función tiene una única responsabilidad.
  - *Ejemplo*: `PedidoService` solo gestiona la creación de pedidos; `CheckoutForm` solo valida datos del formulario.
- **OCP (Open/Closed Principle)**: El sistema es fácilmente extensible sin modificar el código existente.
  - *Ejemplo*: Para agregar un nuevo tipo de validador de identificación, solo se crea una nueva clase y se registra en `ValidatorFactory`, sin modificar el formulario.
- **LSP (Liskov Substitution Principle)**: Las clases hijas pueden sustituir a la clase base sin alterar el funcionamiento.
  - *Ejemplo*: Cualquier clase que herede de `IDValidator` puede ser utilizada por el formulario sin romper la lógica.
- **ISP (Interface Segregation Principle)**: Las interfaces y clases están diseñadas para no forzar la implementación de métodos innecesarios.
  - *Ejemplo*: Cada validador implementa solo el método `validate` necesario para su país.
- **DIP (Dependency Inversion Principle)**: El formulario de checkout depende de abstracciones (validadores) y no de implementaciones concretas.
  - *Ejemplo*: `CheckoutForm` utiliza la interfaz `IDValidator` a través de la fábrica, sin depender de una clase concreta.

## Estructura del proyecto

```
10dencias-django/
├── manage.py
├── README.md
├── requirements.txt
├── store/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── services.py
│   ├── static/
│   ├── templates/
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
└── tendencias_project/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Instalación y ejecución

1. Clona el repositorio y accede a la carpeta del proyecto.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Realiza las migraciones con `python manage.py migrate`.
4. Crea un superusuario con `python manage.py createsuperuser` (opcional, para acceder al admin).
5. Ejecuta el servidor de desarrollo con `python manage.py runserver`.
6. Accede a la tienda en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Créditos

Desarrollado por [Tu Nombre] para la materia de Tendencias de Desarrollo de Software - UDLA.

## Frases motivacionales destacadas (ZenQuotes)

- El sistema permite importar automáticamente frases motivacionales desde la API pública de ZenQuotes (https://zenquotes.io/).
- Todas las frases importadas aparecen en el panel de administración, en la sección "Frases motivacionales".
- El administrador puede marcar hasta 3 frases como "destacadas" usando el campo booleano correspondiente.
- Solo las frases destacadas se mostrarán como opciones de personalización en la página de cada producto.
- Si no hay frases destacadas, se muestra un mensaje informativo en la web.
- Para importar nuevas frases, ejecuta:
  ```bash
  python manage.py import_zenquotes
  ```
