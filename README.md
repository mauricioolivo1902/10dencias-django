# 10dencias - Plataforma E-commerce de Productos Personalizables

Proyecto full-stack desarrollado con Django que simula una tienda en línea para la venta de productos personalizables con frases motivacionales. La plataforma cubre desde la visualización del catálogo hasta un flujo de compra completo con validaciones y gestión de pedidos.

## Link deploy
http://estebanudla.pythonanywhere.com/catalogo/

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [🚀 Características Implementadas](#-características-implementadas)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [⚙️ Instalación y Puesta en Marcha Local](#️-instalación-y-puesta-en-marcha-local)
- [🏛️ Arquitectura y Patrones de Diseño](#️-arquitectura-y-patrones-de-diseño)
- [部署 Despliegue](#-despliegue)
- [✉️ Contacto](#️-contacto)

---

## 📖 Acerca del Proyecto

**10dencias** (un juego de palabras con "tendencias") es una aplicación web que permite a los usuarios explorar un catálogo de productos (tazas, camisetas, hoodies, etc.) y personalizarlos eligiendo entre una selección de frases motivacionales. El proyecto cuenta con un panel de administración para gestionar los productos y las frases, y un flujo de compra completo que incluye un carrito de compras persistente, validación de datos y un sistema de pedidos.

---

## 🚀 Características Implementadas

### Frontend
- **Diseño Responsivo:** Interfaz adaptable a dispositivos móviles y de escritorio.
- **Maquetación con CSS Grid y Flexbox:** Uso obligatorio de estas tecnologías para un layout moderno y flexible.
- **Catálogo de Productos:** Vista de cuadrícula para todos los productos disponibles.
- **Página de Detalle:** Vista individual para cada producto con opciones de personalización.
- **Carrito de Compras Dinámico:** Añade múltiples productos al carrito, con un contador en tiempo real en el encabezado.
- **Página de Gestión del Carrito:** Permite ver, revisar y eliminar productos del carrito.

### Backend
- **Gestión de Modelos Django:** Base de datos relacional para Productos, Frases, Pedidos, Países, etc.
- **Panel de Administración Completo:** CRUD (Crear, Leer, Actualizar, Borrar) para todos los modelos importantes, exclusivo para administradores.
- **Sistema de Carrito con Sesiones:** El carrito de compras persiste entre diferentes páginas utilizando el framework de sesiones de Django.
- **Formulario de Compra con Validación:**
    - Validación personalizada en el backend (ej: número de identificación de 10 dígitos).
    - Desplegables dinámicos (País -> Provincia -> Ciudad) implementados con **JavaScript y AJAX** que consultan endpoints de API sin recargar la página.
- **Flujo de Pedidos Completo:** Creación de registros de Pedido, DetallePedido y DatosFacturación en la base de datos tras una compra exitosa.
- **Página de Confirmación de Pedido:** Feedback visual para el usuario después de completar una compra.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3 (Flexbox, CSS Grid), JavaScript (Vanilla JS, Fetch API, AJAX)
- **Base de Datos:** SQLite (para desarrollo y despliegue simple)
- **Control de Versiones:** Git, GitHub
- **Despliegue:** PythonAnywhere

---

## ⚙️ Instalación y Puesta en Marcha Local

Para ejecutar este proyecto en tu propia máquina, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/10dencias-django.git](https://github.com/tu-usuario/10dencias-django.git)
    cd 10dencias-django
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate

    # En MacOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno:**
    - Crea un archivo llamado `.env` en la raíz del proyecto.
    - Añade las siguientes líneas, reemplazando el valor con tu propia clave secreta:
      ```
      SECRET_KEY=tu-clave-secreta-aqui
      DEBUG=True
      ```

5.  **Ejecutar las migraciones:**
    Este comando creará la base de datos y la poblará con datos iniciales.
    ```bash
    python manage.py migrate
    ```

6.  **Crear un superusuario** para acceder al panel de administración:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    El sitio estará disponible en `http://127.0.0.1:8000/`.

---

## 🏛️ Arquitectura y Patrones de Diseño

Este proyecto fue desarrollado siguiendo principios de diseño de software para asegurar un código limpio, mantenible y escalable.

- **Principio de Responsabilidad Única (SRP):**
  - **Vistas:** Se encargan únicamente de manejar la lógica de peticiones y respuestas HTTP.
  - **Modelos:** Definen exclusivamente la estructura y relaciones de los datos.
  - **Formularios:** Encapsulan la lógica de validación de los datos de entrada.
  - **Servicios:** La lógica de negocio compleja (como la creación de un pedido con múltiples objetos) se extrajo a una **Capa de Servicios** (`services.py`), manteniendo las vistas "delgadas".

- **Desacoplamiento con AJAX:** La lógica para los desplegables dinámicos se implementó creando endpoints de API en el backend que devuelven JSON, manteniendo el frontend y el backend desacoplados.

- **Refactorización Futura (Planificada):** Como próximo paso, la validación del número de identificación será refactorizada para usar el **Patrón Factory** y el **Principio de Inversión de Dependencias (DIP)**, permitiendo añadir fácilmente validadores para diferentes países sin modificar el código del formulario.

---

## Despliegue

La aplicación está desplegada en **PythonAnywhere** y se sirve a través de un servidor Gunicorn con Nginx para los archivos estáticos. El proceso de despliegue incluyó la configuración de variables de entorno, la base de datos, los archivos estáticos (`collectstatic`), y el archivo de configuración WSGI.

---

## ✉️ Contacto

**Esteban Mauricio Olivo Benavides**

mauricioolivo1902@gmail.com
esteban.olivo@udla.edu.ec
