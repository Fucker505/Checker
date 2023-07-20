# Verificador HTTP con Solicitudes Asincrónicas

Este es un código en Python que implementa la clase `Checker` con soporte para realizar solicitudes HTTP de forma asincrónica utilizando la biblioteca `aiohttp`. Esta clase te permite ejecutar solicitudes HTTP (GET, POST, PUT, DELETE, OPTIONS y PATCH) y extraer subcadenas de las respuestas recibidas. También contiene una función para generar direcciones de correo electrónico aleatorias.

## Requisitos

- Python 3.x
- aiohttp

## Uso

1. Importa la clase `Checker` y las enumeraciones `RequestMethods` necesarias para especificar el método de solicitud.
2. Crea una instancia de `Checker` proporcionando los detalles de la tarjeta de crédito (número de tarjeta, mes de vencimiento, año de vencimiento y CVV) como cadenas.
3. Utiliza el método `exec_request` para realizar solicitudes HTTP de forma asincrónica.
4. Utiliza el método `get_str` para extraer una subcadena entre dos cadenas dadas.
5. Utiliza el método `get_random_email` para generar una dirección de correo electrónico aleatoria.
6. Opcionalmente, puedes usar la función `create_headers_easy` para crear un diccionario de encabezados a partir de una cadena formateada.
7. Opcionalmente, puedes utilizar la función `massRequests` para realizar múltiples solicitudes asincrónicas de forma simultánea.

Recuerda que este código utiliza `aiohttp`, por lo que es importante gestionar adecuadamente las sesiones y cerrarlas después de su uso. Además, ten en cuenta que el código se encuentra en un estado funcional pero puede mejorarse y ampliarse según las necesidades específicas de tu proyecto.
