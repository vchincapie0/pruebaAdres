Proyecto de Validación de Archivos en Django:

Proyecto almacenado en carpeta pruebaAdres

1. Instalación de dependencias:
    pip install -r requirements.txt
2. Configuración de Django
    Asegúrate de que settings.py tiene configurado STATICFILES_DIRS:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
3. Migraciones de BD:
    python manage.py migrate
4. Ejecutar Servidor
    python manage.py runserver


Requisitos para ejecutar el script de extracción de CUFE

Script almacenado en carpeta pruebaAdres2

1. Instalación de dependencias:
    pip install -r requirements.txt
2. Estructura del proyecto:
    📂 ADRES/
    |---📂 pruebaAdres
    |---📂 pruebaAdres2/
    |   |---📂 facturas/ # Carpeta de los PDF
    |   |---extraer_cufe.py # Código de extracción
    |   |---ver_datos.py  # Código para validar informacion en BD
    |   |---facturas.db # BD
    |---readme.md 
    |---requirements.txt # Dependencias

3. Ejecutar Script
    Ubicandose en la carpeta pruebaAdres2, ejecutar script: 
    python extraer_cufe.py
    Esto extraerá:
       - Nombre del archivo
       - Número de páginas
       - CUFE (si está presente)
       - Peso del archivo en KB

4. Verificar los datos almacenados
    Para consultar los datos extraídos, usar comando:
    python ver_datos.py




