import json
import random
import datetime
import urllib.parse
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
from modelo_prediccion import predecir_trafico_diario

def main():
    # Carga y preprocesamiento del dataset
    datosTrafico = pd.read_csv("Dataset_limpio.csv")
    datosTrafico["Fecha"] = pd.to_datetime(datosTrafico["Fecha"], format="%Y-%m-%d")
    datosTrafico["HoraInicio"] = pd.to_datetime(datosTrafico["HoraInicio"], format="%H:%M").dt.strftime("%H:%M")
    
    # Asegúrate de que estas columnas existen en tu CSV o ajústa los nombres
    if 'Feriado' not in datosTrafico.columns:
        datosTrafico['Feriado'] = 'No' 
    if 'Evento' not in datosTrafico.columns:
        datosTrafico['Evento'] = 'Ninguno' 
    if 'Congestion' not in datosTrafico.columns:
        datosTrafico['Congestion'] = pd.cut(datosTrafico['FlujoVehicular'], 
                                            bins=[0, 100, 500, 1000, datosTrafico['FlujoVehicular'].max()],
                                            labels=['Baja', 'Media', 'Alta', 'Muy Alta'])
        datosTrafico['Congestion'] = datosTrafico['Congestion'].astype(str)

    tablaTrafico = pd.DataFrame(datosTrafico)

    # --- ENCABEZADO DE LA PAGINA ---
    st.html("""
        <style>
            h1, h2, p, h3 {text-align: center;}
            .stColumn.st-emotion-cache-1mwoiw6.e1lln2w82 {padding: 10px; background: #222; border-radius: 10px;}
            /* Nuevo estilo para centrar el contenido de las columnas de métricas */
            .metric-container {
                display: flex;
                flex-direction: column;
                align-items: center; /* Centra horizontalmente */
                justify-content: center; /* Centra verticalmente */
                text-align: center; /* Asegura que el texto también esté centrado */
            }
            /* Estilo para las columnas de características (Predicción, Análisis, Rutas) */
            .feature-col {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            # {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 300px; /* Ajusta según sea necesario */
            }
        </style>
    """)
    st.title("🧭 :blue[Navegación Inteligente para una Lima sin Tráfico]", anchor=False)
    st.write("Descubre la forma más eficiente de moverte por la ciudad, optimizando tu tiempo y reduciendo el estrés.")
    st.divider()

    # --- CUERPO DE LA PAGINA (Features) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-col">', unsafe_allow_html=True)
        st.header("📊", False)
        st.subheader("Predicción Avanzada", False)
        st.write("Modelos predictivos de última generación.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-col">', unsafe_allow_html=True)
        st.header("🚦", False) # Revertido a icono de semáforo
        st.subheader("Análisis en Tiempo Real", False)
        st.write("Información del tráfico al instante.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="feature-col">', unsafe_allow_html=True)
        st.header("🗾", False)
        st.subheader("Rutas Inteligentes", False)
        st.write("Las mejores alternativas para tu destino.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    # --- SECCION DE NOTICIAS ---
    nt1 = """Reducción significativa del tráfico en días feriados:
    En rutas como la Av. Paseo de la República, el flujo vehicular disminuye considerablemente durante los feriados, especialmente en las horas de la madrugada, registrando niveles de congestión "muy bajos"."""
    nt2 = """Madrugada el mejor momento para circular por Lima:
    Los datos demuestran que entre la 1:00 a. m. y las 5:00 a. m., incluso en días normales, se registra un flujo vehicular muy bajo, lo que convierte a estas horas en las más recomendables para el transporte de carga o traslados rápidos."""
    nt3 = """Efecto de los eventos especiales sin impacto significativo:
    Según el conjunto de datos, la mayoría de los registros no reportan eventos especiales, y no se observan variaciones notables en el flujo vehicular cuando estos ocurren, lo cual podría indicar una planificación eficiente o falta de registro de eventos impactantes."""
    nt4 = """Jueves feriado día con menor tráfico vehicular:
    Los datos del 1 de mayo (jueves feriado) muestran consistentemente una baja congestión vehicular en todos los intervalos analizados, lo cual lo posiciona como un día ideal para actividades de mantenimiento vial."""
    nt5 = """ Congestión vehicular permanece en niveles bajos en la Av. Paseo de la República:
    En los registros recientes de mayo de 2025, se mantiene un nivel de congestión clasificado como "muy bajo", lo que podría estar relacionado con mejoras en la gestión del tránsito o menor actividad urbana."""
    
    numero = random.randint(0, 4)
    noticias = [nt1, nt2, nt3, nt4, nt5]
    f_nt = noticias[numero]
    st.header("Noticias de Tráfico", False)
    st.info(f_nt,icon="ℹ")
    st.divider()

    # --- SECCION DE PREDICCION ---
    st.header("Predicción de Tráfico 🚧", False)
    inputs1, inputs2 , inputs3 = st.columns(3)
    with inputs1:
        ubica_pred = st.selectbox("Ubicación de inicio 🏁.",sorted(datosTrafico["Zona"].unique()), key=333, placeholder="Todas", index= None)
    with inputs2:
        fecha_pred = st.date_input("Selecciona la fecha de predicción", value="today", min_value=datetime.date(2025, 1, 1), max_value=datetime.date(2025, 12, 31))
    with inputs3:
        feriado = st.selectbox("¿Es feriado?", ["No", "Si"], index=None, key=444, placeholder="Selecciona una opción")
    
    if str(ubica_pred) and str(feriado) == "None":
        st.info("Por favor, selecciona una ubicación de inicio válida.", icon="ℹ")
    else:
        prediccion = predecir_trafico_diario(str(ubica_pred), str(fecha_pred), str(feriado))
        st.dataframe(prediccion, hide_index=True)
        grafico_pre = px.area(prediccion, x="Intervalo", y="FlujoVehicular", color="Ruta", labels={"Intervalo": "Horas", "FlujoVehicular": "Flujo Vehicular"}, title="Flujo Vehicular por Hora por Zona")
        st.plotly_chart(grafico_pre, use_container_width=True)
    
    # --- SECCION DEL MAPA ---
    cl1, cl2 = st.columns(2)
    with cl1:
        st.subheader("Elige tu ruta deseada 🚘", False)
        ubi_start = st.selectbox("Ubicación de inicio 🏁.",sorted(datosTrafico["Zona"].unique()), key=111, placeholder="Todas", index= None)
        ubi_end = st.selectbox("Ubicación de destino 🔚.",sorted(datosTrafico["Zona"].unique()), key=222, placeholder="Todas",index= None)

        # Coordenadas de las zonas para el mapa
        coordinates = {
            "Av. Paseo de la Republica": {"lat": -12.113697, "lon": -77.025533}, 
            "Av. Alfredo Benavides": {"lat": -12.128233, "lon": -77.005189}, 
            "Av. Universitaria": {"lat": -12.001329, "lon": -77.083796}, 
            "Av. de la Marina": {"lat": -12.0600, "lon": -77.0800}, 
            "Av. Abancay": {"lat": -12.050864, "lon": -77.028302}, 
            "Av. Mexico": {"lat": -12.072974, "lon": -77.015255},  
            "Av. Argentina": {"lat": -12.050587, "lon": -77.122449}, 
            "Av. Venezuela": {"lat": -12.060980, "lon": -77.083312},  
        }
        zones = datosTrafico["Zona"].unique()
        map_data = pd.DataFrame(
            [{"Zona": zone, "lat": coordinates[zone]["lat"], "lon": coordinates[zone]["lon"]} for zone in zones]
        )
        map_data = map_data.merge(
            datosTrafico.groupby("Zona")["FlujoVehicular"].mean().reset_index(),
            on="Zona",
            how="left"
        )
        st.map(map_data, height=285)
    with cl2:
        if str(ubi_start) and str(ubi_end) == "None":
            components.html("""
                <div style="border:3px solid #2c3e50; border-radius:20px; overflow:hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
                    <script
                        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDOd6ZFmKTMdfjLuQ0v66SbN3vnOUdOOMY&libraries=maps,marker"
                        defer
                    ></script>
                    <gmp-map center="37.4220656,-122.21378127" zoom="10" map-id="" style="height: 500px"></gmp-map>
                </div>""", height=520)
        else:
            try: 
                ubi_start_f= ubi_start + ", Lima, Peru"
                ubi_end_f= ubi_end + ", Lima, Peru"
                res1 = urllib.parse.quote(ubi_start_f, safe='')
                res2 = urllib.parse.quote(ubi_end_f, safe='')
            except Exception as e:
                st.warning("No se pudo generar el mapa. Asegúrate de colocar las ubicaciones.")
                res1 = None
                res2 = None
            if res1 and res2:
                components.html(f"""
                <div style="border:3px solid #2c3e50; border-radius:20px; overflow:hidden; box-shadow: 0 8px 16px rgba(0,0,0,0.4);">
                    <iframe
                        src='https://www.google.com/maps/embed/v1/directions?key=AIzaSyAmBcsfFRbPqws5zmAewz69aw6HGRSVnZc&origin={res1}&destination={res2}&mode=driving&avoid=tolls&region=PE'
                        height="510" width= "100%"
                    ></iframe>
                </div>""",height=520)
    st.divider()


    # --- SECCION DE FILTROS Y GRAFICOS (ANCHO COMPLETO) ---
    st.subheader("Análisis de Flujo Vehicular y Congestión", anchor=False)
    
    opciones_feriado = ["Todas"] + sorted(datosTrafico["Feriado"].astype(str).unique().tolist())
    opciones_eventos = ["Todas"] + sorted(datosTrafico["Evento"].astype(str).unique().tolist())
    opciones_congestion = ["Todas"] + sorted(datosTrafico["Congestion"].astype(str).unique().tolist())

    f1, f2, f3 = st.columns(3, vertical_alignment="center")
    with f1:
        fecha_sel = st.selectbox("Fecha 📅", sorted(datosTrafico["Fecha"].dt.date.unique(), reverse=True), index=0)
        zona_sel = st.selectbox("Zona 🗾", ["Todas"] + sorted(datosTrafico["Zona"].unique()))
    with f2:
        feriado_sel = st.selectbox("Feriado 📆", opciones_feriado)
        evento_sel = st.selectbox("Eventos 🎉", opciones_eventos)
    with f3:
        congestion_sel = st.selectbox("Congestion 🚥", opciones_congestion)

    df_filt = datosTrafico[datosTrafico["Fecha"].dt.date == fecha_sel]
    if zona_sel != "Todas":
        df_filt = df_filt[df_filt["Zona"] == zona_sel]
    if feriado_sel != "Todas":
        df_filt = df_filt[df_filt["Feriado"].astype(str) == feriado_sel]
    if evento_sel != "Todas":
        df_filt = df_filt[df_filt["Evento"].astype(str) == evento_sel]
    if congestion_sel != "Todas":
        df_filt = df_filt[df_filt["Congestion"].astype(str) == congestion_sel]

    if df_filt.empty:
        st.warning("No hay datos para mostrar con los filtros seleccionados. Por favor, ajusta tus selecciones.")
    else:
        grafico_seleccionado = st.radio(
            "Selecciona el gráfico a mostrar:",
            ("Flujo Vehicular por Hora", "Flujo Vehicular Promedio por Zona"),
            horizontal=True
        )

        if grafico_seleccionado == "Flujo Vehicular por Hora":
            tipo_grafico = st.radio("Tipo de gráfico", ["Área", "Línea", "Barra", "Línea con Marcadores", "Boxplot"], horizontal=True)

            # Para el gráfico de flujo vehicular por hora, pivotamos después de filtrar
            if not df_filt.empty:
                # Aseguramos que la columna 'Zona' se use para el color
                # Convertimos a formato "long" para que Plotly Express pueda mapear el color fácilmente
                df_long = df_filt.melt(id_vars=["HoraInicio", "Zona"], 
                                       value_vars=["FlujoVehicular"], 
                                       var_name="Metrica", 
                                       value_name="Valor")
                
                # Filtrar solo la métrica de FlujoVehicular si se ha derretido otras
                df_long = df_long[df_long['Metrica'] == 'FlujoVehicular']

                # Definir una paleta de colores consistente
                # Puedes definir tus propios colores aquí si quieres un mapeo específico
                # Ejemplo: color_map = {"Av. Javier Prado": "red", "Av. Paseo de la Republica": "blue", ...}
                # Para un número mayor de zonas, Plotly usará su paleta por defecto si no se especifica.
                
                if tipo_grafico == "Área":
                    fig = px.area(df_long, x="HoraInicio", y="Valor", color="Zona",
                                  labels={"Valor": "Flujo Vehicular", "HoraInicio": "Hora"},
                                  title="Flujo Vehicular por Hora por Zona")
                elif tipo_grafico == "Línea":
                    fig = px.line(df_long, x="HoraInicio", y="Valor", color="Zona",
                                  labels={"Valor": "Flujo Vehicular", "HoraInicio": "Hora"},
                                  title="Flujo Vehicular por Hora por Zona")
                elif tipo_grafico == "Barra":
                    # Para barras, se podría acumular o mostrar barras agrupadas por zona.
                    # Aquí agrupamos para mostrar barras por zona en cada hora
                    fig = px.bar(df_long, x="HoraInicio", y="Valor", color="Zona", barmode='group',
                                 labels={"Valor": "Flujo Vehicular", "HoraInicio": "Hora"},
                                 title="Flujo Vehicular por Hora por Zona")
                elif tipo_grafico == "Línea con Marcadores":
                    fig = px.scatter(df_long, x="HoraInicio", y="Valor", color="Zona",
                                     labels={"Valor": "Flujo Vehicular", "HoraInicio": "Hora"},
                                     title="Flujo Vehicular por Hora por Zona")
                    fig.update_traces(mode='lines+markers')
                else:  # Boxplot
                    fig = px.box(df_long, x="HoraInicio", y="Valor", color="Zona", points="all",
                                 labels={"Valor": "Flujo Vehicular", "HoraInicio": "Hora"},
                                 title="Flujo Vehicular por Hora por Zona (Boxplot)")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para generar el gráfico de 'Flujo Vehicular por Hora' con los filtros aplicados.")

        elif grafico_seleccionado == "Flujo Vehicular Promedio por Zona":
            tipo_grafico_2 = st.radio("Tipo de gráfico", ["Barras", "Torta", "Barras Horizontales", "Rosquilla", "Dispersión"], horizontal=True)

            promedio_zona = df_filt.groupby("Zona")["FlujoVehicular"].mean().reset_index()

            if promedio_zona.empty:
                st.warning("No hay datos para calcular el promedio de flujo vehicular por zona con los filtros aplicados.")
            else:
                if tipo_grafico_2 == "Barras":
                    fig2 = px.bar(
                        promedio_zona,
                        x="Zona",
                        y="FlujoVehicular",
                        labels={"FlujoVehicular": "Flujo Vehicular Promedio", "Zona": "Zona"},
                        color="Zona", # Aseguramos el color por Zona
                        color_continuous_scale="Viridis", # Esto se aplicará si 'color' es una columna numérica
                        title="Flujo Vehicular Promedio por Zona"
                    )
                elif tipo_grafico_2 == "Torta":
                    fig2 = px.pie(
                        promedio_zona,
                        names="Zona",
                        values="FlujoVehicular",
                        title="Flujo Vehicular Promedio por Zona",
                        color="Zona" # Aseguramos el color por Zona
                    )
                elif tipo_grafico_2 == "Barras Horizontales":
                    fig2 = px.bar(
                        promedio_zona,
                        x="FlujoVehicular",
                        y="Zona",
                        orientation='h',
                        labels={"FlujoVehicular": "Flujo Vehicular Promedio", "Zona": "Zona"},
                        color="Zona", # Aseguramos el color por Zona
                        color_continuous_scale="Viridis",
                        title="Flujo Vehicular Promedio por Zona"
                    )
                elif tipo_grafico_2 == "Rosquilla":
                    fig2 = px.pie(
                        promedio_zona,
                        names="Zona",
                        values="FlujoVehicular",
                        hole=0.4,
                        title="Flujo Vehicular Promedio por Zona",
                        color="Zona" # Aseguramos el color por Zona
                    )
                else:  # Dispersión
                    fig2 = px.scatter(
                        promedio_zona,
                        x="Zona",
                        y="FlujoVehicular",
                        size="FlujoVehicular",
                        color="Zona",
                        labels={"FlujoVehicular": "Flujo Vehicular Promedio", "Zona": "Zona"},
                        title="Flujo Vehicular Promedio por Zona"
                    )
                st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # --- SECCION DE MULTIPLES METRICAS Y ANIMACIONES ---
    st.subheader("Métricas Clave y Estado del Tráfico", anchor=False)

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    # --- PRIMERA MÉTRICA Y ANIMACIÓN (Max Flujo Vehicular) ---
    with metric_col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        max_flujo_vehicular = datosTrafico["FlujoVehicular"].max()
        st.header(f"{max_flujo_vehicular}", anchor=False)
        st.write("max flujo vehicular")
        try:
            with open("animations/trafico.json", "r") as f:
                lottie_animation1 = json.load(f)
            st_lottie(lottie_animation1, speed=1, reverse=False, loop=True, quality="high", height=100, width=100, key="traffic_animation_1")
        except FileNotFoundError:
            st.error("Animación 'trafico.json' no encontrada.")
        except json.JSONDecodeError:
            st.error("Error en 'trafico.json'.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SEGUNDA MÉTRICA Y ANIMACIÓN (Ejemplo: Promedio de Flujo Vehicular) ---
    with metric_col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        promedio_flujo = int(datosTrafico["FlujoVehicular"].mean())
        st.header(f"{promedio_flujo}", anchor=False)
        st.write("promedio flujo vehicular")
        try:
            with open("animations/grafico2.json", "r") as f:
                lottie_animation2 = json.load(f)
            st_lottie(lottie_animation2, speed=1, reverse=False, loop=True, quality="high", height=100, width=100, key="traffic_animation_2")
        except FileNotFoundError:
            st.error("Animación 'grafico2.json' no encontrada.")
        except json.JSONDecodeError:
            st.error("Error en 'grafico2.json'.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TERCERA MÉTRICA Y ANIMACIÓN (Ejemplo: Zonas con Mayor Congestión) ---
    with metric_col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.header("5", anchor=False)
        st.write("zonas con alta congestión")
        try:
            with open("animations/grafico.json", "r") as f:
                lottie_animation3 = json.load(f)
            st_lottie(lottie_animation3, speed=1, reverse=False, loop=True, quality="high", height=100, width=100, key="traffic_animation_3")
        except FileNotFoundError:
            st.error("Animación 'grafico.json' no encontrada.")
        except json.JSONDecodeError:
            st.error("Error en 'grafico.json'.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- CUARTA MÉTRICA Y ANIMACIÓN (Ejemplo: Vehículos en Movimiento) ---
    with metric_col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.header("12k", anchor=False)
        st.write("vehículos en movimiento")
        try:
            with open("animations/carro.json", "r") as f:
                lottie_animation4 = json.load(f)
            st_lottie(lottie_animation4, speed=1, reverse=False, loop=True, quality="high", height=100, width=100, key="traffic_animation_4")
        except FileNotFoundError:
            st.error("Animación 'carro.json' no encontrada.")
        except json.JSONDecodeError:
            st.error("Error en 'carro.json'.")
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.divider()

if __name__ == "__main__":
    main()