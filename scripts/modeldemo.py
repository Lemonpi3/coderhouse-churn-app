import streamlit as st
from scripts import utils
import json
import pickle
import pandas as pd

class DemoPage():
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            self.config = json.load(f)
        # self.data = pd.read_csv("./assets/data/dataset.csv")

        # with open("./assets/models/modelo_1.pkl", "rb") as f:
        #     self.modelo_1 = pickle.load(f)

        # with open("./assets/models/modelo_2.pkl", "rb") as f:
        #     self.modelo_2 = pickle.load(f)

        # with open("./assets/models/ModelsPipeline.pkl", "rb") as f:
        #     self.pipeline = pickle.load(f)
        
        self.display_page()

    def predict_customer(self,df:pd.DataFrame)-> pd.DataFrame:
        #instancio el df con las ids y las listas q contendran lso resultados
        predicts = pd.DataFrame(df.customer_id)
        churn_chance = []
        competitor_reason_chance=[]
        dissatisfaction_reason_chance=[]
        price_reason_chance=[]
        attitude_reason_chance=[]
        other_reason_chance=[]

        #Preds Modelo 1
        data, _ = self.pipeline.clean_nulls_dataset(df,[])
        data = self.pipeline.fitter.transform(data)
        preds_1 = self.modelo_1.predict_proba(data)[:len(data)]
        for pred in preds_1:
            churn_chance.append(round(pred[0]*100,2))

        predicts['churn_chance'] = churn_chance
        
        #Creo las columnas del dataframe
        predicts['competitor_reason_chance'] = 0
        predicts['dissatisfaction_reason_chance'] = 0
        predicts['price_reason_chance'] = 0
        predicts['attitude_reason_chance'] = 0
        predicts['other_reason_chance'] = 0

        #Seleciono las ids de los q van a churnear
        ids = predicts.loc[predicts.churn_chance >= 50].customer_id.to_list()

        #Preds Modelo 2
        data, _ = self.pipeline.clean_nulls_dataset(df[df.customer_id.isin(ids)],[])
        data = self.pipeline.fitter.transform(data)

        preds_2 = self.modelo_2.predict_proba(data)[:len(data)]

        for pred in preds_2:
            attitude_reason_chance.append(round(pred[0]*100,2))
            competitor_reason_chance.append(round(pred[1]*100,2))
            dissatisfaction_reason_chance.append(round(pred[2]*100,2))
            other_reason_chance.append(round(pred[3]*100,2))
            price_reason_chance.append(round(pred[4]*100,2))

        #Cargo las predicciones del modelo 2
        predicts.loc[predicts.churn_chance >= 50,'competitor_reason_chance'] = competitor_reason_chance
        predicts.loc[predicts.churn_chance >= 50,'dissatisfaction_reason_chance'] = dissatisfaction_reason_chance
        predicts.loc[predicts.churn_chance >= 50,'price_reason_chance'] = price_reason_chance
        predicts.loc[predicts.churn_chance >= 50,'attitude_reason_chance'] = attitude_reason_chance
        predicts.loc[predicts.churn_chance >= 50,'other_reason_chance'] = other_reason_chance

        return predicts

    def display_page(self):
        st.title("Aplicación del modelo")
        st.markdown("El modelo esta aplicado en una base de datos de sqllite con flask como api.\n>\nPuedes probarlo en la  [Notebook](https://colab.research.google.com/drive/1roIA3LR2fZoZzlAq2NSs2g5gWIRLzFKI?usp=sharing)")
        # st.title("Prueba el modelo desde aca")
        # demo_data = self.data.sample(20)
        # st.markdown("## Data inicial")
        # st.dataframe(demo_data)
        # predict = st.button("Obten Predicciones")
        # if predict:
        #     r = self.predict_customer(demo_data)
        #     st.dataframe(r)