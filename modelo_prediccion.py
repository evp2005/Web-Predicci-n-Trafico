#===================
#   CREAR MODELO
#===================
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. Cargar el CSV limpio
df = pd.read_csv('dataset_trafico_limpio.csv')

# 2. Convertir fecha a datetime y extraer componentes
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Dia'] = df['Fecha'].dt.day
df['Mes'] = df['Fecha'].dt.month
df['DiaSemana'] = df['Fecha'].dt.dayofweek  # 0 = lunes

# 3. Features y target
features = ['Ruta', 'Feriado', 'Intervalo', 'Dia', 'Mes', 'DiaSemana']
target = 'FlujoVehicular'

# 4. Separar X e y
X = df[features]
y = df[target]

# 5. Preprocesamiento (OneHot para las categóricas)
cat_features = ['Ruta', 'Feriado', 'Intervalo']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
    ],
    remainder='passthrough'  # dejar Dia, Mes, DiaSemana como están
)

# 6. Pipeline de entrenamiento
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 7. Entrenamiento
model.fit(X, y)
print("✅ Modelo entrenado correctamente.")

# 8. Función para asignar categoría de congestión
def calcular_congestion(flujo):
    if flujo <= 50:
        return 'Muy Bajo'
    elif flujo <= 120:
        return 'Bajo'
    elif flujo <= 180:
        return 'Regular'
    elif flujo <= 250:
        return 'Alto'
    else:
        return 'Muy Alto'

def calcular_dia_semana(dia_semana):
    if dia_semana == 0:
        return 'Lunes'
    elif dia_semana == 1:
        return 'Martes'
    elif dia_semana == 2:
        return 'Miercoles'
    elif dia_semana == 3:
        return 'Jueves'
    elif dia_semana == 4:
        return 'Viernes'
    elif dia_semana == 5:
        return 'Sabado'
    elif dia_semana == 6:
        return 'Domingo'

# 9. Función de predicción
def predecir_trafico_diario(ruta, fecha, feriado):
    # Generar los 24 intervalos horarios del día
    intervalos = [f"{str(h).zfill(2)}:00-{str((h+1)%24).zfill(2)}:00" for h in range(24)]
    fecha_dt = pd.to_datetime(fecha)
    dia = fecha_dt.day
    mes = fecha_dt.month
    dia_semana = fecha_dt.dayofweek


    # Construir DataFrame de entrada
    input_df = pd.DataFrame({
        'Ruta': [ruta] * 24,
        'Feriado': [feriado.lower()] * 24,
        'Intervalo': intervalos,
        'Dia': [dia] * 24,
        'Mes': [mes] * 24,
        'DiaSemana': [dia_semana] * 24
    })

    # Predicción
    predicciones = model.predict(input_df)
    input_df['FlujoVehicular'] = predicciones.astype(int)

    # Agregar columnas extra
    input_df['Fecha'] = fecha_dt
    input_df['Congestion'] = input_df['FlujoVehicular'].apply(calcular_congestion)
    input_df['DiaSemana'] = calcular_dia_semana(dia_semana)

    # Reordenar columnas para mejor visualización
    return input_df[['Ruta', 'Fecha', 'DiaSemana', 'Intervalo', 'Feriado', 'FlujoVehicular', 'Congestion']]