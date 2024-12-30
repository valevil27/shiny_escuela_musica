from datetime import date, datetime, timedelta
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
    df = pd.read_csv(app_dir / "dataset.csv", parse_dates=["Fecha"])
    df["Año_Curso"] = pd.Categorical(
        df["Año_Curso"], categories=df["Año_Curso"].unique().sort(), ordered=True
    )
    df["Trimestre"] = pd.Categorical(
        df["Trimestre"],
        categories=[1, 2, 3],  # o las que correspondan
        ordered=True,
    )
    return df


# FIX si sale None resolver referencias
def filter_data(
    df: pd.DataFrame,
    date: datetime,
    category: str = "General",
    selected: str = "General",
) -> pd.DataFrame | None:
    df = df[df["Fecha"] >= date]
    if selected == "General":
        return df
    try:
        df = df[df[category] == selected]
    except Exception:
        return None
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
    "Aprobado": "+0.05",
    "Horas_Practica": 5,
    "Promedio_Asistencia": 0.8,
    "Banda": 0.8,
    "Abandono_Educacion": 0.1,
    "Avance_Grado_Profesional": "+0.1",
    "Satisfaccion": 0.8,
}


@reactive.calc
def get_objectives():
    df = data().copy()
    start_time = datetime.today() - timedelta(days=2 * 365)
    df = filter_data(df, start_time)
    objectives = dict()
    for col, obj in map_objective.items():
        objectives[col] = calculate_objective(obj, df, col)
    return objectives


@reactive.calc
def courses_df() -> list:
    return data()["Año_Curso"].sort_values(ascending=False).unique().tolist() # type: ignore


@reactive.calc
def get_filter() -> str:
    return input.filter()


trim_df = [1, 2, 3]


def last_entry_ds(today: date) -> tuple[int, str]:
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


def course_to_date(trim: int | str, course: str) -> datetime:
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


def calculate_objective(objective: str | float, data: pd.DataFrame, col: str) -> float:
    if type(objective) is not str:
        return float(objective)
    amount = float(objective) + 1
    match col:
        case "Aprobado":
            prev = (
                data.groupby(["Año_Curso", "Trimestre"], observed=True)[col]
                .mean()
                .sort_index()
            ).iloc[-2]
            return prev * amount

        case "Avance_Grado_Profesional":
            df = data[data["Curso"] == "Cuarto"]
            df = df[df["Trimestre"] == 3]
            if len(df) == 0:
                return 0
            prev = (
                df.groupby("Año_Curso", observed=True)["Avance_Grado_Profesional"]
                .apply(lambda x: x.sum() / x.count())
                .iloc[-2]
            )
            return prev * amount
        case _:
            raise ValueError("Columna no implementada")

    return amount


def period(trim: int, course: str) -> str:
    return f"T{trim} {course}"


if __name__ == "__main__":
    df = data()
    print(calculate_objective("-0.2", data(), "Aprobado"))
    print(calculate_objective("+0.2", data(), "Aprobado"))
    print(data())
