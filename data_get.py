import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# Configuración
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Parámetros
start_date = datetime.now() - timedelta(days=3*365)
end_date = datetime.now()
instruments = ["Viento Metal", "Viento Madera", "Percusión"]
subjects = ["Solfeo", "Coro", "Cámara", "Instrumento"]
courses = ["Iniciación", "Primero", "Segundo", "Tercero", "Cuarto"]
teachers = [fake.name() for _ in range(10)]
students = [fake.unique.first_name() for _ in range(100)]
data = []

# Generación de datos
for student_id, student_name in enumerate(students):
    enrollment_year = random.randint(1, 3)
    instrument = random.choice(instruments)
    start_year = start_date.year + enrollment_year - 1
    
    for year in range(start_year, end_date.year + 1):
        for month in [1, 6, 9]:  # Enero, Junio, Septiembre (coherencia escolar)
            date = datetime(year, month, 1)
            if date > end_date:
                break
            
            course = courses[min(year - start_year, len(courses) - 1)]
            band = (year - start_year >= 3 and random.random() < 0.8)
            subject = random.choice(subjects)
            teacher = random.choice(teachers)
            approved = random.random() < 0.9
            hours_practice = random.randint(1, 8)
            satisfaction = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 40, 40])[0]
            dropout = random.random() < 0.1
            exam_grado_profesional = (month == 6 and course == "Cuarto" and random.random() < 0.5)
            advance_grado_profesional = exam_grado_profesional and random.random() < 0.7
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
                avg_attendance
            ])

# Creación del DataFrame
columns = [
    "ID_Alumno", "Fecha", "Curso", "Años_Inscrito", "Banda", "Asignatura",
    "Instrumento", "Profesor", "Aprobado", "Horas_Practica", "Satisfaccion",
    "Abandono_Educacion", "Pruebas_Grado_Profesional", "Avance_Grado_Profesional",
    "Promedio_Asistencia"
]

df = pd.DataFrame(data, columns=columns)

# Guardar como CSV
file_path = "./escuela_musica_dataset.csv"
df.to_csv(file_path, index=False)
