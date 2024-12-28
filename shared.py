from datetime import date, timedelta
from pathlib import Path
import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_csv(app_dir / "dataset.csv")
start_time = date.today() - timedelta(weeks=12)

filter_options = [
    "General",
    "Curso",
    "Asignatura",
    "Profesor",
    "Instrumento",
]
