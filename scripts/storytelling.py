import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from scripts import utils
import json
import numpy as np
import pandas as pd

class DataInfo:
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']

        self.page_txt = {
            'EN':{
                'page_header':'Setup De la app',
                'page_info':'Esta pagina es para configurar algunas settings de la app',
                'color_title':'Configuración de colores',
                'pallete_selector_label':'selecciona las paletas de color',
                'apply_config_button':'aplicar configuración',
            },
            'ES':{
                'page_header':'Setup De la app',
                'page_info':'Esta pagina es para configurar algunas settings de la app',
                'color_title':'Configuración de colores',
                'pallete_selector_label':'selecciona las paletas de color',
                'apply_config_button':'aplicar configuración',
            }
        }
        self.display_page()
    def display_page(self):
        st.write('WIP datainfo')
class StoryTelling:
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']

        self.page_txt = {
            'EN':{
                'page_header':'Setup De la app',
                'page_info':'Esta pagina es para configurar algunas settings de la app',
                'color_title':'Configuración de colores',
                'pallete_selector_label':'selecciona las paletas de color',
                'apply_config_button':'aplicar configuración',
            },
            'ES':{
                'page_header':'Setup De la app',
                'page_info':'Esta pagina es para configurar algunas settings de la app',
                'color_title':'Configuración de colores',
                'pallete_selector_label':'selecciona las paletas de color',
                'apply_config_button':'aplicar configuración',
            }
        }
        self.display_page()
    def display_page(self):
        st.write('WIP storytelling')
