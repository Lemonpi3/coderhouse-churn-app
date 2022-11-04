from distutils.command.config import config
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from scripts import utils
import json
import numpy as np
import pandas as pd
import textwrap
import warnings
from mpl_toolkits.basemap import Basemap

class DataInfo:
    def __init__(self) -> None:
        warnings.filterwarnings("ignore", category=FutureWarning) #ignorar unos carteles de pandas.
        pd.set_option('display.max_columns', None)

        self.data = pd.read_csv("./assets/data/dataset.csv")

        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']
        self.cat_colors = config['cat_palette']

        self.page_txt = {
            'EN':{
                'page_header':'Data Info\n---------',
                'dataset_source':'WIP',
                'types_of_client':'WIP',
                'client_frequency':'WIP',
                'unique_title':'WIP',
                'unique_txt':'WIP',
                'null_amount':'WIP',
                'column_info':'WIP',
            },
            'ES':{
                'page_header':'Información de la Data\n---------',
                'dataset_source':'''
                    La data proviene de una compania de telecomunicaciones en California en el
                    Q2 2022.

                    El dataset fue sacado de [kaggle]("https://www.kaggle.com/datasets/shilongzhuang/telecom-customer-churn-by-maven-analytics").
                    >
                    La columna County fue creada apartir de la data proveniente de [geographic.org]("https://geographic.org/streetview/usa/ca/") con el fin de segmentar los churned en regiones mas grandes.
                    ''',
                'types_of_client':'''
                    #### Hay 3 tipos de clientes en el dataset:
                    * **Stayed**:  Son los usuarios que se quedan en el servicio.
                    * **Joined**:  Son los usuarios nuevos al servicio que se sumaron este cuatrimestre.
                    * **Churned**: Son los usuarios que dejaron el servicio en este cuatrimestre.''',
                'client_frequency':"### Frecuencia de cada tipo usuario en el dataset",
                'unique_title':"### Cantidad de usuarios unicos y forma del dataset",
                'unique_txt':'* **Clientes Unicos: {}**\n* **Shape: {}**',
                'null_amount':"### Cantidad de nulos en el dataset",
                'column_info':"""
                    ### Info de cada columna
                    * **Customer Status:** Si el cliente sigue en el servicio, se unió o lo dejó (churned)
                    * **Churn Category:** La categoria del porque lo dejo (por ejemplo: Dissatisfaction, Competitor, etc). Es la mas importante de las 2 columnas.
                    * **Churn Reason:** La razon especifica del cliente de por que dejo el servicio.
                    * **Gender, Age, Married, Number of Dependents:** Datos personales de como es la persona , si esta casada o no y con cuanta gente vive.
                    * **City, Zip Code, Latitude, Longitude, County:** En que parte del estado vive el cliente.
                    * **Number of Referrals, Tenure in Months:** A cuanta gente le recomendo el servicio y cuantos meses lleva con el servicio (tenure)
                    * **Offer, Phone Service, Multiple Lines, Avg Monthly Long Distance Charges:** El plan que el cliente esta usando , si opto por usar el servicio telefonico en su casa, si tiene multiples lineas telefónicas y el gasto mensual promedio en llamadas a larga distancia (si el cliente no esta subscripto al servicio telefonico el valor es 0)
                    * **Internet Service, Internet Type, Avg Monthly GB Download:** Datos relacionados al servicio del internet, si no contrató el servicio de internet el tipo de internet  esta como nulo y los GBs promedio tendran un valor igual a 0.
                    * **Online Security, Online Backup, Device Protection Plan, Premium Tech Support, Streaming TV, Streaming Movies, Streaming Music, Unlimited Data:** Indican si optaron o no por cada uno de esos servicios.
                    * **Contract, Paperless Billing, Payment Method, Monthly Charge:** La forma y metodo de pago que eligio el cliente y cuanto se le cobra mensualmente.
                    * **Total Charges, Total Refunds, Total Extra Data Charges, Total Long Distance Charges, Total Revenue:** Gastos y reembolsos totales. Total revenue indica cuanto gano la empresa con este cliente.
                    """,
            },
        }
        self.display_page()
        
    def display_page(self):
        st.header(self.page_txt[self.lang]['page_header'])
        st.write(self.page_txt[self.lang]['dataset_source'])
        st.write(self.page_txt[self.lang]['types_of_client'])

        st.write(self.page_txt[self.lang]['client_frequency'])
        temp_df = pd.concat([self.data['Customer Status'].value_counts().to_frame('Cantidad absoluta'),
                        (self.data['Customer Status'].value_counts(normalize=True)*100).to_frame('Cantidad porcentual')], 
                        axis=1).style.format({'Cantidad porcentual': '{:.2f}%'})
        cols = st.columns(3, gap="small")
        with cols[0]:                
            fig, ax = plt.subplots(figsize=(3,3))
            utils.wheel_chart(self.data['Customer Status'], ax, [self.cat_colors[0],self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': 7 })
            st.pyplot(fig.patch.set_alpha(0.0))
        st.dataframe(temp_df)

        st.write(self.page_txt[self.lang]['unique_title'])
        unicos = self.data['Customer ID'].nunique()
        st.write(self.page_txt[self.lang]['unique_txt'].format(unicos,self.data.shape))
        

        st.write(self.page_txt[self.lang]['null_amount'])
        temp_df = pd.concat([self.data.isna().sum().to_frame('cantidad de nulos absoluta'),
                            (self.data.isna().sum() / len(self.data) * 100).to_frame('cantidad de nulos porcentual'),
                            self.data.dtypes.to_frame('tipo de variable')], axis=1).style.format({'cantidad de nulos porcentual': '{:.2f}%'})
        st.dataframe(temp_df)

        st.write(self.page_txt[self.lang]['column_info'])
        st.dataframe(self.data.head())

class StoryTelling:
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']
        self.cat_colors = config['cat_palette']
        self.div_colors = config['div_palette']
        self.data = pd.read_csv("./assets/data/dataset.csv")

        self.page_txt = {
            'EN':{
                
            },
            'ES':{
                'intro_title':'Introducción',
                'comercial_ctx':'''
                    En el area de telecomunicaciones, la rotación de los clientes que contratan y dejan los servicios es bastante comun y frecuente.
                    Las razones de porque dejan los servicios pueden tener diferentes motivos, pero se pueden dividir en 2 grandes grupos: **Evitables** e **Inevitables**.
                    >
                    #### Ahora, ¿que tipos de razones son evitables y cuales son inevitables?
                    Las razones inevitables son aquellas de las cuales la empresa no tiene control y/o culpa como, por ejemplo, cuando un cliente se muda o fallece.
                    >
                    Por otro lado las razones evitables son aquellas que tienen que ver con la calidad del servicio, la atencion que recibio el cliente e incluso la poca competitividad de la empresa comparada con otras del area.
                    >
                    #### Entonces, ¿que es lo que buscamos como empresa para crecer?
                    Lo que se busca como empresa es minimizar la cantidad de clientes que dejan aumentando la retención de los clientes, asi como tambien atraer a una mayor cantidad de clientes.
                    Los valores normales de churned tienen que estar por debajo de los que se unen ya que para que la empresa crezca la cantidad de clientes debe crecer.
                    ''',
                'comercial_problem_title':'#### Lo que nos lleva al problema comercial que tiene la empresa.',
                'user_dist_title':'Distribución de cada grupo de usuario',
                'user_dist_description':'Como se puede ver en el gráfico,en este ultimo cuatrimestre, tenemos muchos mas usuarios que dejaron el servicio que los que se unieron. Lo cual significa que la empresa esta perdiendo clientes y por ende mucho dinero.',
                'revenue_title':'### ¿Pero, Cuánto dinero representan estos usuarios churned?',
                'revenue_report':"""
                    El total de ganancias de este cuatrimestre fue de 
                    <font color='lime'>\$21371131.69</font>
                    pero las ganancias provenientes de los usuarios que dejaron el servicio fueron de 
                    <font color='red'>\$3684459.82</font> que representan
                    <font color='red'>17.24%</font> del total.
                    """,
                'revenue_graph_labels':['Ganancias de Usuarios\n Retenidos + Nuevos','Ganancias de los \nusuarios Perdidos'],
            }
        }
        self.display_page()

    def display_page(self):
        st.header('Storytelling \n--------------')
        st.title(self.page_txt[self.lang]['intro_title'])
        st.write(self.page_txt[self.lang]['comercial_ctx'])
        st.write(self.page_txt[self.lang]['comercial_problem_title'])
        temp_df = pd.concat([self.data['Customer Status'].value_counts().to_frame('Cantidad absoluta'),
                        (self.data['Customer Status'].value_counts(normalize=True)*100).to_frame('Cantidad porcentual')], 
                        axis=1).style.format({'Cantidad porcentual': '{:.2f}%'})
        cols = st.columns(3, gap="small")
        with cols[0]:                
            fig, ax = plt.subplots(figsize=(3,3))
            utils.wheel_chart(self.data['Customer Status'], ax, [self.cat_colors[0],self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': 7 })
            ax.set_title(self.page_txt[self.lang]['user_dist_title'],fontdict={ 'color': 'w','weight': 'bold','size': 10 })
            fig.patch.set_alpha(0.0)
            st.pyplot()
        with cols[1]:
            st.dataframe(temp_df)
            st.write(self.page_txt[self.lang]['user_dist_description'])
        
        st.write(self.page_txt[self.lang]['revenue_title'])
        cols = st.columns(2, gap="small")
        with cols[0]:
            st.markdown(self.page_txt[self.lang]['revenue_report'],unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8,8))

            temp_df = pd.Series([round((21371131.69-3684459.82)/21371131.69*100,2),round(3684459.82/21371131.69*100,2)])
            text_labels = self.page_txt[self.lang]['revenue_graph_labels']
            labels = [text_labels[i] + f'\n{g}%'for i,g in enumerate(temp_df)]
            ax.pie(temp_df,labels=labels, radius=1,colors = [self.cat_colors[1],self.cat_colors[-1]],
                    wedgeprops=dict(width=0.3),textprops={'color': 'w','weight': 'bold','size': 15 })
            fig.patch.set_alpha(0.0)
            st.pyplot()
        st.markdown('## Visto esto, ¿Qué esta causando y Donde estan ocurriendo la perdida de usuarios?')
        cols = st.columns(2, gap="small")
        with cols[1]:
            items = ['All'] + list(self.data[self.data['Customer Status']=='Churned']['Churn Category'].unique())
            motivo = st.selectbox('Categoria de Churn',items)
            colors = [  self.div_colors[0], self.div_colors[0], self.div_colors[0], self.div_colors[1], self.div_colors[1], 
                        self.div_colors[1], self.div_colors[2], self.div_colors[2], self.div_colors[2], self.div_colors[3],
                        self.div_colors[3], self.div_colors[3], self.div_colors[4], self.div_colors[4], self.div_colors[4],]
            if motivo != 'All':
                utils.top_15_ciudad_county_percent(self.data[(self.data['Customer Status']=='Churned') & (self.data['Churn Category']==motivo)],
                    title_city='Top 15 ciudades con mas churned',title_county='Top 15 condados con mas churned',figsize=(4,6.1),
                    fontdict={ 'color': 'white','weight': 'bold','size': 7},colors=colors)
            else:
                utils.top_15_ciudad_county_percent(self.data[(self.data['Customer Status']=='Churned')],
                    title_city='Top 15 ciudades con mas churned', title_county='Top 15 condados con mas churned',figsize=(4,6.1),
                    fontdict={ 'color': 'white','weight': 'bold','size': 7},colors=colors)
            st.pyplot()

        with cols[0]:
            fig, ax = plt.subplots(figsize=(8,8))
            if motivo != 'All':
                utils.plot_scatter_map(self.data[(self.data['Customer Status']=='Churned') & (self.data['Churn Category']==motivo)],title="Distribución espacial de los churned",alpha=0.2,
                                    ax = ax,dot_color=self.cat_colors[-1],land_color=self.div_colors[4],water_col=self.cat_colors[4])
            else:
                utils.plot_scatter_map(self.data[(self.data['Customer Status']=='Churned')],title="Distribución espacial de los churned",alpha=0.2,
                                    ax = ax,dot_color=self.cat_colors[-1],land_color=self.div_colors[4],water_col=self.cat_colors[4])
            fig.patch.set_alpha(0.0)
            st.pyplot()
        
        