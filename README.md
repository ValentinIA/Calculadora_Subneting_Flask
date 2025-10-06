# 🧮 Calculadora de Subneting - Flask

Aplicación web desarrollada con **Flask (Python)** que permite calcular subredes a partir de una dirección IP y una máscara de red.  
El proyecto incluye autenticación (login y registro) mediante **MongoDB**, aunque no esta configurado y se ejecuta sin base de datos.


## 🚀 Características

- Cálculo de subredes mediante función `subneting(ip, mascara)` definida en `Subneting.py`.
- Estructura modular con Flask y rutas separadas (login, registro, calculadora, logout).
- Uso de `passlib` para cifrado de contraseñas.
- Conexión a base de datos **MongoDB**.
- Diseño preparado para integrarse con plantillas HTML personalizadas.

## ⚙️ Instalación

1. **Clonar el repositorio**

2. **Instalar dependencias:**
  pip install -r requirements.txt

3. **Configurar variables de entorno (si usas MongoDB)**
  Crea un archivo .env con:
  MONGODB_URI="tu_conexion_mongodb"

4. **Ejecutar la aplicación:**
   python main.py
