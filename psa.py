#! /usr/bin/env python3
"""
Plot prostate-specific antigen (PSA) scatter plot.

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
2013-10-18. My cancer returned in late 2020 and convirmed in late 2021. I am
undergoing antigen treatments.

From an initial PSA test immediately after the last radiation treatment and
every test since, I have recorded the date, results, and consulting
physician.
"""

from pathlib import Path

import datasense as ds
import numpy as np


def main():
    ax_title = "Prostate-specific Antigen (PSA) Test"
    path_graph_svg = Path("psa.svg")
    path_graph_png = Path("psa.png")
    path_data = Path("psa.csv")
    ax_ylabel = "PSA (ng/mL)"
    date_column = ["Date"]
    ax_xlabel = "Date"
    figsize = (12, 9)
    grid_alpha = 0.1
    ds.style_graph()
    df = ds.read_file(file_name=path_data, parse_dates=date_column)
    x = df["Date"]
    y = df["PSA"]
    fig, ax = ds.plot_scatter_x_y(X=x, y=y, figsize=figsize)
    ax.set_yticks(ticks=np.arange(start=min(y), stop=max(y)+2, step=2))
    ax.grid(visible=True, which="major", axis="y", alpha=grid_alpha)
    ax.set_title(label=f"{ax_title}\n{x.max().date().isoformat()}")
    ax.set_ylabel(ylabel=ax_ylabel)
    ax.set_xlabel(xlabel=ax_xlabel)
    fig.savefig(fname=path_graph_svg, format="svg")
    fig.savefig(fname=path_graph_png, format="png")


if __name__ == "__main__":
    main()
