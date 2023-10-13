# Bienvenidos a prompt sentiment

Esta es una aplicación desarrollada como TFG del grado de ingeniería informática de la Universidad de Burgos que realiza un análisis de sentimientos en comentarios de usuarios.

Después analiza el sentimiento que hay en ellos, los puntúa como positivo o negativo.

Se muestran los resultado mediante ayudas visuales para que se más interactivo y enriquecer la experiencia de usuario.

## Instalación en local
Para poder utilizar la aplicación en local, es necesario instalarse los siguientes componentes: 
* **Python**: Versión 3.8
* **Base de datos**: Sqlite
* **Visual C++ Tools**: A partir de la versión del 2015
* **Librerías de Python**:  
    * **flask**: Versión 1.1.1  
    * **flask-cors**  
    

Todas las librerías de Python necesarias pueden instalarse de la misma forma:
```
$ pip install -r requirements.txt
```

Cuando se hayan completado todos los requisitos anteriores, deberemos introducir las claves que nos han dado en variables de entorno. De esta forma se podrán conectar con nuestro código. 

Para saber exactamente como deben llamarse cada variable hay que acceder a los diferentes archivos .py y ver el nombre, se encuentra en mayúsculas.

Para la parte de la interfaz de usuario, deberemos instalar todos los módulos que utiliza el proyecto.

### Para ejecutar
Tras realizar la instalación, deberemos abrir dos consolas y posicionarlas en el directorio de nuestro proyecto.

flask --app flask_app.py run

Esto levantará la interfaz de usuario en http://localhost:5000/.

Solo deberemos introducir en nuestro buscador la última url, ya que es desde donde interactuaremos con la aplicación.

## Aplicación desplegada
La aplicación ha sido desplegada en www.heroku.com, un sitio web que nos permite alojar nuestra aplicación de forma gratuita. 

## Uso de la aplicación
Para realizar un buen uso de la aplicación, el proyecto consta de una wiki del manual de usuario donde se explican todas las implementaciones de la aplicación.

Puede encontrarse en este link: https://tgs1003.gitbook.io/prompt_sentiment/.


