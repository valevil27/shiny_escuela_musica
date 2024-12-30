from datetime import date, datetime
from pathlib import Path

import pandas as pd
from shiny import reactive
from shiny.express import input
import logging

logging.basicConfig(
    level=logging.INFO,  # muestra mensajes de nivel INFO o superior
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app_dir = Path(__file__).parent


@reactive.calc
def data() -> pd.DataFrame:
    df = pd.read_csv(app_dir / "dataset_v2.csv", parse_dates=["Fecha"])
    df["Año_Curso"] = pd.Categorical(
        df["Año_Curso"], categories=df["Año_Curso"].unique().sort(), ordered=True
    )
    df["Trimestre"] = pd.Categorical(
        df["Trimestre"],
        categories=[1, 2, 3],  # o las que correspondan
        ordered=True,
    )
    return df


def filter_data(
    df: pd.DataFrame,
    date: datetime,
    category: str = "General",
    selected: str = "General",
):
    df = df[df["Fecha"] >= date]
    if selected == "General":
        return df
    df = df[df[category] == selected]
    df["Año_Curso"] = df["Año_Curso"].cat.remove_unused_categories()
    df["Trimestre"] = df["Trimestre"].cat.remove_unused_categories()
    return df


filter_options = [
    "General",
    "Curso",
    "Asignatura",
    "Profesor",
    "Instrumento",
]

type_options = [
    "Tasa de aprobados",
    "Horas de práctica",
    "Asistencia",
    "Acceso a banda",
    "Abandono escolar",
    "Avance a profesional",
    "Satisfacción",
]

tipo_col = {
    "Tasa de aprobados": "Aprobado",
    "Horas de práctica": "Horas_Practica",
    "Asistencia": "Promedio_Asistencia",
    "Acceso a banda": "Banda",
    "Abandono escolar": "Abandono_Educacion",
    "Avance a profesional": "Avance_Grado_Profesional",
    "Satisfacción": "Satisfaccion",
}

map_filter_cols = {
    "General": None,
    "Curso": "Año_Curso",
    "Asignatura": "Asignatura",
    "Profesor": "Instrumento",
    "Instrumento": "Profesor",
}

map_objective = {
    "Aprobado": 0.8,
    "Horas_Practica": 4,
    "Promedio_Asistencia": 0.8,
    "Banda": 0.8,
    "Abandono_Educacion": 0.1,
    "Avance_Grado_Profesional": 0.8,
    "Satisfaccion": 80,
}


@reactive.calc
def courses_df() -> list[str]:
    return data().Año_Curso.sort_values(ascending=False).unique().tolist()


@reactive.calc
def get_filter() -> str:
    return input.filter()


trim_df = [1, 2, 3]


def last_entry_ds(today: date) -> tuple[str, int]:
    today = date.today()
    month, year = today.month, today.year
    match month:
        case x if x < 3:
            return 1, f"{year - 1}-{year}"
        case x if 3 <= x < 6:
            return 2, f"{year - 1}-{year}"
        case x if 6 <= x < 12:
            return 3, f"{year - 1}-{year}"
        case x if x == 12:
            return 1, f"{year}-{year + 1}"
        case _:
            raise ValueError("Not a valid month")


def select_choices(df: pd.DataFrame, filter: str) -> list[str]:
    base_lst = ["General"]
    if filter not in map_filter_cols.keys():
        raise ValueError("Not a filter")
    if filter == "General":
        return base_lst
    base_lst.extend(df[filter].unique().tolist())
    return base_lst


def course_to_date(trim: int | str, course: str) -> date:
    if type(trim) is str:
        trim = int(trim)
    match trim:
        case 1:
            month = 12
            year = int(course.split("-")[0])
        case 2:
            month = 3
            year = int(course.split("-")[1])
        case 3:
            month = 6
            year = int(course.split("-")[1])
        case _:
            raise ValueError("Unexpected trimester")
    return datetime(year, month, 1)


def period(trim: int, course: str) -> str:
    return f"T{trim} {course}"


if __name__ == "__main__":
    print(last_entry_ds(date.today()))
