#! /usr/bin/env python3

'''
Prostate-specific antigen (PSA) analysis

Plot PSA results for each doctor separately with and without warning limits.
Plot PSA results and estimate a linear regression line, and calculate when
the PSA will reach the warning limits.

    time -f '%e' ./psa_analysis.py > psa_analysis.txt
    time -f '%e' ./psa_analysis.py | tee psa_analysis.txt
'''


from typing import Tuple


import numpy as np
import pandas as pd
import matplotlib.axes as axes
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import statsmodels.api as sm
from matplotlib.dates import DateFormatter, MonthLocator
from matplotlib.ticker import NullFormatter, NullLocator


c = cm.Paired.colors


def main():
    psa_proudlove, psa_perry, psa_all = read_data()
    maximum_date = max_date(psa_proudlove, psa_perry)
    x_axis_label, y_axis_label, axis_title, axis_subtitle =\
        ('Date', 'PSA (ng/mL)', 'Prosate-specific Antigen (PSA) Test',
         f'Gilles Pilon {maximum_date}')
    psa_all = psa_reg(psa_all)
    print(psa_all)
    todo = [
        (psa_proudlove, psa_perry, 'Date', 'Date', 'PSA', 'PSA',
         None, '.', 'None', 'gilles_psa'),
        (psa_proudlove, psa_perry, 'Date', 'Date', 'PSA', 'PSA',
         (-0.05, 3), '.', 'None', 'gilles_psa_max'),
        (psa_all, psa_all, 'Date', 'Date', 'PSA', 'Predicted',
         None, '.', '-', 'gilles_psa_regression')
        ]
    for df1, df2, x1, x2, y1, y2, ylim, g1, g2, filename in todo:
        figure_width_height = (8, 6)
        fig = plt.figure(figsize=figure_width_height)
        ax = fig.add_subplot(111)
        ax.plot(df1[x1], df1[y1],
                marker=g1, linestyle=g2, color=c[0],
                label='Dr. Proudlove')
        ax.plot(df2[x2], df2[y2],
                marker=g1, linestyle=g2, color=c[1],
                label='Dr. Perry')
        despine(ax)
        ax.set_title(f'{axis_title}\n{axis_subtitle}')
        ax.set_ylabel(y_axis_label)
        ax.set_xlabel(x_axis_label)
        ax.autoscale(tight=False)
        if ylim is not None:
            ax.set_ylim(*ylim)
        if df1 is not psa_all:
            ax.legend(loc='upper left', frameon=False)
        ax.figure.savefig(f'{filename}.svg', format='svg')
        ax.figure.savefig(f'{filename}.png', format='png')
        ax.figure.savefig(f'{filename}.pdf', format='pdf')


def despine(ax: axes.Axes) -> None:
    '''
    Remove the top and right spines of a graph.

    There is only one x axis, on the bottom, and one y axis, on the left.
    '''
    for spine in 'right', 'top':
        ax.spines[spine].set_visible(False)


def psa_reg(df: pd.DataFrame) -> pd.DataFrame:
    df['DateDelta'] = (df['Date'] - df['Date'].min())/np.timedelta64(1, 'D')
    model = sm.OLS(df['PSA'], sm.add_constant(
        df['DateDelta']), missing='drop'
    ).fit()
    df['Predicted'] = model.fittedvalues
    return df


def max_date(df1: pd.DataFrame, df2: pd.DataFrame) -> str:
    md = max(
        df1['Date'].max(),
        df2['Date'].max()
    ).date().isoformat()
    return md


def read_data() -> Tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame
]:
    df1 = pd.read_csv('psa_proudlove.csv', parse_dates=['Date'])
    df2 = pd.read_csv('psa_perry.csv', parse_dates=['Date'])
    df3 = pd.read_csv('psa_all.csv', parse_dates=['Date'])
    return (df1, df2, df3)


if __name__ == '__main__':
    main()
