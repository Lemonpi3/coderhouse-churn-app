import streamlit as st
from scripts.setuppage import SetupPage
from scripts.storytelling import StoryTelling
from scripts.infodatapage import DataInfo
from scripts.homepage import HomePage
import json

with open("appconfig.json", "r") as f:
    config = json.load(f)

st.set_page_config(layout="wide",page_title='Coderhouse Churn Proyect',page_icon='📊')
st.set_option('deprecation.showPyplotGlobalUse', False)


side_bar_txt = {
    "ES":{
        "LanguageSelect":"Lenguaje (updates after changing page)",
        'NavigationLable':"Navegación",
        "NavigationOptions":["Inicio", "Info de la Data", "Stortylling", "3","Configuración"]},
    "EN":{
        "LanguageSelect":"Language (se updatea al cambiar de página)",
        'NavigationLable':"Navigation",
        "NavigationOptions":["Home", "Data info", "Stortylling", "3","Config"]
    }
}
with st.sidebar:
    page = st.radio(side_bar_txt[config["lang"]]["NavigationLable"],side_bar_txt[config["lang"]]["NavigationOptions"])

    lang = st.selectbox(side_bar_txt[config["lang"]]["LanguageSelect"],["ES","EN"],["ES","EN"].index(config["lang"]))

    if lang:
        with open("appconfig.json", "r") as file:
            data = json.load(file)
        data['lang']= lang
        with open("appconfig.json", "w") as jsonfile:
            json_conf = json.dump(data, jsonfile, indent=0)
            jsonfile.close()
#home
if page == side_bar_txt[config["lang"]]["NavigationOptions"][0]:
    HomePage()
#config
if page == side_bar_txt[config["lang"]]["NavigationOptions"][-1]:
    SetupPage()
#datainfo
if page == side_bar_txt[config["lang"]]["NavigationOptions"][1]:
    DataInfo()
#storytelling
if page == side_bar_txt[config["lang"]]["NavigationOptions"][2]:
    if lang == 'EN':
        st.warning('The English version of this section is under development')
    else:
        StoryTelling()