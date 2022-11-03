import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from scripts import utils
import json

class SetupPage:
    def __init__(self):
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
        def color_palette_menu(cat_palette,div_palette):
            fig,ax = plt.subplots(figsize=(20,1))
            st.text('Categorical Color Pallet')
            st.pyplot(utils.palplot(cat_palette,size=10,ax=ax, fig=fig))
            st.text('Diverging Color Palette')
            fig,ax = plt.subplots(figsize=(20,1))
            st.pyplot(utils.palplot(div_palette[::-1],size=10,ax=ax, fig=fig))

        st.header(self.page_txt[self.lang]['page_header'])
        st.info(self.page_txt[self.lang]['page_info'])
        st.title(self.page_txt[self.lang]['color_title'])
        cols = st.columns(3, gap="small")
        with cols[0]:
            choice = st.selectbox(self.page_txt[self.lang]['pallete_selector_label'],['default','protanopia'])
            if choice == 'default':
                cat_palette = ["#6cd4c5","#a3ea63","#cf75a4","#2a6d76","#25b7f1","#849ab7","#e27c7c"]
                div_palette = ["#e27c7c","#b76a6a","#8b5858","#5f4646","#333333","#425c58","#50847c","#5eaca1","#6cd4c5"]
            elif choice == 'protanopia':
                cat_palette = ["#9999c8","#c1c283","#a8a798","#474773","#6465e2","#8d8daf","#b5b47c"]
                div_palette = ["#b5b47c","#95946a","#747458","#545346","#333333","#4d4d58","#66667d","#7f80a3","#9999c8"]
            color_palette_menu(cat_palette, div_palette)

            if st.button(self.page_txt[self.lang]['apply_config_button']):
                with open("appconfig.json", "r") as f:
                    data = json.load(f)
                data['cat_palette']= cat_palette
                data['dv_palette']=div_palette

                with open("appconfig.json", "w") as jsonfile:
                    json_conf = json.dump(data, jsonfile)
                    jsonfile.write(json_conf)

        