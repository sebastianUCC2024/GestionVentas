# 🚀 GestionVentas CRM

Sistema de Gestión de Ventas y Clientes desarrollado con Django 6.0

## 📋 Descripción

GestionVentas es un CRM (Customer Relationship Management) completo para la gestión de clientes, ventas y seguimientos comerciales. Desarrollado en equipo siguiendo metodología GitFlow y buenas prácticas de desarrollo colaborativo.

## 👥 Equipo de Desarrollo

- **Dev 1**: Autenticación y Usuarios
- **Dev 2**: Módulo de Clientes
- **Dev 3**: Módulo de Ventas
- **Dev 4**: Dashboard/UI y Despliegue

## 🛠️ Tecnologías

- **Backend**: Django 6.0.5
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript
- **Estilos**: Bootstrap 5, CSS personalizado
- **Formularios**: Django Crispy Forms + Bootstrap 5
- **Reportes**: ReportLab, Pandas
- **Deploy**: Gunicorn, WhiteNoise
- **Gestión de Variables**: Python Decouple

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/sebastianUCC2024/GestionVentas.git
cd GestionVentas
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto (usar `.env.example` como referencia):

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Aplicar migraciones

```bash
cd GestionVentas
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a: `http://localhost:8000`

## 📁 Estructura del Proyecto

```
GestionVentas/
├── GestionVentas/          # Configuración principal
│   ├── settings.py         # Configuración Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # WSGI para producción
├── users/                 # App de usuarios
├── clientes/              # App de clientes
├── ventas/                # App de ventas
├── templates/             # Templates globales
├── static/                # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── media/                 # Archivos subidos
├── venv/                  # Entorno virtual (no en git)
├── requirements.txt       # Dependencias
├── .env                   # Variables de entorno (no en git)
├── .env.example          # Ejemplo de variables
└── manage.py             # CLI de Django
```

## 🌿 GitFlow - Ramas

- `main`: Rama principal (producción)
- `dev`: Rama de desarrollo
- `feature/auth-usuarios`: Autenticación
- `feature/client`: Clientes
- `feature/ventas`: Ventas
- `dashboard-ui`: Dashboard y UI

## 🔄 Flujo de Trabajo

### Para desarrolladores

1. **Actualizar rama dev**
```bash
git checkout dev
git pull origin dev
```

2. **Crear/actualizar tu rama de feature**
```bash
git checkout -b feature/nombre-feature
# o si ya existe
git checkout feature/nombre-feature
git pull origin dev --rebase
```

3. **Hacer cambios y commit**
```bash
git add .
git commit -m "feat(modulo): descripción del cambio"
```

4. **Subir cambios**
```bash
git push origin feature/nombre-feature
```

5. **Crear Pull Request** hacia `dev` en GitHub

## 📝 Convenciones de Commits

- `feat(modulo):` Nueva funcionalidad
- `fix(modulo):` Corrección de bug
- `docs:` Documentación
- `style:` Formato, estilos
- `refactor:` Refactorización de código
- `test:` Tests
- `chore:` Tareas de mantenimiento

## 🚀 Despliegue

### Preparar para producción

1. **Configurar variables de entorno**
```env
DEBUG=False
SECRET_KEY=clave-segura-aleatoria
ALLOWED_HOSTS=tu-dominio.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nombre_db
DB_USER=usuario
DB_PASSWORD=password
DB_HOST=host
DB_PORT=5432
```

2. **Recolectar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

3. **Aplicar migraciones**
```bash
python manage.py migrate
```

4. **Ejecutar con Gunicorn**
```bash
gunicorn GestionVentas.wsgi:application --bind 0.0.0.0:8000
```

### Plataformas recomendadas

- **Render**: Fácil despliegue con PostgreSQL incluido
- **Railway**: Deploy automático desde GitHub
- **Heroku**: Clásico para Django
- **PythonAnywhere**: Opción gratuita

## 🔐 Seguridad

- ✅ SECRET_KEY en variables de entorno
- ✅ DEBUG=False en producción
- ✅ ALLOWED_HOSTS configurado
- ✅ CSRF protection habilitado
- ✅ SQL injection protection (ORM)
- ✅ XSS protection
- ✅ Archivos sensibles en .gitignore

## 📊 Funcionalidades

### Módulo de Usuarios
- Registro y autenticación
- Roles de usuario
- Perfiles personalizados

### Módulo de Clientes
- CRUD completo de clientes
- Búsqueda y filtros
- Historial de interacciones

### Módulo de Ventas
- Gestión de ventas
- Seguimiento de oportunidades
- Estados de venta
- Dashboard con métricas

### Dashboard/UI
- KPIs visuales
- Gráficos interactivos
- Diseño responsive
- Experiencia de usuario optimizada

## 🧪 Testing

```bash
python manage.py test
```

## 📄 Licencia

Este proyecto es parte de un trabajo académico de la Universidad Cooperativa de Colombia.

## 👨‍💻 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

Universidad Cooperativa de Colombia - 2024

---

## GIT GRAPH
### PRIMERA PARTE DEL GRAPH 
<img width="926" height="554" alt="PRIMERA PARTE DEL GRAPH" src="https://github.com/user-attachments/assets/3191feca-58e4-4f3b-b81e-6c846dcd9322" />
### SEGUNDA PARTE DEL GRAPH
<img width="925" height="560" alt="SEGUNDA PARTE DEL GRAPH" src="https://github.com/user-attachments/assets/bb149e6c-72bb-4d0e-aed5-ec5db05b42f6" />
### TERCERA PARTE DEL GRAPH 
<img width="937" height="542" alt="TERCERA PARTE DEL GRAPH" src="https://github.com/user-attachments/assets/3f3e2b98-4101-444b-bdd9-dfbdfd1aadfa" />




⭐ **Desarrollado con Django y ❤️ por el equipo de GestionVentas**
