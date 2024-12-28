from datetime import date
import seaborn as sns

# Import data from shared.py
from shared import df, filter_options, last_entry_ds
from shiny.express import input, render, ui
import locale

# Idioma local castellano para trabajar con strftime y fechas, _ para no renderizar
_ = locale.setlocale(locale.LC_TIME, "")
actual_trim, actual_course = last_entry_ds(date.today())


# Barra de título
@render.express
def render_title():
    with ui.layout_columns(class_="mt-3 "):
        ui.h2(f"Escuela de Música - {input.filter()}")
        ui.div(
            ui.p(
                "Fecha de consulta: " + date.today().strftime("%d de %B de %Y"),
                class_="mb-0",
                style="font-size: small;",
            ),
            ui.p(
                f"Trimestre {actual_trim}, Curso {actual_course}",
                style="font-size: small;",
            ),
        )


# Filtros del Dashboard
with ui.sidebar():
    ui.h4("Filtros")
    ui.input_date("fecha_inicio", "Fecha de inicio", language="es", format="mm-yyyy")
    ui.input_selectize(
        "filter", "Aspecto a Examinar", choices=filter_options, selected="General"
    )

# Fila de bars
with ui.layout_columns():
    with ui.card():
        ui.card_header("Tasa de aprobados")

    with ui.card():
        ui.card_header("Horas de práctica semanales")

    with ui.card():
        ui.card_header("Promedio de asistencia")
