# Intangible capital: accumulation and stocks

This repository contains (or will contain) the parameter estimates for intangible capital accumulation from Ewens, Peters and Wang (2018) work "Acquiring Intangibles."  

## Primer on capitalizing intangibles: the perpetual inventory model

## Parameter estimates

[The depreciation and investment parameters](https://github.com/michaelewens/intangible_capital/blob/master/capital_accum_parameters.csv) (in csv form) can be merged onto any dataset of firm-time R&D and SG&A flows using SIC codes.  The variables are
* `sic`: SIC code
* `knowDepr`: the estimate for the knowledge capital depreciation
* `organDepr`: the estimate for the organizational capital depreciation
* `gamma`: the estimate for the percentage of SG&A spending that is considered investment in organizational capital
* `industry5`: an integer in {1:5} that indicates what major Fama-French industry the SIC belongs to.  Note that Ewens, Peter and Wang (2018) put `sic >= 8000 & sic <= 8099` in `industry5 == 1`. 

We will soon provide code that allows you to take raw Compustat data and build the intangible capital stocks.  

## Stocks for Compustat firms

## Code to construct stocks

  ### Stata
  
  ### R
  
  
  ### Python
