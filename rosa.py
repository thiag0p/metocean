
'''
    Rotina de elaboração de rosa de distribuição
'''

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


def rose(dire, inte, suptitle=None, title=None):

    """
        dir     |       Lista com valores de direção
        int     |       Lista com valores de intensidade

    """

    dir_bin = np.arange(0., 361., 45)
    spd_bin = np.arange(0., inte.max() + 5., 5.)

    # Ocorrência do vento binado.
    counts, xedges, yedges, _ = plt.hist2d(dire, inte, bins=[dir_bin, spd_bin])
    ncounts = np.hstack(
        (np.zeros((counts.shape[0], 1)), counts)).cumsum(axis=1)
    # Selecionando cores do colormap.
    colors = ['#79a6d2', '#9fdf9f', '#ffe680', '#ff3300', '#b300b3']
    if len(colors) < len(spd_bin) - 1:
        interval = np.linspace(.1, .95, len(yedges) - 1)
        colors = [plt.cm.rainbow(i) for i in interval]
    fig_kw = dict(figsize=(13, 11), facecolor='white')
    subplot_kw = dict(facecolor='#ebebeb', polar=True)
    fig, ax = plt.subplots(subplot_kw=subplot_kw, **fig_kw)
    ax.set_axisbelow(True)
    ax.grid(b=True, axis='both', which='major', color='white',
            linestyle='-', linewidth=1.2)
    fig.suptitle(suptitle, y=.99, fontsize=15, fontweight='semibold')
    _ = ax.set_title(title, fontsize=12)
    # Setando eixos.
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")
    angles = np.arange(0., 360., 45)
    _, __ = ax.set_thetagrids(angles, fontweight='semibold')
    theta = np.radians(dir_bin)
    for i in range(len(dir_bin) - 1):
        for j in range(len(spd_bin) - 1):
            left, width = theta[i], theta[i + 1] - theta[i]
            height, bottom = ncounts[i, j + 1] - ncounts[i, j], ncounts[i, j]
            if height > 0.:
                ax.bar(left, height, width=width, bottom=bottom,
                       facecolor=colors[j], edgecolor='white', linewidth=1,
                       alpha=.9)
    ax.set_rlabel_position(-68.)
    yticklabels = [int(label) for label in ax.get_yticks()]
    for i, yticklabel in enumerate(yticklabels):
        if i == len(yticklabels) - 1:
            yticklabels[i] = u'Número de\nOcorrências\n\n' + \
                str(yticklabels[-1])
        else:
            yticklabels[i] = str(yticklabels[i])
    _ = ax.set_yticklabels(yticklabels, horizontalalignment='right',
                           verticalalignment='bottom', zorder=2)
    # Criar labels para legenda.
    labels = [
        ('>= {:.0f} - < {:.0f} m/s'.format(
            spd_bin[i], spd_bin[i + 1])).replace('.', ',')
        for i in range(len(spd_bin) - 1)]
    # Criar patch da legenda, atualizar handles e labels.
    patch_legend = [mpatches.Patch(color=colors[i], alpha=.9, label=label)
                    for i, label in enumerate(labels)]
    handles, _ = ax.get_legend_handles_labels()
    handles.append(patch_legend)
    legend = ax.legend(handles[0], labels, bbox_to_anchor=(.85, .92),
                       loc='lower left', scatterpoints=1,
                       title=u'', fancybox=True, borderaxespad=.2)
    frame = legend.get_frame()
    frame.set_color('#ebebeb')
    frame.set_edgecolor('#808080')

    return fig, ax
