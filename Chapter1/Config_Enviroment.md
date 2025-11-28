# Configuración del Entorno de Desarrollo

## Sistema Operativo

El primer paso es configurar tu entorno de desarrollo para que puedas comenzar a trabajar en tu proyecto. A continuación, se detallan los pasos necesarios para configurar tu entorno:

### Instalación de un Virtualizador

Instala un virtualizador, como **VirtualBox** o **VMware**, para crear máquinas virtuales que simulen diferentes sistemas operativos. En este caso, usaremos **Boxes** con la distribución de **Kali Linux**, tal como recomienda el libro.

### Instalación de Paquetes en Kali Linux

Al instalar Kali Linux, asegúrate de instalar los siguientes paquetes:

```bash
sudo apt-get install python-setuptools python-pip

pip install github3
```

### Instalación de WINGIDE en Kali Linux

El libro recomienda utilizar **WINGIDE** como entorno de desarrollo. Para instalarlo, sigue los pasos a continuación:

1. **Agregar el repositorio de WINGIDE (si es necesario)**.
2. **Descargar el instalador desde el sitio oficial**:

    ```bash
    wget https://wingware.com/pub/wingide/wing-personal-linux-x86-64.tar.gz
    ```

3. **Extraer el archivo descargado**:

    ```bash
    tar -xvzf wing-personal-linux-x86-64.tar.gz
    ```

4. **Navegar al directorio extraído e instalar**:

    ```bash
    cd wing-personal-linux-x86-64
    sudo ./install.sh
    ```

### Uso de Otro IDE

Si prefieres usar otro IDE, asegúrate de instalarlo y configurarlo según las instrucciones oficiales de su documentación.

---

## Verificación del Entorno

Una vez que hayas instalado **WINGIDE** o tu IDE preferido, ábrelo y configura un nuevo proyecto para comenzar a trabajar en tu código.

### Programa de Verificación

Escribe un programa simple en Python para verificar que todo esté funcionando correctamente:

```python
def sum_numbers(a, b):
     a = convert_to_int(a)
     b = convert_to_int(b)
     result = a + b
     return result

def convert_to_string(n):
     converted_int = int(n)
     return str(converted_int)

answer = sum_numbers("5", "10")
print("The sum is: " + convert_to_string(answer))
```

¡Con esto, tu entorno de desarrollo estará listo para comenzar!
