from datetime import datetime, timedelta,date         
import pandas as pd
import numpy as np
import streamlit as st
from time import sleep
import streamlit-option-menu
from streamlit-option-menu import option_menu
import plotly.express as px


st.set_page_config(layout="wide")

with st.sidebar:

    menu= option_menu(menu_title=None,  
        options=['Laboratorio Virtual','Datos en Continuo','Datos en Histórico','Simulador Inteligente','ChatBot'],
        icons=['bi bi-info-circle', 'bi bi-cloud-arrow-down', 'bi bi-database-down', 'gear','bi bi-chat-dots'],
        default_index=0,
         styles={'container': {'padding': '5px', 'background-color': '#ffffff'},
        'icon': {'color': 'orange', 'font-size': '18px'},
        'nav-link': {'font-size': '16px', 'text-align': 'left', 'margin': '0px'},
        'nav-link-selected': {'background-color': '#03617E'},})
    
if menu == 'Laboratorio Virtual':
    st.warning('Proximamente')
elif menu == 'Datos en Continuo':
    st.warning('Proximamente')

elif menu == 'Datos en Histórico':

    st.warning('Proximamente')
elif menu == 'Simulador Inteligente':

    st.warning('Proximamente')

elif menu == 'ChatBot':

    st.warning('Proximamente')
