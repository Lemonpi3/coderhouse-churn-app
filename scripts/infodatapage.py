import matplotlib.pyplot as plt
import streamlit as st
from scripts import utils
import json
import pandas as pd
import warnings

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