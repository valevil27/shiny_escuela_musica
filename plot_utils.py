from typing import Literal
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure, FigureWidget
from shared import tipo_col


def mean_fig(
    data: pd.DataFrame,
    objective: float,
    col_name: str,
    name: str = None,
    normalize: bool = False,
    barmode: Literal["group", "stack"] = "group",
) -> FigureWidget:
    if not name:
        name = col_name

    fill_value = objective if normalize else 0

    df = (
        data.groupby(["Año_Curso", "Trimestre"], observed=True)[col_name]
        .mean()
        .sort_index()
    )
    df = df.reindex(
        pd.MultiIndex.from_product(
            [df.index.levels[0], df.index.levels[1]], names=["Año_Curso", "Trimestre"]
        ),
        fill_value=fill_value,
    ).reset_index()
    hover_data = {
        "Trimestre": True,
        "Año_Curso": False,
        "Label": False,
        col_name: ":.2f",
    }
    if normalize:
        df["ogs"] = df[col_name].apply(lambda x: f"{x:.2}" if pd.notnull(x) else "")
        df[col_name] = df[col_name] - objective
        hover_data["ogs"] = ":.2f"  # Mantenemos los valores originales al hacer hover
        hover_data[col_name] = False
    df["Label"] = df[col_name].apply(lambda x: f"{x:.2}" if pd.notnull(x) else "")
    fig = px.bar(
        df,
        x="Año_Curso",
        y=col_name,
        color="Trimestre",
        barmode=barmode,
        labels={
            col_name: name,
            "Año_Curso": "Curso",
            "color": "Trimestre",
            "ogs": name,
        },
        text="Label",
        hover_data=hover_data,
    )

    # cambiar la leyenda a horizontal
    fig.for_each_trace(lambda t: t.update(name=t.name.replace("_", " ")))
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom", 
            y=1.02,
            xanchor="left",
            x=0,
        )
    )
    fig.update_traces(textposition="auto")
    # Ocultar la barra de herramientas
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    if not normalize:
        fig.add_hline(y=objective, line_dash="dash")
    return fig


def satisfaccion_fig(
    data: pd.DataFrame,
    objective: float,
) -> FigureWidget:
    df = (
        data.groupby(["Año_Curso", "Satisfaccion"], observed=True)["ID_Alumno"]
        .count()
        .sort_index()
        .reset_index()
    )
    df["Porcentaje"] = df.groupby(["Año_Curso"], observed=False)["ID_Alumno"].transform(
        lambda x: x / x.sum() * 100
    )
    orden_satisfaccion = [5, 4, 3, 2, 1]  # Orden deseado
    df["Satisfaccion"] = pd.Categorical(
        df["Satisfaccion"], categories=orden_satisfaccion, ordered=True
    )
    df = df.sort_values(["Año_Curso", "Satisfaccion"], ascending=True)

    fig = px.bar(
        df,
        x="Año_Curso",
        y="Porcentaje",
        color=df["Satisfaccion"].astype(str),
        barmode="stack",
        # Puedes asignar tus colores de satisfacción
        color_discrete_map={
            "1": "rgb(255,0,0)",  # Rojo intenso
            "2": "rgb(255,102,102)",  # Rojo más claro
            "3": "rgb(255,255,102)",  # Amarillo
            "4": "rgb(144,238,144)",  # Verde claro
            "5": "rgb(0,128,0)",  # Verde intenso
        },
        labels={
            "Año_Curso": "Curso",
            "color": "Nivel de Satisfacción",
            "Porcentaje": "Porcentaje",
        },
        hover_data={
            "Satisfaccion": False,
            "Año_Curso": False,
            "Porcentaje": ":.2f",
        },
    )

    # 4. Ajustamos el layout si queremos
    fig.update_layout(yaxis_title="Porcentaje", xaxis_title="Curso", showlegend=False)
    fig.add_hline(y=objective * 100, line_dash="dash")
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    return fig


def avance_fig(
    data: pd.DataFrame, objective: float, normalize: bool = False
) -> FigureWidget:
    df = data[data["Curso"] == "Cuarto"]
    df = df[df["Trimestre"] == 3]
    if len(df) == 0:
        return figure_text("No se han realizado pruebas a estudios superiores en este periodo.", 14)
    # Contar cuantos alumnos han pasado al grado profesional cada año
    df = (
        df.groupby("Año_Curso", observed=True)[
            ["Avance_Grado_Profesional", "Pruebas_Grado_Profesional"]
        ]
        .apply(lambda x: x.sum() / x.count())
        .reset_index()
    )
    # Mostrar una gráfica de barras de plotly con los resultados para los que se presentan y los que avanzan
    if normalize:
        df["Avance_Grado_Profesional"] = df["Avance_Grado_Profesional"] - objective
        df["Pruebas_Grado_Profesional"] = df["Pruebas_Grado_Profesional"] - objective

    fig = px.bar(
        df,
        x="Año_Curso",
        y=["Pruebas_Grado_Profesional", "Avance_Grado_Profesional"],
        barmode="group",
        labels={
            "value": "Proporción de Alumnos de Cuarto",
            "variable": "Tipo",
            "Año_Curso": "Curso",
        },
        hover_data={
            "variable": False,
            "Año_Curso": False,
            "value": ":.2f",
        },
    )
    # cambiar la leyenda
    fig.for_each_trace(lambda t: t.update(name=t.name.replace("_", " ")))
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",  # Anclarla en la parte inferior
            y=1.02,
            xanchor="left",
            x=0,
        )
    )
    if not normalize:
        fig.add_hline(y=objective, line_dash="dash")
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    return fig


def prepare_df(data: pd.DataFrame, categoria: str, column: str) -> str:
    match column:
        case (
            "Aprobado"
            | "Horas_Practica"
            | "Promedio_Asistencia"
            | "Banda"
            | "Abandono_Educacion"
            | "Satisfaccion"
        ):
            return (
                data.groupby(categoria, observed=True)[column]
                .mean()
                .sort_index()
                .reset_index()
            )
        case "Avance_Grado_Profesional":
            data = data[data["Curso"] == "Cuarto"]  # Solo los alumnos de cuarto
            data = data[data["Trimestre"] == 3]  # Solo ultimo trimestre
            return (
                data.groupby(categoria, observed=True)[
                    ["Avance_Grado_Profesional", "Pruebas_Grado_Profesional"]
                ]
                .apply(lambda x: x.sum() / x.count())
                .reset_index()
            )
        case "Satisfaccion":
            return data
        case _:
            raise ValueError("Tipo de gráfica no soportada")


def comparativa_fig(
    data: pd.DataFrame,
    objective: float,
    categoria: str = "General",
    seleccion: str = "General",
    tipo_graf: str = "Tasa de aprobados",
) -> FigureWidget:
    col = tipo_col[tipo_graf]
    if categoria == "General":
        return figure_text("Seleccione una categoría para comenzar la comparativa.")

    df = prepare_df(data, categoria, col)
    title = f"{tipo_graf} por {categoria}"
    if seleccion != "General" and tipo_graf != "Satisfacción":
        # Evitamos que se quede el mensaje del error
        try:
            df[col] = df[col] - df[df[categoria] == seleccion][col].tolist()[0]
        except Exception as _:
            return figure_text("Cargando")
        title = f"{title}: {seleccion}"

    # Trato especial para avance
    if col == "Avance_Grado_Profesional":
        fig = fig_bar_acceso(df, categoria)
    elif col == "Satisfaccion":
        fig = fig_bar_satisfaccion(data, categoria)
    else:
        fig = px.bar(df, x=categoria, y=col, title=title)
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    if seleccion == "General":
        fig.add_hline(y=objective, line_dash="dash")
    return fig


def fig_bar_acceso(df: pd.DataFrame, categoria: str) -> Figure:
    fig = px.bar(
        df,
        x=categoria,
        y=["Pruebas_Grado_Profesional", "Avance_Grado_Profesional"],
        barmode="group",
        labels={
            "value": "Porcentaje de Alumnos de Cuarto",
            "variable": "Tipo",
            "Año_Curso": "Curso",
        },
    )
    fig.for_each_trace(lambda t: t.update(name=t.name.replace("_", " ")))
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",  # Anclarla en la parte inferior
            y=1.02,
            xanchor="left",
            x=0,
        )
    )
    return fig


def fig_bar_satisfaccion(df: pd.DataFrame, categoria: str) -> Figure:
    df = (
        df.groupby([categoria, "Satisfaccion"], observed=False)["ID_Alumno"]
        .count()
        .sort_index()
        .reset_index()
    )
    df["Porcentaje"] = df.groupby([categoria], observed=False)["ID_Alumno"].transform(
        lambda x: x / x.sum() * 100
    )
    orden_satisfaccion = [5, 4, 3, 2, 1]  # Orden deseado
    df["Satisfaccion"] = pd.Categorical(
        df["Satisfaccion"], categories=orden_satisfaccion, ordered=True
    )
    df = df.sort_values([categoria, "Satisfaccion"], ascending=True)
    fig = px.bar(
        df,
        x=categoria,
        y="Porcentaje",
        color=df["Satisfaccion"].astype(str),
        barmode="stack",
        # Puedes asignar tus colores de satisfacción
        color_discrete_map={
            "1": "rgb(255,0,0)",  # Rojo intenso
            "2": "rgb(255,102,102)",  # Rojo más claro
            "3": "rgb(255,255,102)",  # Amarillo
            "4": "rgb(144,238,144)",  # Verde claro
            "5": "rgb(0,128,0)",  # Verde intenso
        },
        labels={
            "Año_Curso": "Curso",
            "color": "Nivel de Satisfacción",
            "Porcentaje": "Porcentaje",
        },
        hover_data={
            "Satisfaccion": False,
            categoria: False,
            "Porcentaje": ":.2f",
        },
    )

    # 4. Ajustamos el layout si queremos
    fig.update_layout(yaxis_title="Porcentaje", xaxis_title=categoria, showlegend=False)
    return fig


def figure_text(texto: str, size: int = 24) -> FigureWidget:
    # Creamos un DataFrame mínimo con una sola fila
    df_text = pd.DataFrame({
        "x": [0],
        "y": [0],
        "texto": [texto],
    })

    # Generamos una figura scatter usando la columna 'texto'
    fig = px.scatter(
        df_text,
        x="x",
        y="y",
        text="texto",
    )

    # Ajustes para ocultar todo excepto el texto
    fig.update_traces(
        textposition="middle center", marker_opacity=0, textfont=dict(size=size)
    )
    # Centrar texto
    fig.update_xaxes(
        visible=False,
        range=[-1, 1],
    )
    fig.update_yaxes(visible=False, range=[-1, 1])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="white",
    )

    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False, "staticPlot": True}
    return fig
