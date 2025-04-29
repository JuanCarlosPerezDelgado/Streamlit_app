from datetime import datetime         
import pandas as pd
import matplotlib.pyplot as plt     
import numpy as np
import streamlit as st
import altair as alt
from time import sleep
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import CoolProp.CoolProp as CP
from scipy.optimize import minimize_scalar
from scipy.optimize import minimize
import plotly.graph_objects as go
from plotly.subplots import make_subplots



#Definición de función
def representacion_grafico(propiedades_ciclo,variables_ciclo,indicadores_termodinamicos,velocidad_reproduccion,tipo_grafico_diferido,lista_variables_diferido,df_analizador_redes_ensayo,df_equipo_ensayo,df_evaporador_04_ensayo,df_valvula_expansion_05_ensayo,df_evaporador_06_ensayo,df_valvula_expansion_07_ensayo):

    #Concatenar los dataframe que tienen columnas seleccionadas
    df_ampliado=pd.concat([df_equipo_ensayo,df_analizador_redes_ensayo,df_evaporador_04_ensayo,df_valvula_expansion_05_ensayo,df_evaporador_06_ensayo,df_valvula_expansion_07_ensayo],axis=1)
    df_ampliado=df_ampliado[lista_variables_diferido]
    variables_analogicas=["Potencia total (W)","Energia total (kWh)","Temperatura camara (evaporador 1) (°C)","Temperatura desescarche (evaporador 1) (°C)","Presion de baja (valvula expansion 1) (bar)","Temperatura aspiracion (valvula expansion 1) (°C)","Recalentamiento (valvula expansion 1) (K)","Apertura valvula (valvula expansion 1) (%)","Temperatura camara (evaporador 2) (°C)","Temperatura desescarche (evaporador 2) (°C)","Presion de baja (valvula expansion 2) (bar)","Temperatura aspiracion (valvula expansion 2) (°C)","Recalentamiento (valvula expansion 2) (K)","Apertura valvula (valvula expansion 2) (%)",'Presion evaporacion (bar)','Temperatura evaporacion (°C)',"Presion condensacion (bar)","Temperatura condensacion (°C)","Presion deposito (bar)","Temperatura deposito (°C)","Temperatura exterior (°C)","Temperatura salida gas cooler (°C)","Temperatura aspiracion (°C)","Temperatura descarga (°C)","Temperatura liquido (°C)","Potencia compresor (%)","Potencia ventilador gas-cooler (%)","Apertura valvula by-pass (%)","Apertura valvula alta presion (%)"]
    variables_digitales=["Rele desescarche (evaporador 1) (on/off)","Rele ventilador (evaporador 1) (on/off)","Rele valvula (evaporador 1) (on/off)","Estado desescarche (evaporador 1) (on/off)","Estado dispositivo (evaporador 1) (on/off)","Estado valvula (valvula expansion 1) (on/off)","Rele desescarche (evaporador 2) (on/off)","Rele ventilador (evaporador 2) (on/off)","Rele valvula (evaporador 2) (on/off)","Estado desescarche (evaporador 2) (on/off)","Estado dispositivo (evaporador 2) (on/off)","Estado valvula (valvula expansion 2) (on/off)","Rele compresor (on/off)"]
    lista_variables_analogicas=list(set(variables_analogicas) & set(lista_variables_diferido))
    lista_variables_digitales=list(set(variables_digitales) & set(lista_variables_diferido))
    df_ampliado_analogico=df_ampliado[lista_variables_analogicas].copy()
    df_ampliado_digital=df_ampliado[lista_variables_digitales].copy()
    df_ampliado_scada=pd.concat([df_ampliado_analogico,df_ampliado_digital],axis=1)
    df_ampliado_tabla=df_ampliado_scada
    df_ampliado_tabla.loc[:,"Indice"] = df_ampliado.index.strftime('%H:%M')

    df_ampliado_analogico.loc[:,"Tiempo"] = range(len(df_ampliado_analogico))
    df_ampliado_analogico.loc[:,"Indice"] = df_ampliado_analogico.index.strftime('%H:%M')
    df_ampliado_digital.loc[:,"Tiempo"] = range(len(df_ampliado_digital))
    df_ampliado_digital.loc[:,"Indice"] = df_ampliado_digital.index.strftime('%H:%M')

    #Placeholder para el indicador del tiempo
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2,col3,col4,col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col3:
        tiempo=st.empty()
    with col4:
        pass
    with col5:
        pass

    # Crear una placeholder para la gráfica
    if 'Gráfico de líneas' in tipo_grafico_diferido and lista_variables_diferido:
        st.markdown("<br>", unsafe_allow_html=True)
        chart_analogica = st.empty()  # Placeholder para la gráfica
        chart_digital = st.empty() #Placeholder para la gráfica

    st_autorefresh = st.experimental_rerun
    if 'i' not in st.session_state:
        st.session_state.i = 0


    lista_tiempo=df_ampliado_analogico["Indice"].tolist()
    if st.session_state.i < len(df_ampliado_analogico):

        tiempo.markdown(f"""<div style="background-color: #e1f5fe;padding: 1rem;border-radius: 0.25rem;text-align: center;font-weight: 500;color: #01579b;">{f'Minuto: {i} - Hora: {lista_tiempo[i]}'}</div>""",unsafe_allow_html=True)

        if 'Gráfico de líneas' in tipo_grafico_diferido and lista_variables_diferido:
            # Gráfica analógica
            if not df_ampliado_analogico.empty and any(col in df_ampliado_analogico.columns for col in lista_variables_diferido):
                df_actual_analogico = df_ampliado_analogico.iloc[:i + 1]
                df_melted_analogico = df_actual_analogico.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')

                fig_analogica = px.line(
                    df_melted_analogico,
                    x='Tiempo',
                    y='Valor',
                    color='Variable',
                    labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Valor'},
                    title='Gráfica de variables analógicas',custom_data=['Indice'])
                fig_analogica.update_traces(
                    hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
                )
                fig_analogica.update_layout(
                    width=None,
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                    xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_ampliado_analogico['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                    yaxis=dict(showgrid=True,gridcolor='lightgray',mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Valor', font=dict(color='black'))))
                chart_analogica.plotly_chart(fig_analogica)

                # Gráfica digital
            if not df_ampliado_digital.empty and any(col in df_ampliado_digital.columns for col in lista_variables_diferido):
                df_actual_digital = df_ampliado_digital.iloc[:i + 1]
                df_melted_digital = df_actual_digital.melt(id_vars=['Tiempo','Indice'], var_name='Variable', value_name='Valor')

                fig_digital = px.line(
                    df_melted_digital,
                    x='Tiempo',
                    y='Valor',
                    color='Variable',
                    labels={'Tiempo': 'Tiempo (minutos)', 'Valor': 'Estado'},
                    title='Gráfica de variables digitales',custom_data=['Indice'])
                fig_digital.update_traces(
                    hovertemplate="Tiempo: %{x}<br>Valor: %{y}<br>Hora: %{customdata[0]}<br>Variable: %{fullData.name}<extra></extra>"
                )
                # Ajustes específicos para señales digitales
                fig_digital.update_layout(
                    width=None,
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=-0.4,title_font_color='black'),
                    xaxis=dict(showgrid=True, gridcolor='lightgray',range=[0,df_ampliado_analogico['Tiempo'].max()],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Tiempo (minutos)', font=dict(color='black'))),
                    yaxis=dict(showgrid=True,gridcolor='lightgray',tickvals=[0, 1], range=[-0.1, 1.1],mirror=False,linecolor='black',tickfont=dict(color='black'),title=dict(text='Valor', font=dict(color='black'))))
                chart_digital.plotly_chart(fig_digital)
# ⬇️ Avanzamos al siguiente punto
        st.session_state.i += 1

    # ⬇️ Refrescamos automáticamente
        st.experimental_rerun()
