import streamlit as st
from scripts import utils
import json
import pickle
import pandas as pd
import numpy as np
from scripts.modelsclasses import Model_1, Model_2, Total_Revenue_Regressor

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'Model_1':
            from scripts.modelsclasses import Model_1
            return Model_1
        if name == 'Model_2':
            from scripts.modelsclasses import Model_2
            return Model_2
        if name == 'Total_Revenue_Regressor':
            from scripts.modelsclasses import Total_Revenue_Regressor
            return Total_Revenue_Regressor
        if name == 'Client_Clusterer':
            from scripts.modelsclasses import Client_Clusterer
            return Client_Clusterer
        return super().find_class(module, name)

class DemoPage():
    def __init__(self) -> None:
        self.data = pd.read_csv("./assets/data/dataset.csv")

        with open("appconfig.json", "r") as f:
            self.config = json.load(f)

        self.modelo_1 = CustomUnpickler(open('./assets/models/Modelo_1.pkl', 'rb')).load()
        self.modelo_2 = CustomUnpickler(open('./assets/models/Modelo_2.pkl', 'rb')).load()
        self.modelo_3 = CustomUnpickler(open('./assets/models/Modelo_3.pkl', 'rb')).load()
        self.modelo_4 = CustomUnpickler(open('./assets/models/Modelo_4.pkl', 'rb')).load()
        
        #hago estas correciones porque tenia errores en la parte de limpieza de nulos en las clases, 
        #basicamente uso las clases de modelsclasses.py
        #que estan adaptadas para que funcionen en la app
        self.modelo_1 = Model_1(self.modelo_1.pipeline, self.modelo_1.model)
        self.modelo_2 = Model_2(self.modelo_2.pipeline, self.modelo_2.model)
        self.modelo_3 = Total_Revenue_Regressor(self.modelo_3.pipe, self.modelo_3.model)

        self.display_page()
   
    def display_page(self):
        st.title("Aplicación del modelo")
        st.info("El modelo esta aplicado en una base de datos de sqllite con flask como api.\n>\nPuedes probarlo en la  [Notebook](https://colab.research.google.com/drive/1roIA3LR2fZoZzlAq2NSs2g5gWIRLzFKI)")
        st.markdown("## Predice tu usuario desde aqui")
        
        cols = st.columns(5, gap="small")

        #=====Carga de datos=======

        #-----Datos irrelevantes que se dropean pero que necesitan estar, No los maneja el usuario--------
        customer_id = self.data['Customer ID'].iloc[0]
        customer_status = self.data['Customer Status'].iloc[0]
        churn_category = self.data['Churn Category'].iloc[0]
        churn_reason = self.data['Churn Reason'].iloc[0]
        county = self.data['County'].iloc[0]

        #-----Datos que imputa el usuario------
        with cols[0]:
            gender = st.selectbox('Gender', self.data['Gender'].unique())
            city = st.selectbox('City', self.data['City'].unique())
            contract = st.selectbox('Contract', self.data['Contract'].unique())
            total_refunds = st.number_input('Total Refunds', min_value=self.data['Total Refunds'].min(), max_value=self.data['Total Refunds'].max())
            married = st.selectbox('Married', ['Yes','No'])
            online_backup = st.selectbox('Online Backup', ['Yes','No'])
            streaming_music = st.selectbox('Streaming Music', ['Yes','No'])

        with cols[1]:
            age = st.number_input('Age', min_value=self.data['Age'].min(), max_value=self.data['Age'].max())
            zip_code = st.selectbox('Zip Code', self.data['Zip Code'].unique())
            internet_type = st.selectbox('Internet Type', ['Cable', 'Fiber Optic', 'DSL'])
            total_revenue = st.number_input('Total Revenue', min_value=self.data['Total Revenue'].min(), max_value=self.data['Total Revenue'].max())
            phone_service = st.selectbox('Phone Service', ['Yes','No'])
            divice_protection_plan = st.selectbox('Device Protection Plan', ['Yes','No'])
            unlimited_data = st.selectbox('Unlimited Data', ['Yes','No'])

        with cols[2]:
            n_dependants = st.number_input('Number of Dependents', min_value=self.data['Number of Dependents'].min(), max_value=self.data['Number of Dependents'].max())
            n_referals = st.number_input('Number of Referrals', min_value=self.data['Number of Referrals'].min(), max_value=self.data['Number of Referrals'].max())
            monthly_charge = st.number_input('Monthly Charge', min_value=0., max_value=self.data['Monthly Charge'].max())
            total_long_distance_charges = st.number_input('Total Long Distance Charges', min_value=self.data['Total Long Distance Charges'].min(), max_value=self.data['Total Long Distance Charges'].max())
            multiple_lines = st.selectbox('Multiple Lines', ['Yes','No'])
            premium_tech_suport = st.selectbox('Premium Tech Support', ['Yes','No'])
            paperless_billing = st.selectbox('Paperless Billing', ['Yes','No'])
            
        with cols[3]:
            latitude = st.number_input('Latitude', min_value=self.data['Latitude'].min(), max_value=self.data['Latitude'].max())
            longitude = st.number_input('Longitude', min_value=self.data['Longitude'].min(), max_value=self.data['Longitude'].max())
            total_charges = st.number_input('Total Charges', min_value=self.data['Total Charges'].min(), max_value=self.data['Total Charges'].max())
            total_extra_data_charges = st.number_input('Total Extra Data Charges', min_value=self.data['Total Extra Data Charges'].min(), max_value=self.data['Total Extra Data Charges'].max())
            internet_service = st.selectbox('Internet Service', ['Yes','No'])
            streaming_tv = st.selectbox('Streaming TV', ['Yes','No'])
            avg_monthly_long_distance_charges = st.number_input('Avg Monthly Long Distance Charges', min_value=self.data['Avg Monthly Long Distance Charges'].min(), max_value=self.data['Avg Monthly Long Distance Charges'].max())

        with cols[4]:
            offer = st.selectbox('Offer', self.data['Offer'].unique())
            tenure = st.number_input('Tenure in Months', min_value=self.data['Tenure in Months'].min(), max_value=self.data['Tenure in Months'].max())
            payment_method = st.selectbox('Payment Method', self.data['Payment Method'].unique())
            avg_gb_download = st.number_input('Avg Monthly GB Download', min_value=self.data['Avg Monthly GB Download'].min(), max_value=self.data['Avg Monthly GB Download'].max())
            online_security = st.selectbox('Online Security', ['Yes','No'])
            streaming_movies = st.selectbox('Streaming Movies', ['Yes','No'])

        input_dict = {
            "customer_id": [customer_id],
            "gender": [gender],
            "age": [age],
            "married": [married],
            "number_of_dependents": [n_dependants],
            "city": [city],
            "zip_code": [zip_code],
            "latitude": [latitude],
            "longitude": [longitude],
            "number_of_referrals": [n_referals],
            "tenure_in_months": [tenure],
            "offer": [offer],
            "phone_service": [phone_service],
            "avg_monthly_long_distance_charges": [avg_monthly_long_distance_charges],
            "multiple_lines": [multiple_lines],
            "internet_service": [internet_service],
            "internet_type": [internet_type],
            "avg_monthly_gb_download": [avg_gb_download],
            "online_security": [online_security],
            "online_backup": [online_backup],
            "device_protection_plan": [divice_protection_plan],
            "premium_tech_support": [premium_tech_suport],
            "streaming_tv": [streaming_tv],
            "streaming_movies": [streaming_movies],
            "streaming_music": [streaming_music],
            "unlimited_data": [unlimited_data],
            "contract": [contract],
            "paperless_billing": [paperless_billing],
            "payment_method": [payment_method],
            "monthly_charge": [monthly_charge],
            "total_charges": [total_charges],
            "total_refunds": [total_refunds],
            "total_extra_data_charges": [total_extra_data_charges],
            "total_long_distance_charges": [total_long_distance_charges],
            "total_revenue": [total_revenue],
            "customer_status": [customer_status],
            "churn_category": [churn_category],
            "churn_reason": [churn_reason],
        }

        def get_predicts():
            df_input = pd.DataFrame(input_dict)

            st.markdown('## Predicciones')
            model_1_predict = self.modelo_1.predict(df_input)['churn_chance'].iloc[0]
            model_2_predict = self.modelo_2.predict(df_input)
            model_3_predict = self.modelo_3.predict(df_input)[0]
            model_4_predict = self.modelo_4.predict(df_input)[0]
            st.markdown(f'### **Modelo 1 (Chance de churnear): {round(model_1_predict,2)}%**')
            st.markdown(f'### **Modelo 2 (% Razones posibles de churn):**')
            st.dataframe(model_2_predict)
            st.markdown(f'### **Modelo 3 (% Revenue esperada para el usuario en el cuatrimestre): ${round(model_3_predict,2)}**')
            st.markdown(f'### **Modelo 4 (grupo al que pertenece el usuario): {model_4_predict}**')

        if st.button('Predict'):
            get_predicts()