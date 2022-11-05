import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from scripts import utils
import json
import numpy as np
import pandas as pd
import textwrap
import warnings
from mpl_toolkits.basemap import Basemap

class StoryTelling:
    def __init__(self) -> None:
        with open("appconfig.json", "r") as f:
            config = json.load(f)
        self.lang = config['lang']
        self.cat_colors = config['cat_palette']
        self.div_colors = config['div_palette']
        self.data = pd.read_csv("./assets/data/dataset.csv")

        self.page_txt = {
            'EN':{
                
            },
            'ES':{
                'intro_title':'Introducción',
                'comercial_ctx':'''
                    En el area de telecomunicaciones, la rotación de los clientes que contratan y dejan los servicios es bastante comun y frecuente.
                    Las razones de porque dejan los servicios pueden tener diferentes motivos, pero se pueden dividir en 2 grandes grupos: **Evitables** e **Inevitables**.
                    >
                    #### Ahora, ¿que tipos de razones son evitables y cuales son inevitables?
                    Las razones inevitables son aquellas de las cuales la empresa no tiene control y/o culpa como, por ejemplo, cuando un cliente se muda o fallece.
                    >
                    Por otro lado las razones evitables son aquellas que tienen que ver con la calidad del servicio, la atencion que recibio el cliente e incluso la poca competitividad de la empresa comparada con otras del area.
                    >
                    #### Entonces, ¿que es lo que buscamos como empresa para crecer?
                    Lo que se busca como empresa es minimizar la cantidad de clientes que dejan aumentando la retención de los clientes, asi como tambien atraer a una mayor cantidad de clientes.
                    Los valores normales de churned tienen que estar por debajo de los que se unen ya que para que la empresa crezca la cantidad de clientes debe crecer.
                    ''',
                'comercial_problem_title':'#### Lo que nos lleva al problema comercial que tiene la empresa.',
                'user_dist_title':'Distribución de cada grupo de usuario',
                'user_dist_description':'Como se puede ver en el gráfico,en este ultimo cuatrimestre, tenemos muchos mas usuarios que dejaron el servicio que los que se unieron. Lo cual significa que la empresa esta perdiendo clientes y por ende mucho dinero.',
                'revenue_title':'### ¿Pero, Cuánto dinero representan estos usuarios churned?',
                'revenue_report':"""
                    El total de ganancias de este cuatrimestre fue de 
                    <font color='lime'>\$21371131.69</font>
                    pero las ganancias provenientes de los usuarios que dejaron el servicio fueron de 
                    <font color='red'>\$3684459.82</font> que representan
                    <font color='red'>17.24%</font> del total.
                    """,
                'revenue_graph_labels':['Ganancias de Usuarios\n Retenidos + Nuevos','Ganancias de los \nusuarios Perdidos'],
            }
        }
        self.display_page()

    def display_page(self):
        st.header('Storytelling \n--------------')
        st.title(self.page_txt[self.lang]['intro_title'])
        st.write(self.page_txt[self.lang]['comercial_ctx'])
        st.write(self.page_txt[self.lang]['comercial_problem_title'])
        temp_df = pd.concat([self.data['Customer Status'].value_counts().to_frame('Cantidad absoluta'),
                        (self.data['Customer Status'].value_counts(normalize=True)*100).to_frame('Cantidad porcentual')], 
                        axis=1).style.format({'Cantidad porcentual': '{:.2f}%'})
        cols = st.columns(3, gap="small")
        with cols[0]:                
            fig, ax = plt.subplots(figsize=(3,3))
            utils.wheel_chart(self.data['Customer Status'], ax, [self.cat_colors[0],self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': 7 })
            ax.set_title(self.page_txt[self.lang]['user_dist_title'],fontdict={ 'color': 'w','weight': 'bold','size': 10 })
            fig.patch.set_alpha(0.0)
            st.pyplot()
        with cols[1]:
            st.dataframe(temp_df)
            st.write(self.page_txt[self.lang]['user_dist_description'])
        
        st.write(self.page_txt[self.lang]['revenue_title'])
        cols = st.columns(2, gap="small")
        with cols[0]:
            st.markdown(self.page_txt[self.lang]['revenue_report'],unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8,8))

            temp_df = pd.Series([round((21371131.69-3684459.82)/21371131.69*100,2),round(3684459.82/21371131.69*100,2)])
            text_labels = self.page_txt[self.lang]['revenue_graph_labels']
            labels = [text_labels[i] + f'\n{g}%'for i,g in enumerate(temp_df)]
            ax.pie(temp_df,labels=labels, radius=1,colors = [self.cat_colors[1],self.cat_colors[-1]],
                    wedgeprops=dict(width=0.3),textprops={'color': 'w','weight': 'bold','size': 15 })
            fig.patch.set_alpha(0.0)
            st.pyplot()
        st.markdown('## Visto esto, ¿Qué esta causando y Donde estan ocurriendo la perdida de usuarios?')
        cols = st.columns(2, gap="small")
        with cols[1]:
            items = ['All'] + list(self.data[self.data['Customer Status']=='Churned']['Churn Category'].unique())
            motivo = st.selectbox('Categoria de Churn',items)
            colors = [  self.div_colors[0], self.div_colors[0], self.div_colors[0], self.div_colors[1], self.div_colors[1], 
                        self.div_colors[1], self.div_colors[2], self.div_colors[2], self.div_colors[2], self.div_colors[3],
                        self.div_colors[3], self.div_colors[3], self.div_colors[4], self.div_colors[4], self.div_colors[4],]
            if motivo != 'All':
                utils.top_15_ciudad_county_percent(self.data[(self.data['Customer Status']=='Churned') & (self.data['Churn Category']==motivo)],
                    title_city='Top 15 ciudades con mas churned',title_county='Top 15 condados con mas churned',figsize=(4,6.1),
                    fontdict={ 'color': 'white','weight': 'bold','size': 7},colors=colors)
            else:
                utils.top_15_ciudad_county_percent(self.data[(self.data['Customer Status']=='Churned')],
                    title_city='Top 15 ciudades con mas churned', title_county='Top 15 condados con mas churned',figsize=(4,6.1),
                    fontdict={ 'color': 'white','weight': 'bold','size': 7},colors=colors)
            st.pyplot()

        with cols[0]:
            fig, ax = plt.subplots(figsize=(8,8))
            if motivo != 'All':
                utils.plot_scatter_map(self.data[(self.data['Customer Status']=='Churned') & (self.data['Churn Category']==motivo)],title="Distribución espacial de los churned",alpha=0.2,
                                    ax = ax,dot_color=self.cat_colors[-1],land_color=self.div_colors[4],water_col=self.cat_colors[4])
            else:
                utils.plot_scatter_map(self.data[(self.data['Customer Status']=='Churned')],title="Distribución espacial de los churned",alpha=0.2,
                                    ax = ax,dot_color=self.cat_colors[-1],land_color=self.div_colors[4],water_col=self.cat_colors[4])
            fig.patch.set_alpha(0.0)
            st.pyplot()
        
        st.markdown('''
        Las zonas mas pobladas del estado son las mas affectadas principalmente los condados de San Diego y Los Angeles los cuales representan alrededor del 30% de los usuarios perdidos.
        >
        Veamos que razones predominan en cada una de estas areas y cuanto dinero nos estan costado.''')

        #por ahi complicarlo luego
        cols = st.columns(3, gap="small")
        with cols[0]:
            counties = [*['All'], *list(self.data[self.data['Customer Status']=='Churned']['County'].unique())]
            motives = [*['All'] ,*list(self.data[self.data['Customer Status']=='Churned']['Churn Category'].unique())]
            county = st.selectbox('Condado',counties,0)
            st.warning('Hay un bug que no deja mostrar county All y una razon a la vez (toma el county como alpine por razones misteriosas)')
            motivo = st.selectbox('Razon de Churn',motives,0)

            if county != 'All':
                if motivo != 'All':
                    total_churned_revenue = self.data[(self.data['Customer Status']=='Churned') & 
                                (self.data['Churn Category']==motivo) &
                                (self.data['County']==county)]['Total Revenue'].sum()
                    churned_revenue_percent = str(round(total_churned_revenue / self.data[self.data['Customer Status']=='Churned']['Total Revenue'].sum() * 100,2)) + '%'
                    temp_df = pd.DataFrame({'County':[county],'Category':[motivo],'Churned Revenue':[total_churned_revenue],"Percent of\nTotal revenue":[churned_revenue_percent]}).set_index('County',drop=True)
                    st.dataframe(temp_df,use_container_width=True)
                else:
                    temp_df = {'County':[],'Churn Category':[],'Churned Revenue':[],'Percent of\nTotal revenue':[]}
                    total_churned_revenue = self.data[(self.data['Customer Status']=='Churned') & 
                                (self.data['County']==county)]['Total Revenue'].sum()
                    churned_revenue_percent = str(round(total_churned_revenue / self.data[self.data['Customer Status']=='Churned']['Total Revenue'].sum() * 100,2)) + '%'
                    st.write('Total for {}: {} ({} of total revenue)'.format(county,total_churned_revenue,churned_revenue_percent))

                    for cat in self.data[(self.data['Customer Status']=='Churned')]['Churn Category'].unique():
                        churned_revenue = self.data[(self.data['Customer Status']=='Churned') & 
                                (self.data['Churn Category']==cat) &
                                (self.data['County']==county)]['Total Revenue'].sum()
                        churned_revenue_percent = str(round(churned_revenue / self.data[self.data['Customer Status']=='Churned']['Total Revenue'].sum() * 100,2)) + '%'
                        temp_df['County'].append(county)
                        temp_df['Churn Category'].append(cat)
                        temp_df['Churned Revenue'].append(churned_revenue)
                        temp_df['Percent of\nTotal revenue'].append(churned_revenue_percent)

                    st.dataframe(pd.DataFrame(temp_df).set_index('County',drop=True).sort_values('Percent of\nTotal revenue',ascending=False),use_container_width=True)
            else:
                if motivo != 'All':
                    temp_df = {'County':[],'Category':[],'Churned Revenue':[],"Percent of\nTotal revenue":[]}
                    total_cat_revenue = self.data[(self.data['Customer Status']=='Churned') & 
                                    (self.data['Churn Category']==motivo)]['Total Revenue'].sum()
                    total_cat_revenue_percent = str(round(total_cat_revenue / self.data[self.data['Customer Status']=='Churned']['Total Revenue'].sum() * 100,2)) + '%'
                    st.write('Total for {}: {} ({} of total revenue)'.format(motivo,total_cat_revenue,total_cat_revenue_percent))
                    for county in self.data['County'].unique():
                        total_churned_revenue = self.data[(self.data['Customer Status']=='Churned') & 
                                    (self.data['Churn Category']==motivo) &
                                    (self.data['County']==county)]['Total Revenue'].sum()
                        churned_revenue_percent = str(round(total_churned_revenue / self.data[self.data['Customer Status']=='Churned']['Total Revenue'].sum() * 100,2)) + '%'
                        temp_df['County'].append(county)
                        temp_df['Category'].append(motivo)
                        temp_df['Churned Revenue'].append(total_churned_revenue)
                        temp_df['Percent of\nTotal revenue'].append(churned_revenue_percent)

                    temp_df = pd.DataFrame(temp_df).set_index('County',drop=True).sort_values('Percent of\nTotal revenue',ascending=False)
                    st.dataframe(temp_df,use_container_width=True)
                else:
                    total_cat_revenue = self.data[(self.data['Customer Status']=='Churned')].groupby(['County','Churn Category'])['Total Revenue'].sum()
                    total_cat_revenue = pd.DataFrame(total_cat_revenue)
                    total_cat_revenue['Percent of\nTotal revenue'] = [str(round(value / self.data[self.data['Customer Status']=='Churned']['Total Revenue'].sum() * 100,2)) + '%' for value in total_cat_revenue['Total Revenue']]
                    st.dataframe(total_cat_revenue.sort_values('Percent of\nTotal revenue',ascending=False),use_container_width=True)
        with cols[1]:
            if county != 'All':
                if motivo != 'All':
                    utils.plot_box_map(self.data,self.cat_colors,county=county,cat=motivo,fontdict={ 'fontsize': 7,'color': 'white','fontweight': 'bold','horizontalalignment': 'center' })
                    st.pyplot()
                else:
                    utils.plot_box_map(self.data,self.cat_colors,warp_width=8,county=county,fontdict={ 'fontsize': 7,'color': 'white','fontweight': 'bold','horizontalalignment': 'center' },figsize=(8,8))
                    st.pyplot()
                    st.info('Puedes hacer zoom clickeando el boton que sale al pasar el mouse sobre el grafico')
            else:
                if motivo == 'All':
                    utils.plot_box_map(self.data,self.cat_colors,warp_width=8,fontdict={ 'fontsize': 7,'color': 'white','fontweight': 'bold','horizontalalignment': 'center' },figsize=(8,8))
                    st.pyplot()
                    st.info('Puedes hacer zoom clickeando el boton que sale al pasar el mouse sobre el grafico')
                else:
                    utils.plot_box_map(self.data,self.cat_colors,cat=motivo,fontdict={ 'fontsize': 7,'color': 'white','fontweight': 'bold','horizontalalignment': 'center' })
                    st.pyplot()
        with cols[2]:
            if county != 'All':
                cond = ((self.data['County'] == county) &
                        (self.data['Customer Status']=='Churned'))
                churn_category_percent = round(self.data[cond].groupby('Churn Category')['Total Revenue'].sum() / self.data[(self.data['Customer Status']=='Churned')]['Total Revenue'].sum() * 100,2)
                churn_category_money = self.data[cond].groupby('Churn Category')['Total Revenue'].sum()
                st.markdown(f'Porcentaje del revenue de los churned por \ncategoria de churn para {county}')
                utils.plot_churn_cat_rev_percent(self.data[cond],self.cat_colors)
                st.pyplot()
                st.dataframe(pd.DataFrame({'Category':list(churn_category_percent.index),'Revenue':churn_category_money.values,'% of Total Churned Revenue for county':[str(value) +'%' for value in churn_category_percent.values]}))
            else:
                cond = ((self.data['Customer Status']=='Churned'))
                churn_category_percent = round(self.data[cond].groupby('Churn Category')['Total Revenue'].sum() / self.data[(self.data['Customer Status']=='Churned')]['Total Revenue'].sum() * 100,2)
                churn_category_money = self.data[cond].groupby('Churn Category')['Total Revenue'].sum()
                st.markdown(f'Porcentaje del revenue de los churned por \ncategoria de churn para {county}')
                utils.plot_churn_cat_rev_percent(self.data[cond],self.cat_colors)
                st.pyplot()
                st.dataframe(pd.DataFrame({'Category':list(churn_category_percent.index),'Revenue':churn_category_money.values,'% of Total Churned Revenue for county':[str(value) +'%' for value in churn_category_percent.values]}))
        
        st.markdown('''
            * **La competencia es la razon principal** de los churned en los condados representando en general 30-70% de los churned.Los unicos condados donde no es la principal son Fresno, Orange y Ventura donde estan empatados o superados por probelmas en la actitud del soporte.
            >
            En la mayoria de los condados ,entre las razones de la competencia, predomina que ofrece mejores dispositivos. La excepcion a esto es San Diego donde domina la mejor oferta por parte de los competidores.
            >
            * **La razon secundaria es la actitud del soporte y del proveedor** de cada condado representando en general 15-35% de los churned.Se puede observar en Fresno, Orange, Kern, Ventura y San Bernandino como los principales con este problema y San Diego, San Francisco y Sacramento donde este problema es minimo
            >
            * **Y las razones terciarias** son disatisfaccion con los productos,servicios y los precios tanto del servicio como de los cargos a larga distancia.
            >
            Este problema representa aproximadamente 15-30% de los churned en cada condado. En los unicos en los que no se presenta a gran tamaño es en San Diego y Kern y
            en los que peor impactan estas razones son Los Angeles, Contra Costa y San Bernandino.
            ''')
        
        utils.plot_stacked_bar_distribution(colors=self.cat_colors,figsize=(30,8))
        st.pyplot()
        temp_df = pd.read_csv('./assets/data/dist_top_15_df.csv',index_col='County')
        temp_df.index.name ='County'
        st.dataframe(temp_df,use_container_width=True,)
        
        st.markdown('''
            ### ¿Que deberiamos hacer para combatir estos problemas?
            * Para ganarle a la competencia y retener los usuarios deberiamos ofrecer mejores dispositvos y ofertas.
            * Habria que ver que esta pasando con el soporte en Fresno, Orange, Kern, Ventura , San Bernandino y Los Angeles ya que estan dando una mala calidad de servicio.
            * Por la disatisfacción de producto habria que ver la estabilidad de la red, la calidad de los productos que estamos brindando y revisar el costo de las ofertas que tenemos para que esten acorde
                a lo que brindamos. Los condados donde deberiamos concentrarnos incialmente por esto son Los Angeles, Contra Costa y San Bernandino
            ### Hablando de las ofertas que ofrecemos, ¿Hay alguna que causa problemas?
            Veamos la distribución de los Churned en cada tipo de oferta.''')

        fig , ax = plt.subplots(2,3,figsize=(12,8))
        ax = ax.flatten()
        for i,offer in enumerate(self.data['Offer'].unique()):
            temp_df = self.data[self.data['Offer']==offer][['Offer','Customer Status']]
            temp_df = temp_df['Customer Status'].apply(lambda x:'Not churned' if x != 'Churned' else x)
            utils.cat_comp_wheel_chart(temp_df.value_counts(normalize=True).sort_index(),ax[i],title=offer,colors=[self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': 10 })
        fig.patch.set_alpha(0.0)
        st.pyplot()

        st.markdown('''
                Podemos observar que la oferta mas problematica es la **Oferta E** teniendo mas del 50% de usuarios Churned, habria que mejorarla.
                Luego las otras ofertas que impactan negativamente son la **Oferta D y C** donde aproximadamente 1 de cada 4 usuarios es Churned.
                Tambien se puede ver que el 27% de los usuarios que no poseen oferta dejan el servicio, habria que meterlos en una oferta para disminuir las chances de que dejen.
            
                ###  Veamos como el tipo de oferta Afecta a diferentes grupos de usuarios
            ''')
        cols = st.columns(2,gap='small')
        with cols[0]:
            oferta = st.selectbox('Oferta',['All', 'None', 'Offer A', 'Offer B', 'Offer C', 'Offer D', 'Offer E'])
            filtro = st.selectbox('Tipo de categoria',['Servicios','Pagos','Usuario'])
        
        cols = st.columns(2,gap='small')
        with cols[0]:
            if oferta == 'All':
                if filtro == 'Servicios':
                    fig , ax = plt.subplots(1,2,figsize=(8,8))
                    ax = ax.flatten()
                    font_s = 8
                    #Phone Y
                    cond= self.data['Phone Service'] == 'Yes'
                    temp_df = self.data[cond][['Customer Status','Phone Service']]
                    temp_df = temp_df['Customer Status'].apply(lambda x:'Not churned' if x != 'Churned' else x)
                    utils.cat_comp_wheel_chart(temp_df.value_counts(normalize=True).sort_index(),ax[0],title=f'Users with \nPhone Service\n({len(temp_df)} of {len(self.data)} Total users)',colors=[self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': font_s })
                    #Phone N
                    cond= self.data['Phone Service'] == 'No'
                    temp_df = self.data[cond][['Customer Status','Phone Service']]
                    temp_df = temp_df['Customer Status'].apply(lambda x:'Not churned' if x != 'Churned' else x)
                    utils.cat_comp_wheel_chart(temp_df.value_counts(normalize=True).sort_index(),ax[1],title=f'Users without \nPhone Service\n({len(temp_df)} of {len(self.data)} Total users)',colors=[self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': font_s })
                    fig.patch.set_alpha(0.0)
                    st.pyplot()

                    fig , ax = plt.subplots(1,2,figsize=(8,8))
                    ax = ax.flatten()
                    #inter Y
                    temp_df = self.data[['Customer Status','Internet Service']]
                    cond= self.data['Internet Service'] == 'Yes'
                    temp_df = temp_df['Customer Status'].apply(lambda x:'Not churned' if x != 'Churned' else x)
                    utils.cat_comp_wheel_chart(temp_df.value_counts(normalize=True).sort_index(),ax[0],title=f'Users with \nInternet Service\n({len(temp_df)} of {len(self.data)} Total users)',colors=[self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': font_s })
                    
                    #inter N
                    temp_df = self.data[['Customer Status','Internet Service']]
                    cond= self.data['Internet Service'] == 'No'
                    temp_df = temp_df['Customer Status'].apply(lambda x:'Not churned' if x != 'Churned' else x)
                    utils.cat_comp_wheel_chart(temp_df.value_counts(normalize=True).sort_index(),ax[1],title=f'Users with \nInternet Service\n({len(temp_df)} of {len(self.data)} Total users)',colors=[self.cat_colors[-1],self.cat_colors[1]],fontdict={ 'color': 'w','weight': 'bold','size': font_s })
                    fig.patch.set_alpha(0.0)
                    st.pyplot()
                #internet data
                with cols[1]:
                    pass
                                   
