# Volver a cargar las bibliotecas y dataset debido al reinicio
from datetime import date, timedelta
import pandas as pd
import numpy as np
from faker import Faker

# Generar datos iniciales necesarios
fake = Faker()
cursos = ["Iniciación", "Primero", "Segundo", "Tercero", "Cuarto"]
curso_probabilidades = {
    "Iniciación": 0.1,
    "Primero": 0.3,
    "Segundo": 0.5,
    "Tercero": 0.7,
    "Cuarto": 0.9,
}
instrumentos = [
    "Trompeta",
    "Trompa",
    "Saxofón",
    "Clarinete",
    "Percusión",
    "Flauta",
    "Trombón",
]
asignaturas = ["Solfeo", "Instrumento", "Coro", "Cámara"]
profesores = [fake.name() for _ in range(10)]


# Función para generar nuevos datos de alumnos inscritos en años posteriores
def generar_alumnos(id_inicial, n_alumnos):
    start_year = (date.today() - timedelta(days=6 * 365)).year
    end_year = date.today().year
    data = []
    for i in range(n_alumnos):
        id_alumno = id_inicial + i
        abandono = False
        pruebas = False
        profesional = False
        # Año de inscripción
        año_inicio = np.random.randint(
            int(start_year), int(end_year) + 1
        )  
        # Posible curso inicial
        curso_inicial = np.random.choice([
            "Iniciación",
            "Primero",
            "Segundo",
        ])  
        años_inscrito = 0

        # Generar datos por año y trimestre
        for año in range(año_inicio, int(end_year) + 1):
            for mes in [12, 3, 6]:  # Enero, Junio, Septiembre
                años_inscrito += (
                    1 if mes == 12 else 0
                )  # Incrementar años inscritos en diciembre
                match mes:
                    case 12:
                        trimestre = 1
                        curso = f"{año}-{año+1}"
                    case 3:
                        trimestre = 2
                        curso = f"{año-1}-{año}"
                    case 6:
                        trimestre = 3
                        curso = f"{año-1}-{año}"
                probabilidad_banda = curso_probabilidades.get(curso_inicial, 0.0)
                pertenece_a_banda = (
                    años_inscrito >= 2 and np.random.rand() < probabilidad_banda
                )
                # Abandono escolar
                if np.random.rand() < 0.08:
                    abandono = True

                # Pruebas grado medio
                pruebas = (
                    not abandono
                    and trimestre == 3
                    and (
                        curso_inicial in ["Tercero", "Cuarto"]
                        and np.random.rand() < curso_probabilidades[curso_inicial]
                    )
                )
                profesional = pruebas and np.random.rand() < 0.8

                data.append({
                    "ID_Alumno": id_alumno,
                    "Fecha": f"{año}-{mes:02d}-01",
                    "Curso": curso_inicial,
                    "Años_Inscrito": años_inscrito,
                    "Año_Curso": curso,
                    "Trimestre": trimestre,
                    "Banda": pertenece_a_banda,
                    "Asignatura": np.random.choice(asignaturas),
                    "Instrumento": np.random.choice(instrumentos),
                    "Profesor": np.random.choice(profesores),
                    "Aprobado": np.random.rand() < 0.8,  # 80% probabilidad de aprobar
                    "Horas_Practica": np.random.randint(1, 8),
                    "Satisfaccion": np.random.choice([1,2,3,4,5], p = [0.05,0.05,0.15,0.4,0.35]),
                    "Abandono_Educacion": abandono,
                    "Pruebas_Grado_Profesional": pruebas,
                    "Avance_Grado_Profesional": profesional,
                    "Promedio_Asistencia": round(np.random.uniform(0.6, 1.0), 2),
                })
                if abandono or profesional:
                    break

                # Actualizar el curso inicial si corresponde avanzar
                if (
                    mes == 6 and np.random.rand() < 0.8
                ):  # 80% probabilidad de avanzar de curso
                    curso_inicial = cursos[
                        min(cursos.index(curso_inicial) + 1, len(cursos) - 1)
                    ]
            if abandono or profesional:
                break

    return pd.DataFrame(data)


# Generar nuevos datos para alumnos inscritos en años posteriores
id_inicial = 1
nuevos_alumnos = 300
df_alumnos = generar_alumnos(id_inicial, nuevos_alumnos)

# Guardar el archivo actualizado
df_alumnos.to_csv("./dataset_v2.csv", index=False)
