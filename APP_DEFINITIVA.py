from datetime import datetime, timedelta,date         
import pandas as pd
import matplotlib.pyplot as plt     
import numpy as np
import streamlit as st
from time import sleep
import streamlit_option_menu
from streamlit_option_menu import option_menu
import plotly.express as px
import webbrowser

#Importar funciones
from busquedaensayo import busqueda
from busquedaensayo import ensayo
from ensayoendiferido import representacion_grafico
from laboratorio_virtual import imagen_360
from datos_continuo import datos_continuo
from puntos_clave import busqueda_puntos_compresor
from puntos_clave import busqueda_puntos_variable
from puntos_clave import busqueda_puntos_control
from puntos_clave import calculos_termodinamicos
from puntos_clave import calculos_termodinamicos_sin_restricciones
from modelotermodinamico import calculo_modelo
from modelotermodinamico import calculo_comparacion
from API import request_login
from API import make_charts_request
from API import process_charts_response
from CHATBOT import chatbot

st.set_page_config(layout="wide")

with st.sidebar:

    menu= option_menu(menu_title=None,  
        options=['Laboratorio Virtual','Datos en Continuo','Datos en Histórico','ChatBot'],
        icons=['bi bi-info-circle', 'bi bi-cloud-arrow-down', 'bi bi-database-down', 'gear','bi bi-chat-dots'],
        default_index=0,
         styles={'container': {'padding': '5px', 'background-color': '#ffffff'},
        'icon': {'color': 'orange', 'font-size': '18px'},
        'nav-link': {'font-size': '16px', 'text-align': 'left', 'margin': '0px'},
        'nav-link-selected': {'background-color': '#03617E'},})

if menu == 'Laboratorio Virtual':

    menu_herramientas = option_menu(
        menu_title=None,  
        options=['Entorno 360','Realidad Virtual','Información'],
        default_index=0,
        orientation='horizontal',
        styles={'container': {'padding': '5px', 'background-color': '#ffffff'},
        'icon': {'color': 'orange', 'font-size': '18px'},
        'nav-link': {'font-size': '16px', 'text-align': 'left', 'margin': '0px'},
        'nav-link-selected': {'background-color': '#03617E'}})
    if menu_herramientas == 'Entorno 360':
        st.components.v1.iframe("vision.kiconex.com", width=2000, height=1000)
        
    if menu_herramientas == 'Realidad Virtual':
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2,col3 = st.columns(3)
        with col1:
            pass
        with col2:
            st.image("visionqr.png", width=390)
        with col3:
            pass
        col1, col2,col3,col4,col5 = st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col3:
            st.markdown("""
            <a href="https://drive.google.com/file/d/1tx1JBfqA62EtiPIAOtWrzowjwX2QHHOV/view?usp=drive_link" target="_blank">
            <button style='padding: 0.6em 1.5em;
                   background-color: #03617E;
                   color: white;
                   border: none;
                   border-radius: 5px;
                   font-size: 17px;
                   font-weight: bold;
                   cursor: pointer;'>
                Descargar Archivo VR
            </button>
            </a>
            """, unsafe_allow_html=True)
        with col4:
            pass
        with col5:
            pass

elif menu == 'Datos en Continuo':
     
    if 'TOKEN' not in st.session_state:
        st.session_state.TOKEN =''

    if not st.session_state.TOKEN: 

        col1, col2 = st.columns(2)
        with col1:
            USERNAME = st.text_input("Usuario")
        with col2:
            PASSWORD = st.text_input("Contraseña", type="password")
    
        if st.button("Entrar"):
            TOKEN = request_login(USERNAME, PASSWORD)
        
            if TOKEN:
                st.session_state.TOKEN = TOKEN
            else: 
                st.error('Error de autenticación')
    
    if st.session_state.TOKEN:
        pass


elif menu == 'Datos en Histórico':

    menu_herramientas = option_menu(
        menu_title=None,  
        options=['Búsqueda de Ensayos','Simulación en Diferido','Estudio de Puntos Clave','Modelo Termodinámico'],
        default_index=0,
        orientation='horizontal',
        styles={'container': {'padding': '5px', 'background-color': '#ffffff'},
        'icon': {'color': 'orange', 'font-size': '18px'},
        'nav-link': {'font-size': '16px', 'text-align': 'left', 'margin': '0px'},
        'nav-link-selected': {'background-color': '#03617E'}})

    if menu_herramientas == 'Búsqueda de Ensayos':

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2,col3 = st.columns(3)
        instalacion='Equipo para cámaras de refrigeración y congelación de CO2 transcrítico (Escuela de Ingeniería Industriales - Universidad de Málaga)'
        with col1:
            fecha_inicio = st.date_input('Fecha de inicio', value=date(2024, 9, 11),min_value=date(2024, 3, 14),max_value=date(2024, 12, 31))
        with col2:
            fecha_fin = st.date_input('Fecha de fin', value=date(2024, 9, 11),min_value=date(2024, 3, 14),max_value=date(2024, 12, 31))
        with col3:
            duracion_minutos = st.number_input('Duración mínima (minutos)',15,300,60)

        if fecha_inicio > fecha_fin:
            st.error('La fecha de fin debe ser mayor o igual que la fecha de inicio')

        if 'lista_ensayos' not in st.session_state:
            st.session_state.lista_ensayos = []

        if st.button('Buscar'):

            with st.spinner('Buscando ensayos ...'):  

                lista_ensayos,intervalos_ensayos,df_analizador_redes,df_equipo,df_evaporador_04,df_valvula_expansion_05,df_evaporador_06,df_valvula_expansion_07=busqueda(instalacion,fecha_inicio,fecha_fin,duracion_minutos)

                if not lista_ensayos:
                    st.error('Ensayos no encontrados')
                else:
                    st.session_state.lista_ensayos = lista_ensayos
                    st.session_state.intervalos_ensayos = intervalos_ensayos
                    st.session_state.df_analizador_redes = df_analizador_redes
                    st.session_state.df_equipo = df_equipo
                    st.session_state.df_evaporador_04 = df_evaporador_04
                    st.session_state.df_valvula_expansion_05 = df_valvula_expansion_05
                    st.session_state.df_evaporador_06 = df_evaporador_06
                    st.session_state.df_valvula_expansion_07 = df_valvula_expansion_07

        if st.session_state.lista_ensayos:

            ensayo_seleccionado = st.selectbox('Ensayos disponibles',st.session_state.lista_ensayos)

            st.session_state.ensayo_seleccionado = ensayo_seleccionado
            ensayo_elegido=None

            col1, col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14 = st.columns(14)
            with col1:

                if st.button('Cargar'):

                    df_analizador_redes_ensayo,df_equipo_ensayo,df_evaporador_04_ensayo,df_valvula_expansion_05_ensayo,df_evaporador_06_ensayo,df_valvula_expansion_07_ensayo=ensayo(st.session_state.ensayo_seleccionado,st.session_state.lista_ensayos,st.session_state.intervalos_ensayos,st.session_state.df_analizador_redes,st.session_state.df_equipo,st.session_state.df_evaporador_04,st.session_state.df_valvula_expansion_05,st.session_state.df_evaporador_06,st.session_state.df_valvula_expansion_07)
                    st.session_state.df_analizador_redes_ensayo = df_analizador_redes_ensayo
                    st.session_state.df_equipo_ensayo = df_equipo_ensayo
                    st.session_state.df_evaporador_04_ensayo = df_evaporador_04_ensayo
                    st.session_state.df_valvula_expansion_05_ensayo = df_valvula_expansion_05_ensayo
                    st.session_state.df_evaporador_06_ensayo = df_evaporador_06_ensayo
                    st.session_state.df_valvula_expansion_07_ensayo = df_valvula_expansion_07_ensayo

                    data_ensayo=pd.concat([st.session_state.df_equipo_ensayo,st.session_state.df_analizador_redes_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo],axis=1)
                    csv_ensayo=data_ensayo.to_csv().encode("utf-8")
                    st.session_state.csv_ensayo=csv_ensayo

                    ensayo_elegido=ensayo_seleccionado
                    st.session_state.ensayo_elegido=ensayo_elegido

            with col2:
                if 'csv_ensayo' in st.session_state:
                 st.download_button(
                     label="",
                     data=st.session_state.csv_ensayo,
                     file_name="Ensayo_CO2_Transcritico_Malaga_Opentropy.csv",
                     mime="text/csv",
                     icon=":material/download:",
                     )
                else:
                           pass
            with col3:
                pass
            with col4:
                pass
            with col5:
                pass
            with col6:
                pass
            with col7:
                pass
            with col8:
                pass
            with col9:
                pass
            with col10:
                pass
            with col11:
                pass
            with col12:
                pass
            with col13:
                pass
            with col14:
                pass
            if 'df_equipo_ensayo' in st.session_state:
                st.success(f'Datos cargados: {st.session_state.ensayo_elegido}')

    if menu_herramientas == 'Simulación en Diferido':

        if "df_equipo_ensayo" in st.session_state and st.session_state.df_equipo_ensayo is not None:

            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                tipo_grafico_diferido = st.multiselect('Tipo de gráfico',['Scada','Gráfico de líneas','Tabla'],default=['Gráfico de líneas','Scada'])
            with col2:
                velocidad_reproduccion = st.number_input('Velocidad de reproducción (segundos)',0.1,10.0,1.0)

            with st.expander('Configuración'):

                col3, col4 = st.columns(2)
                with col3: 
                    variables_evaporador_04_diferido= st.multiselect('Evaporador 1',st.session_state.df_evaporador_04_ensayo.columns.tolist(),default='Temperatura camara (evaporador 1) (°C)')
                with col4:
                    variables_valvula_expansion_05_diferido = st.multiselect('Válvula expansion 1',st.session_state.df_valvula_expansion_05_ensayo.columns.tolist())

                col5, col6 = st.columns(2)
                with col5:
                    variables_evaporador_06_diferido = st.multiselect('Evaporador 2',st.session_state.df_evaporador_06_ensayo.columns.tolist())
                with col6:
                    variables_valvula_expansion_07_diferido = st.multiselect('Válvula expansion 2',st.session_state.df_valvula_expansion_07_ensayo.columns.tolist())

                col7, col8= st.columns(2)
                with col7:
                    variables_equipo_diferido = st.multiselect('Central transcrítica y gas-cooler',st.session_state.df_equipo_ensayo.columns.tolist(),default=['Temperatura evaporacion (°C)','Temperatura salida gas cooler (°C)','Temperatura deposito (°C)','Temperatura exterior (°C)','Rele compresor (on/off)','Temperatura descarga (°C)'])  
                with col8:
                    variables_analizador_redes_diferido = st.multiselect('Analizador de redes',st.session_state.df_analizador_redes_ensayo.columns.tolist())
        
                col9, col10= st.columns(2)
                with col9:
                    indicadores_termodinamicos = st.multiselect('Indicadores termodinámicos',['COP','Diagramas P-H y T-S','Potencias del ciclo','Rendimientos del compresor','Caracterización de los evaporadores y gas-cooler'])
                with col10:
                    col11, col12= st.columns(2)
                    with col11:
                        variables_ciclo = st.multiselect('Puntos del ciclo',['1','2','3','4s','4','5','6s','6','7','8','9','10','11','12','13','14'])
                    with col12:
                        propiedades_ciclo = st.multiselect('Propiedades',['Temperatura (°C)','Presión (bar)','Entalpía (kJ/Kg)','Entropía (kJ/Kg·K)','Título de vapor','Densidad (Kg/m^3)','Caudal másico (Kg/s)'])

                lista_variables_diferido=variables_analizador_redes_diferido+variables_evaporador_04_diferido+variables_valvula_expansion_05_diferido+variables_evaporador_06_diferido+variables_valvula_expansion_07_diferido+variables_equipo_diferido

            if st.button('Simular'):

                if not tipo_grafico_diferido or (not lista_variables_diferido and not indicadores_termodinamicos and not variables_ciclo):
                    st.warning('Selecciona al menos una variable y un tipo de gráfico')

                else:
                    representacion_grafico(propiedades_ciclo,variables_ciclo,indicadores_termodinamicos,velocidad_reproduccion,tipo_grafico_diferido,lista_variables_diferido,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)            
                        
        else:
            st.warning("No se ha cargado un ensayo")

    if menu_herramientas == 'Estudio de Puntos Clave':

        if "df_equipo_ensayo" in st.session_state and st.session_state.df_equipo_ensayo is not None:

            st.markdown("<br>", unsafe_allow_html=True)

            tipos_puntos=[]
            col1, col2 = st.columns(2)
            with col1:
                puntos = st.selectbox('Tipos de puntos',['Cuasi-estacionarios','Sin restricciones'],index=1)
                st.session_state.tipos_puntos=puntos
                
            with col2:
                if puntos=='Cuasi-estacionarios':
                    metodo_busqueda = st.selectbox('Métodos de búsqueda',['Últimos puntos activos del compresor','Variable comprendida en banda','Control combinado'],index=0)

                elif puntos=='Sin restricciones':
                
                    puntos_encontrados_sin_restricciones=list()
                    lista_puntos_sin_restricciones=list()

                    for i,hora in enumerate(st.session_state.df_equipo_ensayo.index):
                        puntos_encontrados_sin_restricciones.append((hora,hora))
                        lista_puntos_sin_restricciones.append(f'Punto {i+1} - {hora.strftime('%H:%M')}')

                    st.session_state.puntos_encontrados_sin_restricciones=puntos_encontrados_sin_restricciones
                    st.session_state.lista_puntos_sin_restricciones=lista_puntos_sin_restricciones
                    punto_seleccionado_sin_restricciones=st.selectbox('Puntos disponibles',st.session_state.lista_puntos_sin_restricciones,index=14) 
                    st.session_state.punto_seleccionado_sin_restricciones=punto_seleccionado_sin_restricciones

            if puntos=='Cuasi-estacionarios':
  
                with st.expander('Configuración'):

                    if metodo_busqueda=='Últimos puntos activos del compresor':
                        puntos_compresor=st.number_input('Últimos puntos activo',1,4,3)

                    elif metodo_busqueda=='Variable comprendida en banda':
                        variables_disponibles=st.session_state.df_analizador_redes_ensayo.columns.tolist()+st.session_state.df_evaporador_04_ensayo.columns.tolist()+st.session_state.df_valvula_expansion_05_ensayo.columns.tolist()+st.session_state.df_evaporador_06_ensayo.columns.tolist()+st.session_state.df_valvula_expansion_07_ensayo.columns.tolist()+st.session_state.df_equipo_ensayo.columns.tolist()

                        variable_banda = st.selectbox('Variable',variables_disponibles,index=variables_disponibles.index("Temperatura camara (evaporador 1) (°C)"))

                        col3,col4, col5 = st.columns(3)
                        with col3:
                            consigna=st.number_input('Consigna',-100.0,100.0,0-15.0)
                        with col4:
                            banda_superior=st.number_input('Banda superior',0.0,10.0,0.5)
                        with col5:                 
                            banda_inferior=st.number_input('Banda inferior',0.0,10.0,0.5)

                    elif metodo_busqueda=='Control combinado':
                        col3,col4, col5 = st.columns(3)
                        with col3:
                            consigna_temperatura_camara=st.number_input('Consigna de la temperatura de cámara',-50.0,50.0,-15.0)
                        with col4:
                            banda_superior_temperatura_camara=st.number_input('Banda superior de la temperatura de cámara',0.0,10.0,0.5)
                        with col5:                 
                            banda_inferior_temperatura_camara=st.number_input('Banda inferior de la temperatura de cámara',0.0,10.0,0.5)

                        col6,col7, col8 = st.columns(3)
                        with col6:
                            consigna_temperatura=st.number_input('Consigna de la temperatura de evaporación',-50.0,50.0,-30.0)
                        with col7:
                            banda_superior_temperatura=st.number_input('Banda superior de la temperatura de evaporación',-0.0,10.0,0.5)
                        with col8:                 
                            banda_inferior_temperatura=st.number_input('Banda inferior de la temperatura de evaporación',0.0,10.0,0.5)

                        col9,col10, col11 = st.columns(3)
                        with col9:
                            subrenfriamiento=st.number_input('Consigna de salto térmico en gas-cooler',0.0,50.0,5.0)
                        with col10:
                            sobrecalentamiento=st.number_input('Consigna de salto térmico en evaporador',0.0,20.0,10.0)
                        with col11:                 
                            apertura_valvula=st.number_input('Apertura de la válvula by-pass',0.0,100.0,0.0)

                if metodo_busqueda=='Últimos puntos activos del compresor':
                    if 'puntos_encontrados' not in st.session_state:
                        st.session_state.puntos_encontrados = []
                    if st.button('Buscar'):
                        lista_estacionarios,puntos_encontrados=busqueda_puntos_compresor(puntos_compresor,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

                        if not lista_estacionarios:
                            st.error('Cuasi-estacionarios no encontrados')
                        else:
                            st.session_state.puntos_compresor=puntos_compresor
                            st.session_state.lista_estacionarios=lista_estacionarios
                            puntos_encontrados_copia=puntos_encontrados.copy()
                            puntos_encontrados=list()
                            for hora in puntos_encontrados_copia:
                                nuevo_instante=hora -timedelta(minutes=puntos_compresor-1)
                                puntos_encontrados.append((nuevo_instante,hora))
                            st.session_state.puntos_encontrados=puntos_encontrados

                    if st.session_state.puntos_encontrados:
                        punto_compresor_seleccionado=st.selectbox('Cuasi-estacionarios disponibles',st.session_state.lista_estacionarios)
                        st.session_state.punto_compresor_seleccionado=punto_compresor_seleccionado

                        if st.button('Calcular'):
                            calculos_termodinamicos(st.session_state.punto_compresor_seleccionado,st.session_state.lista_estacionarios,st.session_state.puntos_encontrados,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

                if metodo_busqueda=='Variable comprendida en banda':
                    if 'puntos_encontrados_variable' not in st.session_state:
                        st.session_state.puntos_encontrados_variable = []
                    if st.button('Buscar'):
                        lista_estacionarios_variable,puntos_encontrados_variable=busqueda_puntos_variable(variable_banda,consigna,banda_superior,banda_inferior,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

                        if not lista_estacionarios_variable:
                            st.error('Cuasi-estacionarios no encontrados')
                        else:
                            st.session_state.lista_estacionarios_variable=lista_estacionarios_variable
                            st.session_state.puntos_encontrados_variable=puntos_encontrados_variable

                    if st.session_state.puntos_encontrados_variable:
                        punto_variable_seleccionado=st.selectbox('Cuasi-estacionarios disponibles',st.session_state.lista_estacionarios_variable)
                        st.session_state.punto_variable_seleccionado=punto_variable_seleccionado

                        if st.button('Calcular'):
                            calculos_termodinamicos(st.session_state.punto_variable_seleccionado,st.session_state.lista_estacionarios_variable,st.session_state.puntos_encontrados_variable,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

                if metodo_busqueda=='Control combinado':
                    if 'puntos_encontrados_control' not in st.session_state:
                        st.session_state.puntos_encontrados_control = []
                    if st.button('Buscar'):
                        lista_estacionarios_control,puntos_encontrados_control=busqueda_puntos_control(consigna_temperatura_camara,banda_superior_temperatura_camara,banda_inferior_temperatura_camara,consigna_temperatura,banda_superior_temperatura,banda_inferior_temperatura,subrenfriamiento,sobrecalentamiento,apertura_valvula,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

                        if not lista_estacionarios_control:
                            st.error('Cuasi-estacionarios no encontrados')
                        else:
                            st.session_state.lista_estacionarios_control=lista_estacionarios_control
                            st.session_state.puntos_encontrados_control=puntos_encontrados_control

                    if st.session_state.puntos_encontrados_control:
                        punto_control_seleccionado=st.selectbox('Cuasi-estacionarios disponibles',st.session_state.lista_estacionarios_control)
                        st.session_state.punto_control_seleccionado=punto_control_seleccionado

                        if st.button('Calcular'):
                            calculos_termodinamicos(st.session_state.punto_control_seleccionado,st.session_state.lista_estacionarios_control,st.session_state.puntos_encontrados_control,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

            elif puntos=='Sin restricciones':
                if st.session_state.puntos_encontrados_sin_restricciones:
                    if st.button('Calcular'):
                        calculos_termodinamicos_sin_restricciones(st.session_state.punto_seleccionado_sin_restricciones,st.session_state.lista_puntos_sin_restricciones,st.session_state.puntos_encontrados_sin_restricciones,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

        else:
            st.warning('No se ha cargado un ensayo')


    if menu_herramientas == 'Modelo Termodinámico':
        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander('Configuración'):

            col1,col2= st.columns(2)
            with col1:
                temperatura_evaporacion=st.number_input('Temperatura de evaporación (°C)',-60.0,20.0,-30.0)
            with col2:
                temperatura_ambiente=st.number_input('Temperatura ambiente (°C)',-10.0,40.0,28.0)

            col3,col4= st.columns(2)
            with col3:
                salto_evaporador=st.number_input('Salto térmico en evaporador (K)',0.0,20.0,10.0)
            with col4:
                salto_gascooler=st.number_input('Salto térmico en gas-cooler (K)',0.0,20.0,3.0)

            velocidad_compresor=st.number_input('Velocidad de giro del compresor (rev/s)',0.0,80.0,56.0)


        if st.button('Calcular'):
            tabla_propiedades,tabla_propiedades_resumen=calculo_modelo(temperatura_evaporacion,salto_evaporador,temperatura_ambiente,salto_gascooler,velocidad_compresor)
            st.session_state.tabla_propiedades=tabla_propiedades
            st.session_state.tabla_propiedades_resumen=tabla_propiedades_resumen

            if "df_equipo_ensayo" in st.session_state and st.session_state.df_equipo_ensayo is not None:
                calculo_comparacion(temperatura_evaporacion,salto_evaporador,temperatura_ambiente,salto_gascooler,velocidad_compresor,st.session_state.tabla_propiedades,st.session_state.tabla_propiedades_resumen,st.session_state.df_analizador_redes_ensayo,st.session_state.df_equipo_ensayo,st.session_state.df_evaporador_04_ensayo,st.session_state.df_valvula_expansion_05_ensayo,st.session_state.df_evaporador_06_ensayo,st.session_state.df_valvula_expansion_07_ensayo)

elif menu == 'ChatBot':
    chatbot()
