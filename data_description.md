# Descripción del Set de Datos

## ID alumno
- **Tipo**: Int
- **Descripción**: Una PK para la entrada

## Fecha
- **Tipo**: Date
- **Descripción**: Fecha en la que se toma el dato. Nos importa el mes y el año. Tomamos fechas hasta tres años atras, manteniendo la coherencia con el calendario escolar.
- **Gráficos en los que se usa**: Se usa como filtro y para comparación

## Curso
- **Tipo**: String
- **Descripción**: Nivel de la asignatura que se imparte. Consideramos desde iniciación musical hasta cuarto grado de elemental. Mantenemos la coherencia con el alumno y la asignatura dada de forma temporal. Un alumno pasa al siguiente curso de la asignatura si en el último trimestre del pasado año aprobó la asignatura.
- **Gráficos en los que se usa**: Se usa como filtro y para comparación

## Años Inscrito
- **Tipo**: Int
- **Descripción**: Años que el alumno lleva dando clase en la escuela. Mantenemos coherencia con el alumno y la fecha.
- **Gráficos en los que se usa**: Se usa para calculos derivados

## Banda
- **Tipo**: Boolean
- **Descripción**: Indica si el alumno ha entrado en la banda de música. Esto suele pasar en el año 3 desde que se inscribe en la escuela (suponemos distribución normal)
- **Objetivo**: 80% con 3 años inscritos en la escuela accedan a la banda
- **Gráficos en los que se usa**: Se usa para calculos derivados y gráfico 5

## Asignatura
- **Tipo**: String
- **Descripción**: Asignatura en cuestión. Se escogen de entre un número limitado de asignaturas relacionadas con la música (solfeo, coro, cámara, instrumento). Mantenemos coherencia, un mismo alumno debe dar las mismas asignaturas a lo largo de los años, avanzando o no de curso según si ha aprobado o no.
- **Gráficos en los que se usa**: Se usa como filtro y para comparación

## Instrumento
- **Tipo**: String
- **Descripción**: Instrumento principal del alumno. Solo se ofertan clases para instrumentos de viento metal, madera y percusión. Consideramos la percusión como un instrumento en sí mismo. Mantenemos coherencia, un alumno debe mantenerse con un mismo instrumento a lo largo del tiempo.
- **Gráficos en los que se usa**: Se usa como filtro y para comparación

## Profesor
- **Tipo**: String
- **Descripción**: Profesor del alumno en dicha asignatura. El set de profesores es limitado. Un profesor puede dar diferentes asignaturas, siempre y cuando estas estén relacionadas. Al igual que con las asignaturas y los cursos, mantenemos la coherencia con los profesores, es decir, un alumno en tercero de trompeta debe haber realizado primero y segundo de trompeta en años anteriores, a poder ser manteniendo el mismo profesor.
- **Gráficos en los que se usa**: Se usa como filtro y para comparación

## Aprobado
- **Tipo**: Boolean
- **Descripción**: El alumno ha aprobado o no
- **Objetivo**: Aumento del 5% anual
- **Gráficos en los que se usa**: 1

## Horas Práctica
- **Tipo**: Int
- **Descripción**: Horas que el alumno dedica a la práctica en casa
- **Objetivo**: 5 horas semanales
- **Gráficos en los que se usa**: 2

## Satisfacción
- **Tipo**: Int
- **Descripción**: Satisfacción general del alumno con la asignatura. Los valores van desde 1 (nada satisfecho) a 5 (totalmente satisfecho)
- **Objetivo**: Los valores 4 y 5 deben representar en torno al 80% del conjunto
- **Gráficos en los que se usa**: 3

## Abandono Educación
- **Tipo**: Boolean
- **Descripción**: Si el alumno abandonó la escuela de música en este periodo. En caso de ser positivo se suspende la materia y no vuelve a aparecer en el set. No se cuenta a la hora de realizar cálculos derivados
- **Objetivo**: Menor del 10%
- **Gráficos en los que se usa**: 4 y filtro para cálculos

## Pruebas a Grado Profesional
- **Tipo**: Boolean
- **Descripción**: Si el alumno realizó el examen de acceso a grado medio. Estas pruebas se realizan normalmente a partir del cuarto grado de elemental, aunque podría darse antes. Se realizan al finalizar el tercer trimestre según el calendario escolar, es decir, los valores positivos se registran solamente en el mes de junio.
- **Objetivo**: Todos los alumnos de 
- **Gráficos en los que se usa**: 6 y filtro para cálculos

## Avance a Grado Profesional
- **Tipo**: Boolean
- **Descripción**: Si el alumno aprobó el examen de acceso a grado medio. Estas pruebas se realizan normalmente a partir del cuarto grado de elemental, aunque podría darse antes. Una vez aprobados, el alumno deja de aparecer en el dataset. Exclusivo con abandono educación. Solo puede ser positivo si el alumno se ha presentado a las pruebas (Prueba Grado Profesional).
- **Objetivo**: 
- **Gráficos en los que se usa**: 6 

## Promedio Asistencia
- **Tipo**: Float
- **Descripción**: Porcentaje de asistencia del alumno.
- **Objetivo**: 80%
- **Gráficos en los que se usa**: 7

