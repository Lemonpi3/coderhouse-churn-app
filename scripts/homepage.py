import streamlit as st
from scripts import utils
import json

class HomePage():
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']

        self.page_txt = {
            'EN':{
                'page_header':'Welcome',
                'page_info':'If you want to change the color palettes go to the config section found in the sidebar',
                'page_txt':"If you want to see the notebook follow this link ➡ [link](https://colab.research.google.com/drive/1GEjWwAE95JHSPKmM9H44bBQAFvAfFELX)",
                
            },
            'ES':{
                'page_header':'Bienvenido/a',
                'page_txt':"Si quieres ver la notebook sigue este link ➡ [link](https://colab.research.google.com/drive/1GEjWwAE95JHSPKmM9H44bBQAFvAfFELX)",
                'page_info':'Si quieres cambiar las paletas de colores visita la sección de configuración.',
            }
        }
        self.display_page()
    
    def display_page(self):
        st.header(self.page_txt[self.lang]['page_header'])
        st.write(self.page_txt[self.lang]['page_txt'])
        st.info(self.page_txt[self.lang]['page_info'])
