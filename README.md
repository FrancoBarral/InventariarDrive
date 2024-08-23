# Inventariar Drive
El funcionamiento de la app es inventariar todos los archivos pertenencientes a la unidad de nuestro drive. En el caso de que encuentre algun archivo que su privacidad sea publica, se la modificara a privado, enviandole un mail al dueño de ese archivo.
A su vez, se guarda los datos de un historico de los cambios que fueron ejecutados, con la ultima fecha de modificación.
***
## Instalacion
1. Tener instalado Python 3.9 o superior
2. Crear entorno virtual:
``` $ python -m venv env ```
3. Clonar repositorio
``` $ git clone https://github.com/FrancoBarral/InventariarDrive.git ```
4. Crear archivo .env donde indicaremos las credenciales (enviadas por Mail)
5. Instalar los requirements:
``` $ pip install -r requirements.txt ```
6. Ejecutar aplicacion en consola:
``` $ python app.py ```
