# Protein-specific antigen (PSA) analysis

## In brevi

Prostate-specific antigen (PSA) is produced for the ejaculate, where it liquifies the semen in the seminal coagulum and allows sperm to swim freely (Balk et.al. 2003). PSA is present in small quantities in the serum of men with healthy prostates, but is often elevated in the presence of prostate cancer or other prostate disorders (Catalona et.al. 1994).

This Jupyter Notebook creates two scatter plots:

1. PSA v. Date, using the full range of the data to set the y axis limits.
2. PSA v. Date, using the *trigger point* of 3.0 to set the y axis limits. This upper limit is the point at which the doctors said I would need further treatment if my PSA results were to reach this value.
3. PSA v. Date, using the full range of the data to set the y axis limits, and a linear regression line fitted to the data.

## Data

Download the two data files:

- [PSA results from Dr. Proudlove](https://drive.google.com/open?id=0BzrdQfHR2I5DdHNFMWtSQ3JSclE)
- [PSA results from Dr. Perry](https://drive.google.com/open?id=0BzrdQfHR2I5DdF9pRUM1c1FZZmM)
- [PSA results from Dr. Proudlove and Dr. Perry](https://drive.google.com/open?id=1P-m2GIVUq9o68cvTXa16-cpfb3xMp7fw)

## Methodology

Three plots are drawn with pandas.DataFrame.plot. Ordinary least squares (OLS) regression is estimated with statsmodels.formula.api.

## References

Balk, S.P. Y.J. Ko, and G.J. Bubley. "Biology of prosate-specific antigen." *Journal of Clinical Oncology* 21 (January 2003), no. 2: 383-91. [PMID 12525533 (https://www.ncbi.nlm.nih.gov/pubmed/12525533)](https://www.ncbi.nlm.nih.gov/pubmed/12525533). [doi:10.1200/JCO.2003.02.083 (https://doi.org/10.1200 2FJCO.2003.02.083)](https://doi.org/10.1200/JCO.2003.02.083).

Catalona, W.J., J.P. Richie, F.R. Ahmann, M.A. Hudson, P.T. Scardino, R.C. Flanigan, J.B. deKernion, T.L. Ratliff, L.R. Kavoussi, and B.L. Dalkin. "Comparison of digital rectal examination and serum prostate specific antigen in the early detection of prostate cancer: results of a multicenter clinical trial of 6,630 mean." *The Journal of Urology* 151 (May 1994), no. 5: 1283-90. [PMID 7512659 (https://www.ncbi.nlm.nih.gov/pubmed/7512659)](https://www.ncbi.nlm.nih.gov/pubmed/7512659).
