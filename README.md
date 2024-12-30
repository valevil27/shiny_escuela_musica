# Dashboard para Escuela de Música

Este proyecto es un dashboard interactivo desarrollado con Shiny Express para Python. Su objetivo es detallar el rendimiento de una escuela de música en comparación con sus objetivos establecidos. El dashboard permite visualizar y analizar diversos indicadores clave de rendimiento (KPIs) de la escuela, proporcionando una herramienta útil para la toma de decisiones.

Este trabajo ha sido realizado en el contexto de la asignatura de Inteligencia de Negocio para el Máster en Big Data de la Universidad de Murcia.

## Estructura del Proyecto

La estructura del proyecto es la siguiente:

- `app.py`: Contiene la aplicación base desarrollada con Shiny Express para Python. Este archivo es el punto de entrada principal del dashboard.
- `data_gen_v2.py`: Incluye el script para la generación de datos utilizados en el dashboard. Este script se encarga de crear y preprocesar los datos necesarios para las visualizaciones.
- `plot_utils.py`: Contiene las funciones para generar las gráficas utilizando Plotly. Estas funciones son utilizadas dentro de la aplicación Shiny para crear visualizaciones interactivas.
- `shared.py`: Incluye un conjunto de funciones compartidas que son utilizadas por el resto de los archivos del proyecto. Estas funciones proporcionan utilidades comunes que facilitan la implementación del dashboard.

Cada uno de estos archivos juega un papel crucial en el funcionamiento del dashboard, asegurando que los datos se generen, procesen y visualicen correctamente.

## Instalación de dependencias

Para instalar las dependencias del proyecto, asegúrate de tener instalado el gestor de librerías `uv`. Luego, ejecuta el siguiente comando en la terminal desde el directorio del proyecto:

```sh
uv install
```

Este comando leerá los archivos `pyproject.toml` y `uv.lock` para instalar todas las dependencias necesarias.
