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
        
        if self.lang == "EN":
            with open("./assets/text/datainfotext_en.json", "r", encoding="utf-8") as f:
                self.page_txt = json.load(f)
        if self.lang == "ES":
            with open("./assets/text/datainfotext_es.json", "r", encoding="utf-8") as f:
                self.page_txt = json.load(f)
        self.display_page()
        
    def display_page(self):
        st.header(self.page_txt['page_header'])
        st.write(self.page_txt['dataset_source'])
        st.write(self.page_txt['types_of_client'])

        st.write(self.page_txt['client_frequency'])
        temp_df = pd.concat([self.data['Customer Status'].value_counts().to_frame('Cantidad absoluta'),
                        (self.data['Customer Status'].value_counts(normalize=True)*100).to_frame('Cantidad porcentual')], 
                        axis=1).style.format({'Cantidad porcentual': '{:.2f}%'})
        cols = st.columns(3, gap="small")
        
        with cols[0]:                
            fig, ax = plt.subplots(figsize=(3,3))
            utils.wheel_chart(self.data['Customer Status'], ax, [self.cat_colors[0],self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': 7 })
            st.pyplot(fig.patch.set_alpha(0.0))
        st.dataframe(temp_df)

        st.write(self.page_txt['unique_title'])
        unicos = self.data['Customer ID'].nunique()
        st.write(self.page_txt['unique_txt'].format(unicos,self.data.shape))
        
        st.write(self.page_txt['null_amount'])
        temp_df = pd.concat([self.data.isna().sum().to_frame('cantidad de nulos absoluta'),
                            (self.data.isna().sum() / len(self.data) * 100).to_frame('cantidad de nulos porcentual'),
                            self.data.dtypes.to_frame('tipo de variable')], axis=1).style.format({'cantidad de nulos porcentual': '{:.2f}%'})
        st.dataframe(temp_df)

        st.write(self.page_txt['column_info'])
        st.dataframe(self.data.head())