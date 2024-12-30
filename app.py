import locale
from datetime import date

import pandas as pd
from shiny.express import input, render, ui
from shinywidgets import render_plotly

from plot_utils import (
    avance_fig,
    comparativa_fig,
    figure_text,
    mean_fig,
    satisfaccion_fig,
)
from shared import (
    tipo_col,
    course_to_date,
    courses_df,
    data,
    filter_options,
    filter_data,
    get_objectives,
    type_options,
    last_entry_ds,
    select_choices,
    logger,
)

# Idioma local castellano para trabajar con strftime y fechas, _ para no renderizar
_ = locale.setlocale(locale.LC_TIME, "")
actual_trim, actual_course = last_entry_ds(date.today())

ui.page_opts(window_title="Rendimiento Escuela", fillable=True)


# Barra de título
@render.express
def render_title():
    with ui.layout_columns(class_="mt-1 mb-0", col_widths=[8, 4]):
        title = f"Escuela de Música - {input.category()}"
        sel = input.selected()
        if sel != "General":
            title = f"{title}: {input.selected()}"
        ui.h2(title)
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

    # Curso inicio de la comparativa. Por defecto es el último
    @render.ui
    def select_course_start():
        return ui.input_select(
            "course_start",
            "Curso de Inicio",
            choices=courses_df(),
            selected=actual_course,
        )

    # Trimestre inicio de la comparativa. Por defecto es el último
    ui.input_select(
        "trim_start",
        "Trimestre de Inicio",
        choices=["1", "2", "3"],
        selected=str(actual_trim),
    )
    # Categoría a comparar
    ui.input_select("category", "Categoría", choices=filter_options, selected="General")

    @render.ui
    def input_sel_filter():
        return ui.input_select(
            "selected",
            "Seleccionar",
            choices=select_choices(data(), input.category()),
        )

    ui.input_select(
        "tipo",
        "Tipo de Comparación",
        choices=type_options,
        selected="Tasa de aprobados",
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

    ui.input_checkbox("normalize", "Diferencia con Objetivo")


# Fila 1
with ui.layout_columns(height=300):
    with ui.card(full_screen=True):
        ui.card_header("Tasa de aprobados")

        @render_plotly
        def aproved_plotly():
            objective = get_objectives()
            if objective is None:
                return figure_text("Cargando...")
            objective = objective["Aprobado"]
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            logger.debug(df)
            fig = mean_fig(
                df,
                objective,
                "Aprobado",
                "Promedio de Aprobado",
                normalize=input.normalize(),
            )
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Horas de práctica semanales")

        @render_plotly()
        def horas_practica_plotly():
            objective = get_objectives()
            if objective is None:
                return figure_text("Cargando...")
            objective = objective["Horas_Practica"]
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            fig = mean_fig(
                df,
                objective,
                "Horas_Practica",
                "Horas de Práctica Semanales",
                normalize=input.normalize(),
            )
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Promedio de asistencia")

        @render_plotly()
        def asistencia_plotly():
            objective = get_objectives()
            if objective is None:
                return figure_text("Cargando...")
            objective = objective["Promedio_Asistencia"]
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            fig = mean_fig(
                df,
                objective,
                "Promedio_Asistencia",
                "Promedio de Asistencia",
                normalize=input.normalize(),
            )
            return fig


# Fila 2
with ui.layout_columns(height=300):
    with ui.card(full_screen=True):
        ui.card_header("Acceden a la Banda en 3 años")

        @render_plotly
        def acceso_banda_plotly():
            df = data()
            df = df[df["Años_Inscrito"] == 3]
            objective = get_objectives()
            if objective is None:
                return figure_text("Cargando...")
            objective = objective["Banda"]
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            fig = mean_fig(
                df,
                objective,
                "Banda",
                "Proporción que Accede a Banda",
                normalize=input.normalize(),
            )
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Abandonan la escuela")

        @render_plotly
        def abandono_plotly():
            objective = get_objectives()
            if objective is None:
                return figure_text("Cargando...")
            objective = objective["Abandono_Educacion"]
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            fig = mean_fig(
                df,
                objective,
                "Abandono_Educacion",
                "Proporción de Alumnos Totales",
                normalize=input.normalize(),
            )
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Avanzan a estudios profesionales")

        @render_plotly
        def avance_estudios_plotly():
            df: pd.DataFrame | None = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            df = df[df["Curso"] == "Cuarto"]  # type: ignore
            objective = get_objectives()
            if objective is None or df is None:
                return figure_text("Cargando...")
            objective = objective["Avance_Grado_Profesional"]
            fig = avance_fig(
                df,
                objective,
                normalize=input.normalize(),
            )
            return fig


# Fila 2
with ui.layout_columns(col_widths=[8, 4], height=300):
    with ui.card(full_screen=True):
        ui.card_header("Comparativa")

        @render_plotly
        def comparativa_plotly():
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
            )
            if df is None:
                return figure_text("Cargando...")
            tipo_graf = input.tipo()
            objective = get_objectives()
            if objective is None or df is None:
                return figure_text("Cargando...")
            fig = comparativa_fig(
                df,
                objective=objective[tipo_col[tipo_graf]],
                categoria=input.category(),
                seleccion=input.selected(),
                tipo_graf=tipo_graf,
            )
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Índice de Satisfacción")

        @render_plotly
        def satisfaccion_plotly():
            objective = get_objectives()
            if objective is None:
                return figure_text("Cargando...")
            objective = objective["Satisfaccion"]
            df = filter_data(
                data(),
                date=course_to_date(input.trim_start(), input.course_start()),
                category=input.category(),
                selected=input.selected(),
            )
            if df is None:
                return figure_text("Cargando...")
            fig = satisfaccion_fig(
                df,
                objective,
            )
            return fig
