from datetime import date
from pathlib import Path

import pandas as pd
from shiny import reactive

app_dir = Path(__file__).parent
@reactive.calc
def data() -> pd.DataFrame:
    df = pd.read_csv(app_dir / "dataset_v2.csv")
    df["Periodo"] = "T" + df["Trimestre"].astype(str) + " " + df["Año_Curso"]
    df["Año_Curso"] = pd.Categorical(df["Año_Curso"], categories=df["Año_Curso"].unique().sort(), ordered=True)
    return df

filter_options = [
    "General",
    "Curso",
    "Asignatura",
    "Profesor",
    "Instrumento",
]

map_filter_cols = {
    "General": None,
    "Curso": "Año_Curso",
    "Asignatura": "Asignatura",
    "Profesor": "Instrumento",
    "Instrumento": "Profesor",
}

@reactive.calc
def courses_df():
    return data().Año_Curso.sort_values(ascending=False).unique().tolist()

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


def course_to_date(trim: int, course: str) -> date:
    match trim:
        case 1:
            month = 1
            year = int(course.split("-")[0])
        case 2:
            month = 2
            year = int(course.split("-")[0])
        case 3:
            month = 3
            year = int(course.split("-")[1])
        case _:
            raise ValueError("Unexpected trimester")
    return date(year, month, 1)

def period(trim: int, course: str) -> str:
    return f"T{trim} {course}"


if __name__ == "__main__":
    print(last_entry_ds(date.today()))
