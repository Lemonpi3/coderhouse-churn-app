import matplotlib.ticker as ticker
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import squarify
import textwrap
import pandas as pd

def palplot(pal, size=1, ax=None, fig=None):
    """Plot the values in a color palette as a horizontal array.
    Parameters
    ----------
    pal : sequence of matplotlib colors
        colors, i.e. as returned by seaborn.color_palette()
    size :
        scaling factor for size of plot
    ax :
        an existing axes to use
    """
    n = len(pal)
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(n * size, size))
    ax.imshow(np.arange(n).reshape(1, n),
              cmap=mpl.colors.ListedColormap(list(pal)),
              interpolation="nearest", aspect="auto")
    ax.set_xticks(np.arange(n) - .5)
    ax.set_yticks([-.5, .5])
    ax.set_xticklabels(["" for _ in range(n)])
    fig.set_facecolor((0,0,0,0))
    fig.set_alpha(0.0)
    ax.set_xticks([])
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.set_facecolor((0,0,0,0))
    ax.set_alpha((0.0))

def wheel_chart(X,ax,colors,width=0.3,radius=1,fontdict ={'color': 'darkred', 'weight': 'bold', 'size': 16,}):
    size_of_groups= round(X.value_counts(normalize=True) *100,2).values
    cmap = sns.color_palette(colors)
    labels = [X.unique()[i] + f'\n{g}%'for i,g in enumerate(size_of_groups)]
    ax.pie(size_of_groups,labels=labels, radius=radius,colors = cmap[:len(X.unique())],
            wedgeprops=dict(width=width),textprops=fontdict)

def cat_comp_wheel_chart(X,ax,colors,title='',width=0.3,radius=1,fontdict ={'color': 'darkred', 'weight': 'bold', 'size': 16,}):
    size_of_groups=round(X * 100,2)
    cmap = sns.color_palette(colors)
    text_labels = X.index
    labels = [text_labels[i] + f'\n{g}%'for i,g in enumerate(size_of_groups)]
    ax.pie(size_of_groups,labels=labels, radius=radius,colors = cmap[:len(text_labels)],
            wedgeprops=dict(width=width),textprops=fontdict)
    ax.set_title(title,fontdict)

def plot_scatter_map(df, alpha=0.7, title='', ax=None ,dot_color='blue',land_color='grey',water_col='lightblue', marcar_ciudades=True, fontdict ={'color': 'white', 'weight': 'bold', 'size': 7,}):
  '''
  Dibuja un scatter con el mapa de california
  Parametros:
  df: el dataframe ya filtrado (usa la latitud y longitud)
  alpha: transparencia de los puntitos. Por defecto es 0.7
  title: titulo del grafico (requiere pasar ax)
  ax: el axis de matplotlib
  marcar_ciudades: si es igual a True marca las ciudades de Sacramento, San Fracisco 
  ,Los Angeles y San Diego (True por defecto, requiere pasar ax)
  
  retorna==>> dibuja el mapa la ubicacion de las lineas del dataframe seleccionadas.
  '''
  m = Basemap(projection='lcc', resolution='i', 
              lat_0=37.5, lon_0=-119,
              width=1E6, height=1.2E6, ax=ax)

  m.drawcoastlines(color='black')
  m.drawcountries(color='black')
  m.fillcontinents(color=land_color,lake_color=water_col)
  m.drawstates(color='black')
  m.drawlsmask(ocean_color=water_col,lakes=True)
  
  m.drawcounties()

  lat = df['Latitude'].values
  lon = df['Longitude'].values

  if marcar_ciudades and m.ax:
    x, y = m(-117.16,32.71)
    m.ax.annotate('• San Diego', xy=(x, y), xycoords='data', xytext=(x, y), textcoords='data',fontsize=fontdict['size'],fontweight=fontdict['weight'],color=fontdict['color'],alpha=0.7)
    x, y = m(-121.49,38.58)
    m.ax.annotate(f'• Sacramento', xy=(x, y), xycoords='data', xytext=(x, y), textcoords='data',fontsize=fontdict['size'],fontweight=fontdict['weight'],color=fontdict['color'],alpha=0.7)
    x, y = m(-118.24,34.05)
    m.ax.annotate(f'• Los Angeles', xy=(x, y), xycoords='data', xytext=(x, y), textcoords='data',fontsize=fontdict['size'],fontweight=fontdict['weight'],color=fontdict['color'],alpha=0.7)
    x, y = m(-122.41,37.77)
    m.ax.annotate(f'• San Francisco', xy=(x, y), xycoords='data', xytext=(x, y), textcoords='data',fontsize=fontdict['size'],fontweight=fontdict['weight'],color=fontdict['color'],alpha=0.7)

  ax.set_title(title,color =fontdict['color'],fontsize=fontdict['size']*2)
  m.scatter(lon, lat, latlon=True,
          alpha=alpha,color=dot_color)

def top_15_ciudad_county_percent(df,figsize=(6,10),title_city='',title_county='',fontdict ={'color': 'white', 'weight': 'bold', 'size': 7,},colors=['#ae2012', '#bb3e03', '#ee9b00', '#ee9b00', '#ee9b00', '#ee9b00', '#ee9b00','#B39002','#B39002','#B39002','#B39002','#B39002','#B39002','#B39002','#B39002']):

    top_churned_cities = df['City'].value_counts()
    top_churned_counties = df['County'].value_counts()
    representation_of_county = round(top_churned_counties/len(df) *100,2)
    representation_of_city = round(top_churned_cities/len(df) * 100,2)

    fig, ax = plt.subplots(2,1,figsize=figsize)
    ax=ax.flatten()
    ax=ax.flatten()
    
    ax[0].patch.set_alpha(0.0)
    ax[0].spines['right'].set_visible(False)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['bottom'].set_visible(False)

    ax[0].barh(representation_of_city.index[:15],representation_of_city[:15],color=sns.color_palette(colors))
    ax[0].set_title(title_city,color =fontdict['color'],fontsize=fontdict['size']+2)
    ax[0].invert_yaxis()
    ax[0].spines['left'].set_color('white')
    ax[0].set_yticklabels(representation_of_city.index[:15],fontsize=fontdict['size'])
    ax[0].set_xticks([])
    ax[0].tick_params(colors='white',size=0.1)

    for i, v in enumerate(round(representation_of_city[:15],2).values):
        ax[0].text(v+.1, i + .25, str(v)+'%', fontweight=fontdict['weight'],color=fontdict['color'],fontsize=fontdict['size'])

    ax[1].patch.set_alpha(0.0)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)

    ax[1].set_title(title_county,color =fontdict['color'],fontsize=fontdict['size']+2)
    ax[1].barh(representation_of_county.index[:15],representation_of_county[:15],color=sns.color_palette(colors))
    ax[1].invert_yaxis()
    ax[1].spines['left'].set_color('white')
    ax[1].set_yticklabels(representation_of_county.index[:15],fontsize=fontdict['size'])
    ax[1].set_xticks([])
    ax[1].tick_params(colors='white',size=0.1)

    for i, v in enumerate(round(representation_of_county[:15],2).values):
        ax[1].text(v+.1, i + .25, str(v)+'%', fontweight=fontdict['weight'],color=fontdict['color'],fontsize=fontdict['size'])

    fig.patch.set_alpha(0.0)

def plot_box_map(df, colors, figsize=(4,4),warp_width=10, county = 'All',cat = 'All', fontdict = {'color': 'white','fontsize':10, 'fontweight':'bold','horizontalalignment':'center',}):
    if county != 'All':
        if cat == 'All':
            cond = (
            (df['Churn Reason'] != 'Moved') & 
            (df['Churn Reason'] != 'Deceased') & 
            (df['Churn Reason'] !="Don't know") & 
            (df['County'] == county)
            )
        else:
            cond = (
            (df['Churn Reason'] != 'Moved') & 
            (df['Churn Reason'] != 'Deceased') & 
            (df['Churn Reason'] !="Don't know") & 
            (df['County'] == county) &
            (df['Churn Category'] == cat)
            )
    else:
        if cat == 'All':
            cond = (
            (df['Churn Reason'] != 'Moved') & 
            (df['Churn Reason'] != 'Deceased') & 
            (df['Churn Reason'] !="Don't know")
            )
        else:
            cond = (
            (df['Churn Reason'] != 'Moved') & 
            (df['Churn Reason'] != 'Deceased') & 
            (df['Churn Reason'] !="Don't know") & 
            (df['Churn Category'] == cat) &
            (df['County'] != 'All')
            )
            
    fig,ax=plt.subplots(figsize=figsize)
    fig.patch.set_alpha(0.0)
    fig.set_facecolor((0,0,0,0))
    fig.set_alpha(0.0)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.yaxis.set_major_locator(ticker.NullLocator())
    sizes = df[cond]['Churn Reason'].value_counts(normalize=True) * 100

    labels = ['Lack of affordable download / upload speed' if label == 'Lack of affordable download/upload speed' else label for label in sizes.index]
    labels = [f"{label}\n{round(value,2)}%" if value > 2.5 else '' for label,value in zip(labels, sizes.values)]

    labels = [textwrap.fill(label, width=warp_width,
                        break_long_words=False) for label in labels]

    s = squarify.plot(sizes=sizes,
                        label=labels,
                        alpha=.8,
                        color=sns.color_palette(colors),
                        ax=ax,
                        text_kwargs=fontdict,
                        pad=10,
                        )
    fontdict['fontsize']= fontdict['fontsize'] * 1.7
    
    if county != 'All':
        if cat == 'All':
            s.set_title(f'Churn Reasons distribution for {county}',fontdict=fontdict)
        else:
            s.set_title(f'Churn Reasons distribution\n for {county}-{cat}',fontdict=fontdict)
    else:
        if cat == 'All':
            s.set_title(f'Churn Reasons\n distribution total',fontdict=fontdict)
        else:
            s.set_title(f'Churn Reasons\n distribution for {cat}',fontdict=fontdict)
    plt.axis('off')

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

def plot_churn_cat_rev_percent(df,cat_colors):
    churn_category_percent = round(df.groupby('Churn Category')['Total Revenue'].sum() / df['Total Revenue'].sum() * 100,2)

    fig,ax=plt.subplots(figsize=(8,6))
    g = sns.barplot(data=churn_category_percent,
    x=churn_category_percent.sort_values().index,
    y=churn_category_percent.sort_values().values, 
    ax=ax,
    palette=cat_colors,
    )
    g.set_xticklabels(churn_category_percent.sort_values(ascending=False).index)
    g.set_xlabel('Categoria de churn',color='w', fontweight='bold')
    g.patch.set_alpha(0.0)
    g.spines['right'].set_visible(False)
    g.spines['top'].set_visible(False)
    g.spines['left'].set_visible(False)
    g.set_yticks([])
    g.set_xticklabels(churn_category_percent.sort_values().index,color='white', fontweight='bold',size=10)

    #labels de los % en las barras
    for i, v in enumerate(round(churn_category_percent.sort_values(),2).values):
        ax.text(i-0.2 ,v+0.1 , str(v)+'%', fontweight='bold',color='white')
    fig.patch.set_alpha(0.0)

def plot_stacked_bar_distribution(colors=["#6cd4c5","#a3ea63","#cf75a4","#2a6d76","#25b7f1","#849ab7","#e27c7c"],fontdict={
    'fontweight': 'bold', 'color':'white','fontsize':15},figsize=(32,8)):

    distribution = pd.read_csv('./assets/data/distribution_top_15.csv')
    
    sorter = ['los_angeles', 'san_diego', 'orange', 'riverside',
       'san_bernardino', 'sacramento', 'santa_clara', 'alameda', 'fresno',
       'contra_costa', 'kern', 'humboldt', 'tulare',
       'san_mateo', 'sonoma']

    #cambio el tipo de la columna a categoria para poder sortearla
    distribution.County = distribution.County.astype("category")
    distribution.County.cat.set_categories(sorter, inplace=True)
    distribution.sort_values(['County','Churn Category'], inplace = True,ascending=(True,True))

    #devuelvo al tipo que era antes para seguir usandola
    distribution.County = distribution.County.astype("object")
    distribution['%'] = distribution['%'] * 100

    fig,ax=plt.subplots(1,1,figsize=figsize)

    g = sns.histplot(data= distribution,
                y='County', hue='Churn Category',weights='%',
                palette = sns.color_palette(colors),
                legend=False,
                multiple = 'stack',
                )
    g.patch.set_alpha(0.0)

    #pongo los % en las cajas con mas de 1.2%
    for c in g.containers:
        labels = [str(round(v.get_width(),2))+'%' if v.get_width() > 1.2 else '' for v in c]
        g.bar_label(c, labels=labels, label_type='center')


    g.set_title('Distribución de Churn Category en Top 15 condados',fontdict=fontdict)

    # g.set_ylabel('Condado',color=fontdict['color'])
    g.set_ylabel('')
    #cambio los ticks numericos por las clases para tener una referencia de donde esta 
    #cada razon.
    g.tick_params(colors='white',size=0.1)
    g.set_xlabel('')
    g.set_xticks(range(5,105,20),labels=distribution['Churn Category'].unique()[::-1],rotation=0)

    for i,tick_label in enumerate(g.axes.get_yticklabels()):
        tick_label.set_size(20)

    #les pongo el color para que ayude a referenciar con el color de cada caja
    for i,tick_label in enumerate(g.axes.get_xticklabels()):
        #correcion bug colores
        if i == 0:
            color = colors[4]
        elif i == 1:
            color = colors[3]
        elif i == 3:
            color = colors[1]
        elif i == 4:
            color = colors[0]
        else:
            color = colors[2]

        tick_label.set_color(color)
        tick_label.set_size(20)
        
    fig.patch.set_alpha(0.0)
    #quito unas partes blancas que habian quedado y los ejes
    g.grid(visible=False)
    sns.despine(left=True,bottom=True)

    #acomodo la leyenda a la derecha por fuera del grafico
    # sns.move_legend(ax,bbox_to_anchor=(1, 0.5),loc=10)
    fig.patch.set_alpha(0.0)