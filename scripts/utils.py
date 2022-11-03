
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
    import matplotlib.ticker as ticker
    import matplotlib as mpl
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    
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