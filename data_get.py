import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# Probabilidades
prob = {
    "examen_4": 0.8,
    "examen_3": 0.4,
    "aprobar_examen": 0.8,
}

# Configuración
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Parámetros
start_date = datetime.now() - timedelta(days=6 * 365)
end_date = datetime.now()
instruments = ["Viento Metal", "Viento Madera", "Percusión"]
subjects = ["Solfeo", "Coro", "Cámara", "Instrumento"]
courses = ["Iniciación", "Primero", "Segundo", "Tercero", "Cuarto"]
teachers = [fake.name() for _ in range(10)]
students = [fake.unique.first_name() for _ in range(200)]
data = []

# Generación de datos
for student_id, student_name in enumerate(students):
    enrollment_year = random.randint(1, 3)
    instrument = random.choice(instruments)
    start_year = start_date.year + enrollment_year - 1

    for year in range(start_year, end_date.year + 1):
        for month in [12, 3, 6]:  # calendario escolar
            date = datetime(year, month, 30)
            if date > end_date:
                break

            course = courses[min(year - start_year, len(courses) - 1)]
            band = year - start_year >= 3 and random.random() < 0.8
            subject = random.choice(subjects)
            teacher = random.choice(teachers)
            approved = random.random() < 0.9
            hours_practice = random.randint(1, 8)
            satisfaction = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 40, 40])[
                0
            ]
            dropout = random.random() < 0.1
            exam_grado_profesional = (
                month == 6
                and course == "Cuarto"
                and random.random() < prob["examen_4"]
                or month == 6
                and course == "Tercero"
                and random.random() < prob["examen_3"]
            )
            advance_grado_profesional = (
                exam_grado_profesional and random.random() < prob["aprobar_examen"]
            )
            avg_attendance = round(random.uniform(0.6, 1.0), 2)

            # Aseguramos que no hay datos después del abandono o avance a grado profesional
            if dropout or advance_grado_profesional:
                break

            # Añadimos datos al dataset
            data.append([
                student_id + 1,
                date.date(),
                course,
                year - start_year + 1,
                band,
                subject,
                instrument,
                teacher,
                approved,
                hours_practice,
                satisfaction,
                dropout,
                exam_grado_profesional,
                advance_grado_profesional,
                avg_attendance,
            ])

# Creación del DataFrame
columns = [
    "ID_Alumno",
    "Fecha",
    "Curso",
    "Años_Inscrito",
    "Banda",
    "Asignatura",
    "Instrumento",
    "Profesor",
    "Aprobado",
    "Horas_Practica",
    "Satisfaccion",
    "Abandono_Educacion",
    "Pruebas_Grado_Profesional",
    "Avance_Grado_Profesional",
    "Promedio_Asistencia",
]

# Lista de cursos en orden de probabilidad

curso_probabilidades = {
    "Iniciación": 0.1,
    "Primero": 0.3,
    "Segundo": 0.5,
    "Tercero": 0.7,
    "Cuarto": 0.9,
}


def calculate_trimester(date):
    if date.month in [9, 10, 11, 12]:  # 1º Trimestre
        return 1

    elif date.month in [1, 2, 3]:  # 2º Trimestre
        return 2

    elif date.month in [4, 5, 6, 7, 8]:  # 3º Trimestre
        return 3
    else:
        raise ValueError("Invalid month", date.month)


# Crear columna Año_Curso
def calculate_school_year(date):
    year = date.year
    if date.month >= 9:  # De septiembre a diciembre pertenece al siguiente año escolar
        return f"{year}-{year + 1}"
    else:  # De enero a agosto pertenece al año escolar anterior
        return f"{year - 1}-{year}"


# Arreglar la columna "Banda" manteniendo la coherencia por ID_Alumno
def asignar_banda(grupo):
    grupo = grupo.sort_values("Fecha")  # Ordenar por fecha

    pertenece_a_banda = False

    for index, row in grupo.iterrows():
        if row["Años_Inscrito"] >= 3:
            probabilidad = curso_probabilidades.get(row["Curso"], 0.0)

            if not pertenece_a_banda:  # Asignar si aún no pertenece
                pertenece_a_banda = np.random.rand() < probabilidad

            grupo.at[index, "Banda"] = pertenece_a_banda

        else:
            grupo.at[index, "Banda"] = False

    return grupo


df = pd.DataFrame(data, columns=columns)

df["Trimestre"] = df["Fecha"].apply(calculate_trimester)
df["Año_Curso"] = df["Fecha"].apply(calculate_school_year)
# Aplicar la función por cada ID de alumno para asignar el acceso a banda 
df = df.groupby("ID_Alumno", group_keys=False).apply(asignar_banda)

# Guardar como CSV
file_path = "./escuela_musica_dataset.csv"
df.to_csv(file_path, index=False)
