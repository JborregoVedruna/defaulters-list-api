# Defaulters List API

Este proyecto es una API REST para la gestión de listas de morosos (defaulters), construida siguiendo principios de arquitectura limpia y patrones de diseño modernos para asegurar escalabilidad y mantenibilidad.

## ✨ Características Principales

- 🏗️ **Arquitectura Hexagonal**: Separación clara entre la lógica de dominio y los detalles de infraestructura (Puertos y Adaptadores).
- 🧩 **Patrón Mediator & CQRS**: Desacoplamiento de comandos y consultas para una orquestación limpia de los casos de uso.
- 📂 **Persistencia NoSQL**: Integración con **MongoDB** para una gestión flexible y escalable de los datos de morosidad.
- ⚡ **Desarrollo Ágil**: Implementado con **Flask**, un micro-framework de Python potente y ligero.
- 🛡️ **Seguridad y Calidad**: Análisis proactivo de vulnerabilidades en infraestructura mediante **KICS (Checkmarx)**.
- 🐳 **Contenerización Completa**: Configuración lista para entornos aislados mediante Docker y Docker Compose.
- 📖 **Documentación de Pruebas**: Archivo de peticiones HTTP incluido para validación rápida de endpoints.

---

## 🚀 Instrucciones para Ejecutar el Proyecto

### Requisitos Previos

- **Python 3.10** o superior.
- **Docker** y **Docker Compose** (recomendado).

### Ejecución Local

1.  **Clonar el repositorio** y situarse en la raíz del proyecto.
2.  **Configurar entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar variables de entorno**:
    Asegúrate de tener un archivo `.env` configurado (puedes basarte en el ejemplo):
    ```env
    MONGO_URI=mongodb://localhost:27017/
    MONGO_DB_NAME=caixabank_debts
    PORT=5000
    ```
5.  **Ejecutar la aplicación**:
    ```bash
    python src/app.py
    ```

### 🐳 Ejecución con Infraestructura Completa (Docker Compose)

Puedes levantar la API junto con su base de datos MongoDB y una interfaz de administración (Mongo Express) con un solo comando:

1.  **Ejecutar Docker Compose**:
    ```bash
    docker-compose up --build
    ```

#### 🛠️ Servicios Incluidos:

- **API REST**: [http://localhost:5000](http://localhost:5000) (Puerto configurable).
- **Base de Datos**: MongoDB (Puerto 27017).
- **Consola de Administración (Mongo Express)**: [http://localhost:8081](http://localhost:8081)
  - Usuario: `admin` | Password: `pass`
- **Análisis de Seguridad (KICS)**: Ejecución automática del escaneo con reporte generado en `kics-report.html`.

---

## 🏗️ Arquitectura y Decisiones Técnicas

El proyecto ha sido diseñado bajo una estructura **Ports & Adapters (Hexagonal Architecture)** para separar las preocupaciones:

### 1. Capas del Sistema

- **Domain**: Contiene los modelos de negocio (`Debt`) y los contratos (Interfaces) para la persistencia. Es el núcleo puro de la aplicación.
- **Application**: Implementa los casos de uso específicos (`SaveDebt`, `GetDebts`). Utiliza el patrón **Mediator** para gestionar la comunicación entre los controladores y los manejadores de comandos/consultas.
- **Infrastructure**: Implementa los adaptadores técnicos.
  - **Inbound**: Controladores REST de Flask que exponen los endpoints.
  - **Outbound**: Adaptador para **MongoDB** utilizando `pymongo`.

### 2. Patrón Mediator

Se utiliza un mediador para desacoplar los controladores de los casos de uso. El controlador solo sabe enviar una petición (`Command` o `Query`), y el mediador se encarga de localizar el `Handler` correspondiente para ejecutar la lógica de negocio.

### 3. Persistencia con MongoDB

Se ha elegido MongoDB por su flexibilidad en el esquema de datos, lo que permite evolucionar rápidamente los registros de deuda sin las restricciones de una base de datos relacional tradicional.

### 4. Seguridad con KICS

Integrado en la infraestructura de Docker para detectar automáticamente configuraciones inseguras en Dockerfiles o archivos de Docker Compose, asegurando que el despliegue cumpla con estándares mínimos de seguridad.

---

## 🧪 Pruebas de la API

Tienes ejemplos de peticiones listos para usar en el archivo [requests.http](./requests.http). Puedes ejecutarlas directamente desde VS Code si tienes instalada la extensión "REST Client".

### Endpoints Principales:

- `POST /api/v1/debts/`: Registrar una nueva deuda.
- `GET /api/v1/debts/`: Listar todas las deudas registradas.
- `GET /api/v1/debts/dni/<dni>`: Buscar deudas por el DNI del deudor.

---

## 📈 Mejoras y Extensiones Futuras

- **Autenticación JWT**: Implementar seguridad avanzada con tokens para proteger los endpoints.
- **Caché con Redis**: Optimizar las consultas frecuentes mediante una capa de caché persistente.
- **Observabilidad (Grafana/Loki)**: Integrar monitoreo profesional para trazabilidad de logs y métricas de rendimiento.
- **Validación Avanzada**: Uso de `pydantic` para una validación más estricta de los datos de entrada en los DTOs.
- **Pruebas Automatizadas**: Implementación de tests unitarios y de integración con `pytest` para garantizar una cobertura mínima del 80%.
