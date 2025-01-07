# BACKEND_PERMISOS_SEDH


Permisos Personales es un sistema monolitico para el area de Recursos Humanos de la Secretaria de Derechos Humanos en Honduras. dicho sistema se encarga de gestionar los permisos personales, oficiales, vacaciones de todos los empleados.

el proyecto utiliza la conexion a la BD mediante sqlServer para su conexión estara mas abajo en la sección de instrucciones.

## Tabla de contenido:
* [Descargas](#descargas)
* [instrucciones](#instrucciones)
* [importante](#importante)
* [Desarrolladores](#desarrolladores)
* [Colaboradores](#colaboradores)


## Descargas  
- [GitHub Desktop](https://desktop.github.com/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Python v3.13.0](https://www.python.org/downloads/release/python-3130/)
- [Git 2.47.1 ](https://git-scm.com/downloads/win)(Al instalar permita todos los permisos para que tenga una consola de git en Visual Studio Code)

## Instrucciones
para ejecutar este proyecto 
1. descargue el proyecto en Git hub desktop o descarguelo como zip.
2. abralo con un editor de texto como visual Studio Code.
3. abra una terminal en VSC, **escoga consola de Git Bash** y coloque el siguiente comando, eso creara un entorno virtual de python y las dependencias quedaran solo en el proyecto y no en su PC como recomienda python.

```bash
 python -m venv venv
```
despues: 
```bash
source venv/Scripts/activate
```

4. descargue las dependencias del poyecto, notará que ``el framework que se usa en este proyecto es FastApi`` para futuras modificaciones del sistema, en la terminal de VSC ejecute:
```bash
pip install -r requirements.txt
```

5. este proyecto tiene metodos de seguridad como varibles de entorno, cree un archivo en la carpeta raiz del proyecto como: `.env` en ella necesitará colocar las credenciales de conexion de BD, servidor y token.
necesitará las variables para la conexion: 

`Configuración del servidor:
HOST
PORT`

`Configuración de la base de datos:
DB_SERVER,
DB_NAME,
DB_USER,
DB_PASSWORD`

`para el token de autenticacion:
SECRET_KEY,
ALGORITHM,
ACCESS_TOKEN_EXPIRE_MINUTES`

6. iniciar el proyecto, ejecutar en la terminal de VSC, cambie el Host por su ip de PC o host de la varibale de entorno que coloco en el paso anterior.
```bash
uvicorn app.main:app --host X.X.X.X --port 80
```

## Importante
* *este proyecto usa python v3.13.0 con el framework FastApi.*
* *este proyecto usa variables de entorno obligatorias para ejecutar el proyecto.*

## Desarrolladores
- **[@CarLuis07](https://github.com/CarLuis07/)  - Luis Cardona - `kikecar97@gmail.com`**

### Colaboradores


- Emerson Duron  - `emerson.duron@sedh.gob.hn`
