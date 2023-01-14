#! /usr/bin/env python3
'''
Plot prostate-specific antigen (PSA) line plots.

Plot PSA results for each doctor separately with and without warning limits.
Plot PSA results and estimate a linear regression line, and calculate when
the PSA will reach the warning limits.

time -f '%e' ./psa_analysis.py
./psa_analysis.py

Balk, S.P. Y.J. Ko, and G.J. Bubley.
"Biology of prosate-specific antigen."
*Journal of Clinical Oncology* 21 (January 2003), no. 2: 383-91.
[PMID 12525533 (https://www.ncbi.nlm.nih.gov/pubmed/12525533)]
(https://www.ncbi.nlm.nih.gov/pubmed/12525533).
[doi:10.1200/JCO.2003.02.083 (https://doi.org/10.1200 2FJCO.2003.02.083)]
(https://doi.org/10.1200/JCO.2003.02.083).

Catalona, W.J., J.P. Richie, F.R. Ahmann, M.A. Hudson, P.T. Scardino,
R.C. Flanigan, J.B. deKernion, T.L. Ratliff, L.R. Kavoussi, and B.L. Dalkin.
"Comparison of digital rectal examination and serum prostate specific antigen
in the early detection of prostate cancer: results of a multicenter clinical
trial of 6,630 mean."
*The Journal of Urology* 151 (May 1994), no. 5: 1283-90.
[PMID 7512659 (https://www.ncbi.nlm.nih.gov/pubmed/7512659)]
(https://www.ncbi.nlm.nih.gov/pubmed/7512659).

Prostate-specific antigen (PSA) is produced for the ejaculate, where it
liquifies the semen in the seminal coagulum and allows sperm to swim freely
(Balk et.al. 2003). PSA is present in small quantities in the serum of men with
healthy prostates, but is often elevated in the presence of prostate cancer or
other prostate disorders (Catalona et.al. 1994).

I was diagnosed with prostate cancer on 2013-03-08. I had a radical
prostatectomy on 2013-06-11 and 30 radiation treatments from 2013-09-13 to
2013-10-18.

From an initial PSA test immediately after the last radiation treatment and
every six months since, I have recorded the date, results, and consulting
physician. These results are analysed in this Jupyter notebook.

This Jupyter Notebook creates three scatter plots:

PSA v. Date, using the full range of the data to set the y axis limits.
PSA v. Date, using the trigger point of 3.0 to set the y axis limits.
This upper limit is the point at which the doctors said I would need further
treatment if my PSA results were to reach this value.
PSA v. Date, using the full range of the data to set the y axis limits, and a
linear regression line fitted to the data.
'''

from typing import NoReturn, Tuple
import time

import matplotlib.pyplot as plt
import statsmodels.api as sm
import datasense as ds
import pandas as pd
import numpy as np

colour1 = '#0077bb'
colour2 = '#33bbee'
figsize = (8, 6)
output_url = 'psa_analysis.html'
header_title = 'PSA analysis'
header_id = 'psa-analysis'
x_axis_label, y_axis_label, axis_title =\
    ('Date', 'PSA (ng/mL)', 'Prosate-specific Antigen (PSA) Test')
file_name_proudlove, file_name_perry, file_name_all =\
    ('psa_proudlove.csv', 'psa_perry.csv', 'psa_all.csv')


def main():
    start_time = time.time()
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    psa_proudlove, psa_perry, psa_all = read_data(
        file_name_1=file_name_proudlove,
        file_name_2=file_name_perry,
        file_name_3=file_name_all
    )
    axis_subtitle = f'Gilles Pilon {max_date(psa_proudlove, psa_perry)}'
    psa_all, model = psa_reg(psa_all)
    todo = [
        (psa_proudlove, psa_perry, 'Date', 'Date', 'PSA', 'PSA',
         None, '.', 'None', 'gilles_psa'),
        (psa_proudlove, psa_perry, 'Date', 'Date', 'PSA', 'PSA',
         (-0.05, 20), '.', 'None', 'gilles_psa_max'),
        (psa_all, psa_all, 'Date', 'Date', 'PSA', 'Predicted',
         None, 'None', '-', 'gilles_psa_regression')
        ]
    for df1, df2, x1, x2, y1, y2, ylim, g1, g2, filename in todo:
        plot_line(
            df1, df2, x1, x2, y1, y2,
            ylim, g1, g2, axis_subtitle, filename, psa_all
        )
    stop_time = time.time()
    ds.page_break()
    ds.report_summary(
        start_time=start_time,
        stop_time=stop_time,
        read_file_names=['psa_proudlove.csv', 'psa_perry.csv', 'psa_all.csv']
    )
    print()
    parameters = model.params
    print(parameters)
    print()
    print('summary()')
    print(model.summary())
    print()
    print('summary2()')
    print(model.summary2())
    print()
    print('df')
    print(psa_all)
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def plot_line(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    x1: str,
    x2: str,
    y1: str,
    y2: str,
    ylim: None,
    g1: str,
    g2: str,
    axis_subtitle: str,
    filename: str,
    psa_all: pd.DataFrame
) -> NoReturn:
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=figsize
    )
    ax.plot(
        df1[x1], df1[y1], marker=g1, linestyle=g2, color=colour1,
        label='Dr. Proudlove'
    )
    ax.plot(
        df2[x2], df2[y2], marker=g1, linestyle=g2, color=colour2,
        label='Dr. Perry'
    )
    ds.despine(ax=ax)
    ax.set_title(label=f'{axis_title}\n{axis_subtitle}')
    ax.set_ylabel(ylabel=y_axis_label)
    ax.set_xlabel(xlabel=x_axis_label)
    ax.autoscale(tight=False)
    if ylim is not None:
        ax.set_ylim(*ylim)
    if df1 is not psa_all:
        ax.legend(loc='upper left', frameon=False)
    fig.savefig(fname=f'{filename}.svg', format='svg')
    ds.html_figure(file_name=f'{filename}.svg')


def psa_reg(df: pd.DataFrame) -> Tuple[
    pd.DataFrame,
    sm.regression.linear_model.RegressionResultsWrapper
]:
    """
    Perform linear regression.
    """
    df['DateDelta'] = (df['Date'] - df['Date'].min())/np.timedelta64(1, 'D')
    x = sm.add_constant(data=df['DateDelta'])
    y = df['PSA']
    model = sm.OLS(endog=y, exog=x, missing='drop').fit()
    df['Predicted'] = model.fittedvalues
    return df, model


def max_date(
    df1: pd.DataFrame,
    df2: pd.DataFrame
) -> str:
    """
    Determine the maximum date in the dataframes.
    """
    md = max(df1['Date'].max(), df2['Date'].max()).date().isoformat()
    return md


def read_data(
    file_name_1: str,
    file_name_2: str,
    file_name_3: str
) -> Tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame
]:
    """
    Read the three raw files into dataframes.
    """
    df1 = pd.read_csv(file_name_1, parse_dates=['Date'])
    df2 = pd.read_csv(file_name_2, parse_dates=['Date'])
    df3 = pd.read_csv(file_name_3, parse_dates=['Date'])
    return (df1, df2, df3)


if __name__ == '__main__':
    main()
