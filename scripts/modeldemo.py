import streamlit as st
from scripts import utils
import json

class DemoPage():
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)

        self.display_page()
    
        
    def display_page(self):
        st.title("Aplicación del modelo")
        st.markdown("El modelo esta aplicado en una base de datos de sqllite con flask como api.\n>\nPuedes probarlo en la  [Notebook](https://colab.research.google.com/drive/1Bl-SoktMZqwaI53Mhx6heTFW-F_9TiMR?usp=sharing)")