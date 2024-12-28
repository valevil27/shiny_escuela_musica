import pandas as pd
import plotly.express as px
from plotly.graph_objects import FigureWidget


def mean_fig(
    data: pd.DataFrame, col_name: str, name: str = None
) -> FigureWidget:
    if not name:
        name = col_name

    df = (
        data
        .groupby(["Año_Curso", "Trimestre"], observed=False)[col_name]
        .mean()
        .sort_index()
        .reset_index()
    )
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
        },
        text="Label",
        hover_data={
            "Trimestre": True,
            "Año_Curso": False,
            "Label": False,
            col_name: ":.2f",
        },
    )

    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
    # Ocultar la barra de herramientas
    fig = FigureWidget(fig)
    fig._config = fig._config | {"displayModeBar": False}
    return fig
