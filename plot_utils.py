from typing import Literal
import pandas as pd
import plotly.express as px
from plotly.graph_objects import FigureWidget


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

    df = (
        data.groupby(["Año_Curso", "Trimestre"], observed=False)[col_name]
        .mean()
        .sort_index()
        .reset_index()
    )
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
        color=df.Trimestre.astype(str),
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

    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
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
        data.groupby(["Año_Curso", "Satisfaccion"], observed=False)["ID_Alumno"]
        .count()
        .sort_index()
        .reset_index()
    )
    df["Porcentaje"] = df.groupby(["Año_Curso"], observed = False)["ID_Alumno"].transform(
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

def avance_fig(data: pd.DataFrame, objective: float, normalize: bool = False) -> FigureWidget:
    df = data
    df = df[df['Curso'] == 'Cuarto']
    df = df[df['Trimestre'] == 3]
    # Contar cuantos alumnos han pasado al grado profesional cada año
    df = df.groupby("Año_Curso", observed=True)[['Avance_Grado_Profesional', 'Pruebas_Grado_Profesional']].apply(lambda x: x.sum() / x.count()).reset_index()
    # Mostrar una gráfica de barras de plotly con los resultados para los que se presentan y los que avanzan
    if normalize:
        df['Avance_Grado_Profesional'] = df['Avance_Grado_Profesional'] - objective
        df['Pruebas_Grado_Profesional'] = df['Pruebas_Grado_Profesional'] - objective

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
    if not normalize:
        fig.add_hline(y=objective, line_dash="dash")
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    return fig
