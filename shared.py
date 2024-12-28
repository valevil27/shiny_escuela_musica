from datetime import date, timedelta
from pathlib import Path
import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "dataset.csv")

filter_options = [
    "General",
    "Curso",
    "Asignatura",
    "Profesor",
    "Instrumento",
]

courses_df = df.Año_Curso.unique().tolist()
trim_df = [1,2,3]


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


if __name__ == "__main__":
    print(last_entry_ds(date.today()))
