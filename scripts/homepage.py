import streamlit as st
from scripts import utils
import json
import streamlit.components.v1 as components

class HomePage():
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']

        if self.lang == "EN":
            with open("./assets/text/main_text_en.json", "r", encoding="utf-8") as f:
                self.page_txt = json.load(f)
        if self.lang == "ES":
            with open("./assets/text/main_text_es.json", "r", encoding="utf-8") as f:
                self.page_txt = json.load(f)
        
        self.presentacion = '''
    <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAFSCiujuaU&#x2F;view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>
<a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAFSCiujuaU&#x2F;view?utm_content=DAFSCiujuaU&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">Link al canva</a>
'''
        self.display_page()
    
        
    def display_page(self):
        st.header(self.page_txt['page_header'])
        st.write(self.page_txt['page_txt'])
        st.info(self.page_txt['page_info'])
        st.markdown("## Resumen del proyecto a modo de presentación")
        components.html(self.presentacion,height=700)
