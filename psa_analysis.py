#! /usr/bin/env python3

'''
Prostate-specific antigen (PSA) analysis

time -f '%e' ./psa_analysis.py | tee psa_analysis.txt
'''


# time -f '%e' ./psa_analysis.py > psa_analysis.txt
# ./psa_analysis.py > psa_analysis.txt


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.axes as axes
import statsmodels.formula.api as smf


# https://matplotlib.org/tutorials/colors/colormaps.html
c = cm.Paired.colors  # c[0] c[1] ... c[11]


def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_color('none')


def psa_reg(df: pd.DataFrame) -> pd.DataFrame:
    df['Julian'] = df.index.to_julian_date()
    results = smf.ols(formula='PSA ~ Julian', data=df).fit()
    parameters = results.params
    julian_predicted = (3.0 - parameters[0])/parameters[1]
    gregorian_predicted = pd.to_datetime(julian_predicted, unit='D',
                                         origin='julian').strftime('%Y-%m-%d')
    df['Predicted'] = results.predict(df['Julian'])
    df = df.drop(columns='Julian')
    return df, results, gregorian_predicted


if __name__ == '__main__':
    psa_proudlove = pd.read_csv('psa_proudlove.csv',
                                parse_dates=True,
                                index_col='Date')
    psa_perry = pd.read_csv('psa_perry.csv',
                            parse_dates=True,
                            index_col='Date')
    psa_all = pd.read_csv('psa_all.csv',
                          parse_dates=True,
                          index_col='Date')
    title = 'Prosate-specific Antigen (PSA) Test'
    max_date = max(psa_proudlove.index.max(),
                   psa_perry.index.max()).date().isoformat()
    subtitle = f'Gilles Pilon {max_date}'
    yaxislabel = 'PSA (ng/mL)'
    xaxislabel = 'Date'
    for ylim, filename in \
            (None, 'gilles_psa'),\
            ((-0.05, 3), 'gilles_psa_max'):
        fig, ax = plt.subplots(figsize=(12, 12))
        psa_proudlove.plot(y='PSA',
                           color=c[0],
                           style='.',
                           legend=False,
                           label='Dr. Proudlove',
                           ax=ax)
        psa_perry.plot(y='PSA',
                       color=c[1],
                       style='.',
                       legend=False,
                       label='Dr. Perry',
                       ax=ax)
        despine(ax)
        ax.set_title(f'{title}\n{subtitle}')
        ax.set_ylabel(yaxislabel)
        ax.set_xlabel(xaxislabel)
        ax.autoscale(tight=False)
        if ylim is not None:
            ax.set_ylim(*ylim)
        ax.legend(loc='upper left', frameon=False)
        ax.figure.savefig(f'{filename}.svg', format='svg')
        ax.figure.savefig(f'{filename}.png', format='png')
        ax.figure.savefig(f'{filename}.pdf', format='pdf')
    fig, ax = plt.subplots(figsize=(12, 12))
    psa_all, results, gregorian_predicted = psa_reg(psa_all)
    psa_all.plot(y='PSA',
                 color=c[2],
                 style='.',
                 legend=False,
                 label=None,
                 ax=ax)
    psa_all.plot(y='Predicted',
                 color=c[3],
                 style=None,
                 legend=False,
                 label=None,
                 ax=ax)
    ax.set_title(f'{title}\n{subtitle}')
    ax.set_ylabel(yaxislabel)
    ax.set_xlabel(xaxislabel)
    ax.autoscale(tight=False)
    despine(ax)
    ax.figure.savefig('gilles_psa_regression.svg', format='svg')
    ax.figure.savefig('gilles_psa_regression.png', format='png')
    ax.figure.savefig('gilles_psa_regression.pdf', format='pdf')
    print(f'My PSA will reach 3.0 on {gregorian_predicted}.'
          f'\n\n{results.summary()}')
