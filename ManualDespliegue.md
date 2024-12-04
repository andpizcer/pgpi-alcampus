# Manual de Despliegue de Aplicación con Docker

## Requisitos Previos
1. **Instalar Docker**:  
   Asegúrate de que Docker está instalado en tu máquina. Puedes descargarlo desde [Docker Hub](https://www.docker.com/).

2. **Instalar Docker Compose** (opcional):  
   Si no está instalado, sigue la guía oficial para instalar [Docker Compose](https://docs.docker.com/compose/install/).

3. **Comprobar la Instalación**:  
   Verifica que Docker está funcionando ejecutando el siguiente comando en el terminal:  
   ```bash
   docker --version
   ```

---

## Pasos para el Despliegue

### 1. Abrir el Terminal
- En **Windows**: Usa *PowerShell* o *Command Prompt*.  
- En **Linux/MacOS**: Usa *Bash* o tu terminal favorito.

### 2. Cargar la Imagen de Docker
1. Navega al directorio donde se encuentra el archivo `pgpi-alcampus.tar`.
2. Ejecuta el siguiente comando para cargar la imagen de Docker:  
   ```bash
   docker load -i pgpi-alcampus.tar
   ```

   Este comando cargará la imagen en el entorno de Docker.

### 3. Verificar la Imagen
1. Lista las imágenes disponibles en Docker con el siguiente comando:  
   ```bash
   docker images
   ```
2. Busca una imagen con un nombre similar a **`pgpi-alcampus-web`**. Toma nota del nombre y el **TAG** (versión) de la imagen.

### 4. Ejecutar el Contenedor
1. Utiliza el siguiente comando para iniciar un contenedor desde la imagen:  
   ```bash
   docker run -p 8000:8000 pgpi-alcampus-web
   ```
   - `-p 8000:8000` mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina local.
   - `pgpi-alcampus-web` es el nombre de la imagen.

2. Si el nombre exacto difiere, reemplaza `pgpi-alcampus-web` con el nombre encontrado en el paso anterior.

### 5. Acceder a la Aplicación
1. Abre tu navegador web.
2. Ingresa la URL:  
   ```plaintext
   http://localhost:8000
   ```
3. Deberías ver la aplicación desplegada correctamente.

---

## Configuración de la Aplicación

### **Inicio de Sesión**
Una vez que la aplicación esté desplegada, puedes iniciar sesión utilizando las siguientes credenciales predeterminadas:  
- **Correo electrónico**: `client1@gmail.com`  
- **Contraseña**: `electrodomestico`

Asegúrate de cambiar estas credenciales si es necesario para entornos de producción.

---

## Realización de Pagos

Para realizar pagos en los pedidos dentro de la aplicación, es necesario usar una **cuenta de sandbox** o una **tarjeta de prueba**. Estas herramientas permiten simular transacciones sin utilizar información real, lo cual es ideal para entornos de desarrollo y pruebas.

### **Tarjeta de Prueba Recomendable**
Puedes usar la siguiente tarjeta de prueba para realizar los pagos en la aplicación:

- **Número de Tarjeta**: `4032033601520898`  
- **Fecha de Expiración**: `08/2028`  
- **CVC**: `007`

### **Pasos para Realizar un Pago**
1. Durante el proceso de compra, selecciona la opción de realizar un pago.
2. Ingresa los datos de la tarjeta proporcionados arriba.
3. Confirma el pago.  
   > **Nota**: No se realizará ninguna transacción real. Este proceso es únicamente para probar la funcionalidad de la aplicación.

---

## Opción Alternativa: Despliegue en Línea

Si no deseas realizar el despliegue localmente, la aplicación ya está disponible en línea en el siguiente enlace:  
[Aplicación Desplegada en Render](https://pgpi-alcampus.onrender.com)

Simplemente abre el enlace en tu navegador para acceder directamente a la aplicación.

---

## Solución de Problemas
1. **Comando `docker` no encontrado**:  
   Verifica que Docker está instalado y en tu variable de entorno `PATH`.

2. **El puerto 8000 ya está en uso**:  
   Cambia el puerto del host con el comando:  
   ```bash
   docker run -p 8080:8000 pgpi-alcampus-web
   ```  
   Luego accede a la URL: `http://localhost:8080`.

3. **La imagen no se encuentra después de cargarla**:  
   Asegúrate de usar el comando `docker images` para verificar los nombres y etiquetas de las imágenes cargadas.

4. **Fallo al acceder a `localhost:8000`**:  
   Asegúrate de que no haya firewalls bloqueando el puerto 8000.

---

Con este manual, deberías poder desplegar y ejecutar la aplicación correctamente en tu entorno local o acceder a la versión en línea ya desplegada. Además, puedes probar las funcionalidades de pagos utilizando la tarjeta de prueba proporcionada.