# Intangible capital: accumulation and stocks

This repository contains (or will contain) the parameter estimates for intangible capital accumulation from Ewens, Peters and Wang (2018) work "Acquisition prices and the measurement of intangible capital."  

## Primer on capitalizing intangibles: the perpetual inventory model

Small section on the "model" so that the parameters below make sense.

## Parameter estimates

[The depreciation and investment parameters](https://github.com/michaelewens/intangible_capital/blob/master/capital_accum_parameters.csv) (in csv form) can be merged onto any dataset of firm-time R&D and SG&A flows using SIC codes.  The variables are
* `sic`: SIC code
* `knowDepr`: the estimate for the knowledge capital depreciation
* `organDepr`: the estimate for the organizational capital depreciation
* `gamma`: the estimate for the percentage of SG&A spending that is considered investment in organizational capital
* `industry5`: an integer in {1:5} that indicates what major Fama-French industry the SIC belongs to.  Note that Ewens, Peter and Wang (2018) put `sic >= 8000 & sic <= 8099` in `industry5 == 1`. 

We will soon provide code that allows you to take raw Compustat data and build the intangible capital stocks.  

## Stocks for Compustat firms

The [csv file](https://github.com/michaelewens/intangible_capital/blob/master/intangible_stocks.csv) contains firm-year stocks of both knowledge -- `G` -- and organizaton -- `S` -- capital implied by the parameter estimates.  The columns are

* `gvkey`: the Compustat unique identifier
* `S`: organization capital (net) using SG&A 
* `G`: knowledge capital (net) using R&D

We use the industry-level parameter estimates from Ewens, Peters and Wang (2018) combined with the past 10 years of SG&A and R&D from the firm's income statement.  All dollars are nominal.  Importantly, these stocks are _net_ assets, not gross.  So any year-on-year change represents a net, rather than gross investment.  

## Code to construct stocks

  ### Stata
  
  ### R
  
  
  ### Python
