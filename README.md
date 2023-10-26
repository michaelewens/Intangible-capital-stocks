# Intangible capital: depreciation rates and stocks

This repository contains the parameter estimates for intangible capital accumulation and estimated knowledge and organization capital stocks from Ewens, Peters and Wang (2023) work "[Measuring Intangible Capital with Market Prices](https://osf.io/preprints/socarxiv/kvp2f/)."  

In April 2019, we updated our methodology for adjusting goodwill and fixed a bug in our estimation code.  The parameter estimates have changed, so we encourage researchers to use these updated numbers.  In October 2023, we identified a small data error in our estimation sample that resulted in small changes to the parameter estimates and estimated intangible stocks.  The changes had no meaningful impacts on the relative performance of the paper's intangible asset stocks. 

## Primer on capitalizing intangibles: the perpetual inventory model

See Sections 2 and 4 of [Ewens, Peters and Wang (2023)](https://osf.io/preprints/socarxiv/kvp2f/).   Parameters of interest:

* ![equation](https://latex.codecogs.com/gif.latex?%5Cdelta_%7BG%7D): the depreciation rate of knowledge capital investment (i.e. R&D)
* ![equation](https://latex.codecogs.com/gif.latex?%5Cdelta_%7BS%7D):  the depreciation rate of organization capital investment (i.e. SG&A)
* ![equation](https://latex.codecogs.com/gif.latex?%5Cgamma): the percent of SG&A spending that is treated as investment in organizational capital. 

Each of these parameters are estimated for the [five Fama-French industries](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_5_ind_port.html).

## Parameter estimates

[The depreciation and investment parameters](https://github.com/michaelewens/intangible_capital/blob/master/capital_accum_parameters_2023.csv) (in csv form) can be merged onto any dataset of firm-time R&D and SG&A flows using SIC codes.  The variables are
* `sic`: SIC code
* `knowDepr`: the estimate for the knowledge capital depreciation
* `organDepr`: the estimate for the organizational capital depreciation
* `gamma`: the estimate for the percentage of SG&A spending that is considered investment in organizational capital
* `industry5`: an integer in {1:5} that indicates what major Fama-French industry the SIC belongs to.  Note that Ewens, Peters and Wang (2018) put `sic >= 8000 & sic <= 8099` in `industry5 == 1`.  We also move some "high-tech" TV/radio providers into consumer ([see this file for classification scheme](https://github.com/michaelewens/intangible_capital/blob/master/industry5.do)) 

Here are the estimates (Oct. 2023) along with their bootstrapped standard errors:

![Parameter estimates from Ewens, Peters and Wang (2020)](https://github.com/michaelewens/intangible_capital/blob/master/parameter_est2023.png)

We will soon provide code that allows you to take raw Compustat data and build the intangible capital stocks.  

## Stocks for Compustat firms

The [csv file](https://github.com/michaelewens/intangible_capital/blob/master/intangibleCapital_090123.csv) or [Stata .dta file](https://github.com/michaelewens/intangible_capital/blob/master/intangibleCapital_090123.dta) contains firm-year stocks of knowledge -- `knowCapital` -- and organization -- `orgCapital` -- capital implied by the parameter estimates.  The columns are:

* `gvkey`: the Compustat unique identifier
* `fyear`: the fiscal year
* `orgCapital`: organization capital (net) using SG&A 
* `knowCapital`: knowledge capital (net) using R&D

To load in Stata so you have the most up-to-date file:

`insheet using "https://github.com/michaelewens/intangible_capital/blob/master/intangibleCapital_090123.csv?raw=true", comma clear`

or

`use "https://github.com/michaelewens/intangible_capital/raw/master/intangibleCapital_090123.dta", clear`

We use the industry-level parameter estimates from [Ewens, Peters and Wang (2023)](https://osf.io/preprints/socarxiv/kvp2f/) combined with the past 10 years of SG&A and R&D from the firm's income statement in Compustat.  All dollars are nominal.  Importantly, these stocks are _net_ assets, not gross.  So any year-on-year change represents a net, rather than gross investment.

## Code to construct stocks

Dijun Liu [wrote a Python script](https://github.com/michaelewens/Intangible-capital-stocks/blob/master/intangibes_cleaned.py) that generates stocks with correlations > .99 with the EPW stocks.

  ### Stata
  
  ### R
  
  ### Python
 
 ## Citation
 
 ```Latex
 @article{ewensPetersWang2023,
  title={Measuring Intangible Capital with Market Prices},
  author={Ewens, Michael and Peters, Ryan and Wang, Sean},
  journal={Management Science},
  year={Forthcoming}
  }
 ```
  
Ewens, Michael, Ryan Peters and Sean Wang. "[Measuring Intangible Capital with Market Prices](https://osf.io/preprints/socarxiv/kvp2f/)." Management Science, forthcoming, 2023.
