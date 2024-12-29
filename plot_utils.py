import pandas as pd
import numpy as np
import plotly.express as px
from plotly.graph_objects import FigureWidget


def mean_fig(
    data: pd.DataFrame,
    objective: float,
    col_name: str,
    name: str = None,
    normalize: bool = False,
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
        barmode="group",
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

def pie_fig(data: pd.DataFrame, objective: float) -> FigureWidget:
    df = data.Satisfaccion.value_counts().reset_index()
    df.columns = ["Satisfaccion", "count"]

    # Ordenar los valores de satisfacción en el orden deseado
    orden_satisfaccion = [4, 3, 2, 1, 5]  # Orden deseado
    df["Satisfaccion"] = pd.Categorical(
        df["Satisfaccion"], categories=orden_satisfaccion, ordered=True
    )
    df = df.sort_values("Satisfaccion", ascending=True)
    fig = px.pie(
        df, 
        names = "Satisfaccion",
        values = "count",
        color="Satisfaccion",  # Columna para asignar colores
        color_discrete_map={
            1: "rgb(255,0,0)",  # Rojo intenso
            2: "rgb(255,102,102)",  # Rojo más claro
            3: "rgb(255,255,102)",  # Amarillo
            4: "rgb(144,238,144)",  # Verde claro
            5: "rgb(0,128,0)",  # Verde intenso
        },
        )
    fig.update_traces(sort=False, rotation=0)
    # Añadir una línea para el 80%
    theta = - 2*np.pi * objective + np.pi / 2 # Convertir el porcentaje a radianes
    x_start, y_start = 0.5, 0.5  # Centro del gráfico
    x_end =  0.41 * np.cos(theta) + x_start  # Coordenadas finales
    y_end =  0.41 * np.sin(theta) + y_start

    fig.add_shape(
        type="line",
        xref="paper", yref="paper",
        x0=x_start, y0=y_start,
        x1=x_end, y1=y_end,
        line=dict(color="black", width=4, dash="dash"),
    )

    # Añadir anotación para la meta
    fig.add_annotation(
        x=x_end - 0.1,
        y=y_end,
        xref="paper", yref="paper",
        text=f"{objective:.0%}",
        showarrow=False,
        font=dict(size=16, color="black"),
    )
    fig.update_layout(showlegend=False, margin=dict(l=0))
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    return fig
