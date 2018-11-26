# Intangible capital: depreciation rates and stocks

This repository contains the parameter estimates for intangible capital accumulation and estimated knowledge and organization capital stocks from Ewens, Peters and Wang (2018) work "[Acquisition prices and the measurement of intangible capital](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3287437)."  

## Primer on capitalizing intangibles: the perpetual inventory model

See Sections 2 and 4 of [Ewens, Peters and Wang (2018)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3287437).   Parameters of interest:

* ![equation](https://latex.codecogs.com/gif.latex?%5Cdelta_%7BG%7D): the depreciation rate of knowledge capital investmentment (i.e. R&D)
* ![equation](https://latex.codecogs.com/gif.latex?%5Cdelta_%7BS%7D):  the depreciation rate of organization capital investmentment (i.e. SG&A)
* ![equation](https://latex.codecogs.com/gif.latex?%5Cgamma): the percent of SG&A spending that is treated as investment in organizational capital. 

Each of these parameters are estimated for the [five Fama-French industries](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_5_ind_port.html).

## Parameter estimates

[The depreciation and investment parameters](https://github.com/michaelewens/intangible_capital/blob/master/capital_accum_parameters.csv) (in csv form) can be merged onto any dataset of firm-time R&D and SG&A flows using SIC codes.  The variables are
* `sic`: SIC code
* `knowDepr`: the estimate for the knowledge capital depreciation
* `organDepr`: the estimate for the organizational capital depreciation
* `gamma`: the estimate for the percentage of SG&A spending that is considered investment in organizational capital
* `industry5`: an integer in {1:5} that indicates what major Fama-French industry the SIC belongs to.  Note that Ewens, Peter and Wang (2018) put `sic >= 8000 & sic <= 8099` in `industry5 == 1`. 

Here are the estimates (Nov. 2018) along with their bootstrapped standard errors:

![Parameter estimates from Ewens, Peters and Wang (2018)](https://github.com/michaelewens/intangible_capital/blob/master/parameter_estimates_table.png)

We will soon provide code that allows you to take raw Compustat data and build the intangible capital stocks.  

## Stocks for Compustat firms

The [csv file](https://github.com/michaelewens/intangible_capital/blob/master/intangibleCapital_112618.csv) or [Stata .dta file](https://github.com/michaelewens/intangible_capital/blob/master/intangibleCapital_112618.dta) contains firm-year stocks of knowledge -- `knowCapital` -- and organizaton -- `orgCapital` -- capital implied by the parameter estimates.  The columns are:

* `gvkey`: the Compustat unique identifier
* `fyear`: the fiscal year
* `orgCapital`: organization capital (net) using SG&A 
* `knowCapital`: knowledge capital (net) using R&D

To load in Stata so you have the most up-to-date file:

`insheet using "https://github.com/michaelewens/intangible_capital/blob/master/intangibleCapital_112618.csv?raw=true", comma clear`

We use the industry-level parameter estimates from [Ewens, Peters and Wang (2018)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3287437) combined with the past 10 years of SG&A and R&D from the firm's income statement in Compustat.  All dollars are nominal.  Importantly, these stocks are _net_ assets, not gross.  So any year-on-year change represents a net, rather than gross investment.

## Code to construct stocks

Coming soon.

  ### Stata
  
  ### R
  
  ### Python
 
 ## Citation
 
 ```Latex
 @article{ewensPetersWang2018,
  title={Acquisition prices and the measurement of intangible capital},
  author={Ewens, Michael and Peters, Ryan and Wang, Sean},
  journal={Working Paper}
  year={2018}
  }
 ```
  
Ewens, Michael, Ryan Peters and Sean Wang. "[Acquisition prices and the measurement of intangible capital](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3287437)." Working paper, 2018.
