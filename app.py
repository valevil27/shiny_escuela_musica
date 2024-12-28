from datetime import date

# Import data from shared.py
from plot_utils import mean_fig
from shared import data, filter_options, last_entry_ds, select_choices, courses_df
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import locale

# Idioma local castellano para trabajar con strftime y fechas, _ para no renderizar
_ = locale.setlocale(locale.LC_TIME, "")
actual_trim, actual_course = last_entry_ds(date.today())


# Barra de título
@render.express
def render_title():
    with ui.layout_columns(class_="mt-1 mb-0", col_widths=[8, 4]):
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
            class_="align-right",
        )


# Filtros del Dashboard
with ui.sidebar():
    ui.h4("Filtros")

    @render.ui
    def select_course_start():
        return ui.input_select(
            "course_start",
            "Curso de Inicio",
            choices=courses_df(),
            selected=actual_course,
        )

    ui.input_select(
        "trim_start", "Trimestre de Inicio", choices=[1, 2, 3], selected=actual_trim
    )
    ui.input_select(
        "filter", "Aspecto a Comparar", choices=filter_options, selected="General"
    )

    @render.ui
    def input_sel_filter():
        return ui.input_select(
            "objective",
            "Base de la Comparativa",
            choices=select_choices(data(), input.filter()),
        )

    @render.ui
    def error_msg():
        if input.course_start() == actual_course and actual_trim < int(
            input.trim_start()
        ):
            return ui.p(
                "El trimestre de inicio debe ser anterior o igual al actual.",
                class_="text-red",
            )


# Fila de bars
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Tasa de aprobados")

        @render_plotly
        def aproved_plotly():
            fig = mean_fig(data(), "Aprobado", "Porcentaje de Aprobado")
            fig.add_hline(y=0.8, line_dash="dash")
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Horas de práctica semanales")
        @render_plotly()
        def horas_practica_plotly():
            fig = mean_fig(data(), "Horas_Practica", "Horas de Práctica Semanales")
            fig.add_hline(y=4, line_dash="dash")
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Promedio de asistencia")
        @render_plotly()
        def asistencia_plotly():
            fig = mean_fig(data(), "Promedio_Asistencia", "Porcentaje de Asistencia")
            fig.add_hline(y=0.8, line_dash="dash")
            return fig

with ui.layout_columns():
    with ui.card():
        ui.card_header("Acceden a la Banda en 3 años")

    with ui.card():
        ui.card_header("Avanzan a estudios superiores")

    with ui.card():
        ui.card_header("Abandonan la escuela")

with ui.layout_columns(col_widths=[8, 4]):
    with ui.card():
        ui.card_header("Comparativa")

    with ui.card():
        ui.card_header("Índice de Satisfacción")
