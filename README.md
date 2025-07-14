# 10dencias - E-commerce de Productos Personalizables

## Descripción

10dencias es una plataforma e-commerce innovadora, construida con el framework Django, que permite a los usuarios personalizar productos como tazas, camisetas y hoodies con frases motivacionales inspiradoras. Surge como respuesta a la creciente demanda de experiencias de compra únicas, potenciando la conexión emocional con cada artículo adquirido.

El sistema está diseñado con una arquitectura modular que separa claramente la lógica de negocio, la gestión de datos y la presentación visual, adhiriéndose a los principios SOLID y a las buenas prácticas de desarrollo para garantizar un código mantenible, escalable y fácil de documentar.

---

## Funcionalidades Principales

### Para Clientes

* Catálogo de Productos: Explora un catálogo de 10 productos personalizables (tazas, camisetas, hoodies, medias, gorras, agendas, bolsos, termos, macetas, mochilas), cada uno con su descripción, imagen y un botón de personalización.

* Detalle de Producto y Personalización: Accede a una página de producto moderna que incluye una "hero section", la selección de frases motivacionales de un catálogo curado y opciones de personalización.

* Carrito de Compras: Disfruta de un carrito funcional y responsivo, con un contador de ítems, resumen de los productos, opción para eliminar artículos y acceso directo al proceso de compra.

* Proceso de Compra (Checkout): Completa tu compra a través de un proceso moderno con un formulario validado, selección dinámica de país, provincia y ciudad (con soporte para todas las provincias y principales ciudades de Ecuador mediante AJAX), resumen detallado del pedido y soporte para cupones de descuento.

* Cupones de Descuento: Aplica cupones como "10DENCIAS" (con un 10% de descuento) para ver el descuento aplicado y el total actualizado en tu pedido.

* Gestión de Sesión: El carrito de compras y otros datos temporales se almacenan en la sesión del usuario, asegurando la persistencia de la información entre diferentes páginas.

### Para Administradores

* Panel de Administración: Gestiona de forma centralizada productos, frases motivacionales, pedidos y datos de facturación a través del panel de administración de Django.

* Gestión de Frases Motivacionales: Importa automáticamente frases desde la **API pública de ZenQuotes**, edítalas, elimínalas y selecciona hasta tres como "destacadas" para que aparezcan de forma resaltada en la personalización de productos.

---

## Restricciones y Limitaciones del Proyecto

Para mantener el enfoque en la calidad y la viabilidad del producto base, 10dencias cuenta con las siguientes restricciones:

* Sin Comunicación entre Usuarios: No incluye módulos de mensajería, comentarios, valoraciones o cualquier tipo de interacción social entre clientes.

* Sin Gestión de Inventario en Tiempo Real: El control de stock de productos debe realizarse manualmente desde el panel de administración, no hay un sistema automático.

* Sin Integración con Pasarelas de Pago Reales: El sistema no procesa pagos en línea ni se integra con servicios de pago externos (ej. PayPal, Stripe). El flujo de compra finaliza con la confirmación del pedido.

* Sin Gestión de Envíos: No incluye funcionalidades para la gestión de envíos, seguimiento de pedidos o notificaciones automáticas al usuario sobre el estado de su orden.

---

## Arquitectura y Patrones de Diseño

10dencias está construido sobre el framework **Django**, adoptando una arquitectura que garantiza la **mantenibilidad, escalabilidad y flexibilidad**. Se han aplicado los siguientes principios y patrones de diseño:

### Principios SOLID

* SRP (Single Responsibility Principle - Principio de Responsabilidad Única): Cada clase o módulo tiene una única razón para cambiar.
    * Ejemplo: La lógica compleja de creación de pedidos y gestión del carrito se encuentra centralizada en la capa de servicios (`services.py`), mientras que las vistas (`views.py`) se encargan exclusivamente de recibir peticiones, validar datos y delegar la lógica correspondiente.

* OCP (Open/Closed Principle - Principio Abierto/Cerrado): El software debe estar abierto a la extensión, pero cerrado a la modificación.
    * Ejemplo: Para añadir un nuevo tipo de validador de identificación para otro país, simplemente se crea una nueva clase validadora y se integra en la factoría, sin modificar el código existente del formulario de checkout.

* LSP (Liskov Substitution Principle - Principio de Sustitución de Liskov): Las clases derivadas deben poder sustituir a sus clases base sin alterar la corrección del programa.
    * Ejemplo: Cualquier clase que herede de una interfaz o clase base de validador (`EstrategiaValidacion` en `validators.py`) puede ser utilizada por el formulario de checkout sin romper su lógica.


### Patrones de Diseño Aplicados

* MTV (Modelo-Template-Vista): Implementación estándar de Django para la separación de responsabilidades.

* Service Layer (Capa de Servicios): Centraliza la lógica de negocio compleja para mantener las vistas limpias y enfocadas en la interacción HTTP.
    * Ejemplo: `services.py` contiene funciones como `crear_pedido` que encapsulan la lógica de negocio para procesar una compra.

* Form Object: Utilización de formularios dedicados para la validación y procesamiento de datos específicos del usuario.
    * Ejemplo: `CheckoutForm` en `forms.py` maneja la validación de todos los datos necesarios para completar un pedido.

* Factory: Se utiliza para la creación de instancias de validadores de identificación de manera dinámica.
    * Ejemplo: La función `obtener_validador` en `validators.py` actúa como una factoría, devolviendo la instancia de validador adecuada según el país.

* Strategy: Permite definir una familia de algoritmos, encapsular cada uno como un objeto y hacerlos intercambiables.
    * Ejemplo: Las clases `ValidacionEcuador` y `ValidacionColombia` en `validators.py` implementan diferentes estrategias para la validación de identificaciones, que son seleccionadas dinámicamente.

* Template Method: Uso de herencia de plantillas base para mantener una estructura y diseño consistentes en todo el sitio.
    * Ejemplo: `checkout.html` y `catalogo.html` extienden `base.html` y redefinen bloques específicos para su contenido.

* Session Pattern: Gestión del carrito de compras y otros datos temporales directamente en la sesión del usuario para una experiencia persistente.

---

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto 10dencias en tu entorno local:

1.  **Clona el repositorio**:
    ```bash
    git clone https://github.com/mauricioolivo1902/10dencias-django
    cd 10dencias-django
    ```
2.  **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Realiza las migraciones de la base de datos**:
    ```bash
    python manage.py migrate
    ```
4.  **Crea un superusuario (opcional)**: Necesario si deseas acceder al panel de administración de Django.
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones en pantalla para crear tu usuario.
5.  **Ejecuta el servidor de desarrollo**:
    ```bash
    python manage.py runserver
    ```
6.  **Accede a la tienda**: Abre tu navegador y visita http://127.0.0.1:8000/catalogo.

### Frases Motivacionales de ZenQuotes

Para importar automáticamente frases motivacionales desde la API pública de ZenQuotes, ejecuta el siguiente comando:

```bash
python manage.py import_zenquotes


---
### Pruebas Funcionales

El proyecto incluye pruebas automatizadas para garantizar la estabilidad y calidad del sistema. Estas pruebas, definidas en store/tests.py, verifican el correcto funcionamiento de procesos críticos como la personalización y compra de productos, así como la gestión de frases motivacionales.

Para ejecutar las pruebas, navega a la raíz del proyecto en tu terminal y ejecuta:

```bash
python manage.py test store

---
### Créditos
Desarrollado por Mauricio Olivo para la materia de Ingeniería Web de Ingeniería de Software - UDLA.