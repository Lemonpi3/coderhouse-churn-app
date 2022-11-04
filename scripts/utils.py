import matplotlib.ticker as ticker
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

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