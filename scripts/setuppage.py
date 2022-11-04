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
                'page_header':'Setup De la app\n---------',
                'page_info':'Esta pagina es para configurar algunas settings de la app',
                'color_title':'Configuración de colores',
                'pallete_selector_label':'selecciona las paletas de color',
                'apply_config_button':'aplicar configuración',
                'cat_c_txt':'Categorical Color Pallet',
                'div_c_txt':'Diverging Color Palette',
            },
            'ES':{
                'page_header':'Setup De la app\n---------',
                'page_info':'Esta pagina es para configurar algunas settings de la app',
                'color_title':'Configuración de colores',
                'pallete_selector_label':'selecciona las paletas de color',
                'apply_config_button':'aplicar configuración',
                'cat_c_txt':'Colores para paleta categorica',
                'div_c_txt':'Colores para paleta divergente',
            }
        }
        self.display_page()

    def display_page(self):
        def color_palette_menu(cat_palette,div_palette):
            fig,ax = plt.subplots(figsize=(20,1))
            st.text(self.page_txt[self.lang]['cat_c_txt'])
            st.pyplot(utils.palplot(cat_palette,size=10,ax=ax, fig=fig))
            st.text(self.page_txt[self.lang]['div_c_txt'])
            fig,ax = plt.subplots(figsize=(20,1))
            st.pyplot(utils.palplot(div_palette[::-1],size=10,ax=ax, fig=fig))

        st.header(self.page_txt[self.lang]['page_header'])
        st.info(self.page_txt[self.lang]['page_info'])
        st.title(self.page_txt[self.lang]['color_title'])
        cols = st.columns(3, gap="small")
        with cols[0]:
            choice = st.selectbox(self.page_txt[self.lang]['pallete_selector_label'],['default','protanopia','deuteranopia','tritanopia','achromatopsia',
                                                                                        'protanomaly','deuteranomaly','tritanomaly','achromatomaly'])
            if choice == 'default':
                cat_palette = ["#6cd4c5","#a3ea63","#cf75a4","#2a6d76","#25b7f1","#849ab7","#e27c7c"]
                div_palette = ["#e27c7c","#b76a6a","#8b5858","#5f4646","#333333","#425c58","#50847c","#5eaca1","#6cd4c5"]
            elif choice == 'protanopia':
                cat_palette = ["#9999c8","#c1c283","#a8a798","#474773","#6465e2","#8d8daf","#b5b47c"]
                div_palette = ["#b5b47c","#95946a","#747458","#545346","#333333","#4d4d58","#66667d","#7f80a3","#9999c8"]
            elif choice == 'deuteranopia':
                cat_palette = ["#938bc9","#bdb88b","#adb395","#433e73","#5b50df","#8c8aae","#bbc37c"]
                div_palette = ["#bbc37c","#9a9f69","#777b58","#555746","#333232","#4b4959","#635f7e","#7b75a4","#938bc9"]
            elif choice == 'tritanopia':
                cat_palette = ["#71cbcc","#a69da3","#ca8f8d","#2d7271","#2cd7d5","#85aaa9","#dc7c7c"]
                div_palette = ["#dc7c7c","#b36a6a","#885858","#5d4646","#323333","#435959","#527f7f","#61a5a6","#71cbcc"]
            elif choice == 'achromatopsia':
                cat_palette = ["#b3b3b3","#c5c5c5","#959595","#595959","#919191","#969696","#9a9a9a"]
                div_palette = ["#9a9a9a","#818181","#676767","#4d4d4d","#323232","#535353","#737373","#939393","#b3b3b3"]
            elif choice == 'protanomaly':
                cat_palette = ["#7fb1c6","#afd273","#be929e","#365674","#3f86e9","#8892b3","#cf9d7c"]
                div_palette = ["#cf9d7c","#a8836a","#816858","#5a4e46","#323333","#465358","#59727d","#6c92a2","#7fb1c6"]
            elif choice == 'deuteranomaly':
                cat_palette = ["#80b9c7","#b1d776","#bd8c9d","#375b74","#4291e8","#8894b2","#cd967c"]
                div_palette = ["#cd967c","#a77d69","#806558","#5a4c46","#333333","#475558","#5a767d","#6d97a2","#80b9c7"]
            elif choice == 'tritanomaly':
                cat_palette = ["#6fcfc7","#a5c57b","#cc819b","#2c6f74","#29c6e6","#84a1b1","#de7c7c"]
                div_palette = ["#de7c7c","#b46a69","#895858","#5e4646","#333332","#425a58","#51817d","#60a9a3","#6fcfc7"]
            elif choice == 'achromatomaly':
                cat_palette = ["#92c2bb","#b5d698","#af869b","#446266","#60a2bc","#8e98a5","#bb8c8c"]
                div_palette = ["#bb8c8c","#997676","#776060","#554a4a","#333332","#4b5755","#637b77","#7b9e99","#92c2bb"]
            color_palette_menu(cat_palette, div_palette)

            if st.button(self.page_txt[self.lang]['apply_config_button']):
                with open("appconfig.json", "r") as f:
                    data = json.load(f)
                data['cat_palette']= cat_palette
                data['div_palette']= div_palette

                with open("appconfig.json", "w") as jsonfile:
                    json_conf = json.dump(data, jsonfile,indent=0)
                    jsonfile.close()

        