<!-- Author manuscript (October 26, 2023 version) of Ewens, Peters and Wang, "Measuring Intangible Capital with Market Prices," Management Science 71.1 (2024): 407-427, https://doi.org/10.1287/mnsc.2021.02058. Converted from the PDF with docling. Equations appear as "formula-not-decoded" placeholders in this conversion; see the PDF for the displayed equations. -->

## Measuring Intangible Capital with Market Prices ∗

Michael Ewens 1 , Ryan H. Peters 2 , and Sean Wang 3

1 Columbia Business School &amp; NBER 2 Tulane University 3 Southern Methodist University

October 2023

Accounting standards prohibit internally created knowledge and organizational capital from being disclosed on firm balance sheets. As a result, balance sheets exhibit downward biases that have become exacerbated by increasing levels of intangible investments. To offset these biases, researchers must estimate the value of these off-balance sheet intangibles by capitalizing prior flows of R&amp;D and SG&amp;A. In doing so, a set of capitalization parameters must be assumed, i.e., the R&amp;D depreciation rate and the fraction of SG&amp;A that represents a long-lived asset. We estimate these parameters using market prices from firm exits and use them to capitalize intangibles for a comprehensive panel of firms from 1978-2017. We then use a series of validation tests to examine the performance of our intangible capital stocks versus those developed from commonly used parameters. On average, our estimates of intangible capital are 15% smaller than estimates from status-quo parameters while exhibiting larger variation across industry. Intangible capital stocks derived from exit price parameters outperform existing measures when explaining market enterprise values and identifying human capital risk. Adjusting book values with exit-based intangible capital stocks markedly attenuates well-documented biases in marketto-book and return on equity ratios while increasing the precision of the HML asset pricing factor. We conclude that our capitalization parameters create intangible stocks that perform equal to or better than status-quo measures in various applications.

∗ Authors' email addresses: michael.ewens@columbia.edu, ryan.peters@tulane.edu and seanwang@smu.edu. The paper previously circulated under the title 'Acquisition Prices and the Measurement of Intangible Capital.' Special thanks to Dimitris Papanikolaou and Luke Taylor. We thank Gordon Phillips for providing data for the SDCCompustat merge and Shiyu Zhang for research assistance. Jan Bena (discussant), Nagpurnanand Prabhala (discussant), Hila Fogel-Yaari, Arthur Korteweg, Pierre Liang, Song Ma, Tom Ruchti and seminar participants at Columbia University, Cornell University (accounting and finance), University of Rochester, Michigan State University, University of Michigan, UT-Dallas, Southern Methodist University, Singapore Management University, National University of Singapore, HKUST, University of Hong Kong, CityU Hong Kong, University of Utah, Tulane University, Caltech, American Finance Association, Paris Financial Management conference, Washington University Conference on Corporate Finance, Midwest Finance Association, the Cass Mergers and Acquisitions Conference, and the Finance, Organizations and Market Conference (2018) provided helpful feedback. Code and data to incorporate the intangible capital measures can be found at: http://bit.ly/intan\_cap . First version: September 2018.

Corporate investment has transformed over the last few decades, with U.S. firms spending less on tangible assets and more on intangibles related to knowledge and organizational capital (Figure 1). This reduction in physical capital investments, along with the weaker connection between physical capital investments and firm valuation, is described as a 'broader investment puzzle' by Guti´ errez and Philippon (2017) and Crouzet and Eberly (2019). A shared conclusion of both papers is that standard investment measures on firms' balance sheets fail to capture the growing importance of intangible assets, resulting in a downward bias in the recorded book values of invested capital. 1 This bias has grown over time, as evidenced by the dramatic upward trend in market-to-book ratios.

Reliable measures of intangible capital are becoming increasingly important for capital markets and financial managers. For instance, numerous studies have provided evidence of mispriced equity for firms with higher levels of intangible capital, which could lead to suboptimal resource allocation. 2 In debt markets, banks are less willing to lend to firms with higher information asymmetry and more uncertainty about their liquidation values, two primary characteristics of intangible-intensive firms. 3 In corporate finance, financial managers making capital budgeting decisions must estimate book values of intangible capital to calculate returns to intangible capital (Hall, Mairesse, and Mohnen, 2010). To adjust for the downward bias in invested capital, researchers estimate the off-balance sheet intangible capital with accumulated flows of R&amp;D 4 , SG&amp;A 5 , or both. 6 Such adjustments require assumptions about the capital accumulation process, such as intangible depreciation rates and the fraction of SG&amp;A to be capitalized. Unfortunately, as Corrado, Hulten, and Sichel (2009)

1 Accounting rules for intangibles originated in 1974 when intangibles were a small proportion of the economy, and they have not changed, despite a fundamental change towards intangibles as economic value drivers. Specifically, internal Research and Development (R&amp;D) costs and Selling, General, and Administrative (SG&amp;A) activities are expensed, and thus intangible values do not appear on the balance sheet. Such expensing has been shown to reduce the overall usefulness of accounting statements (Lev and Zarowin, 1999).

2 A partial list of these studies includes Daniel and Titman (2006); Eberhart, Maxwell, and Siddique (2004); Aksoy, Cooil, Groening, Keiningham, and Yal¸ cın (2008); Edmans (2011); Eisfeldt and Papanikolaou (2013).

3 Williamson (1988); Shleifer and Vishny (1992); Loumioti (2012); Mann (2018)

4 Bernstein and Nadiri (1988); Chan, Lakonishok, and Sougiannis (2001); Hirshleifer, Hsu, and Li (2013)

5 Eisfeldt and Papanikolaou (2013, 2014); Belo, Lin, and Vitorino (2014)

6 Falato, Kadyrzhanova, Sim, and Steri (2022); Peters and Taylor (2017)

highlight, 'relatively little is known about depreciation rates for intangibles' (pp 674). While there is no clear consensus on parameter values, the most recently updated rates for knowledge capital depreciation use Bureau of Economic Analysis (BEA) data based on multiple data sets, including NSF surveys, where depreciation rates are based on the Li and Hall (2020) forward-looking profit model. Hulten and Hao (2008) provide the main parameter for organizational capital (hereafter, we refer to the combination of these parameters as 'BEA-HH'). These capitalization parameters, however, are limited by gaps in industry coverage. 7

We propose a capitalization model that uses the market values of intangible assets to estimate a new set of intangible capitalization parameters (hereafter referred to as 'Exits' or 'exit-based' parameters) from a firm's prior flows of intangible investments. Specifically, we obtain market values of intangible assets from firm exits that include acquisitions, liquidations, and bankruptcies. We identify the market prices of identifiable intangible assets and goodwill from these firms and match these prices to the firm's past spending on R&amp;D and SG&amp;A to estimate parameters that capture (1) the depreciation rate of prior R&amp;D investment in knowledge capital and (2) the fraction of SG&amp;A that represents an investment into organizational capital.

The results of our parameter estimation imply an average 33% annual depreciation rate for R&amp;D versus 23% for BEA R&amp;D depreciation rates where industry coverage is available. 8 Across industries, we find a significantly higher depreciation rate for the two industries with the highest R&amp;D intensity: healthcare (33% vs 17%) and high-tech (42% vs 28%). For organizational capital, we find that our 28% estimate of the fraction of SG&amp;A representing invested capital is similar to that used in earlier work (30%). However, while prior studies have assumed this ratio to be constant across industries, this ratio varies dramatically across industries, from 20% (consumer) to 51% (healthcare).

7 Approximately 46% of 4-digit SIC codes for public firms have depreciation rates for knowledge capital using BEA parameters found here: https://apps.bea.gov/national/FA2004/Details/xls/DetailNonres\_rate.xlsx . Organizational capital parameters have only been estimated in the pharmaceutical industry.

8 Some 53% of 4-digit SIC codes are missing depreciation rates for R&amp;D, and a depreciation rate of 15% is generally assumed by prior papers when a depreciation rate is unavailable for the given industry.

To assess the quality of these parameter estimates versus existing parameters, we develop a series of out-of-sample validation tests where we use our exit-based parameters to measure intangible capital and compare the results of our validation tests to those using estimated values of intangible capital against those derived from BEA-HH parameters. Utilizing a full panel of Compustat firms from 1978-2017, our primary validation test asks whether augmenting book values of invested capital with our intangible asset estimates improves their ability to explain market enterprise values. We find that exits-based intangible stocks improve the R 2 in year-by-year cross-sectional regressions in all 39 years (relative to BEA-HH) from 1978 to 2017. This additional explanatory power is statistically significant in all years.

Additional validation tests directly examine the association between economic outcomes and capitalized knowledge and organizational capital stocks. To begin, we examine whether our estimates of organizational capital better capture differences in human capital and brand value versus BEA-HH estimates of organizational capital. We follow Eisfeldt and Papanikolaou (2013) to test whether firms with high organizational capital are more likely to disclose risks regarding the potential loss of key talent in their 10-K filings. To do so, we analyze text from management discussions about risk in over one hundred thousand 10-K filings from 2002-2017 and identify whether the firm mentions 'personnel' or 'key talent.' Exits-based organizational capital measures more accurately sort firms into portfolios of high and low human capital risk versus BEA-HH based sorts. A similar exercise using firms' brand equity rankings corroborates the effectiveness of our measures in identifying organizational capital. Our final validation asks if and how our new estimates of intangible capital can explain previously established measures of patent values and trademark production. We find that Exits stocks explain marginally more of the R-squared in patent valuations from Kogan, Papanikolaou, Seru, and Stoffman (2017) and the number of new trademarks filed by a firm in a given year (Heath and Mace, 2020). Overall, we find that intangible capital stocks created from our Exits parameters are better associated with the expected economic outcomes relative to using BEA-HH parameters, with the documented improvements in the quality of our intangible stocks likely coming from industry-level variation in the organizational capital investment rate parameters and broader industry coverage in knowledge capital depreciation rates.

To illustrate how estimated intangible capital stocks may improve the usefulness of financial statements in empirical research applications, we incorporate our measure of capitalized intangible assets using Exits parameter estimates into several commonly used variables in corporate finance and asset pricing applications. Specifically, we calculate intangible adjusted measures of marketto-book ratios, returns on equity, and portfolio returns to the HML value premium factor. We find that using Exits parameters to adjust these values for intangible capital improves the usefulness of all three variables. First, the impact of incorporating intangibles when calculating market-tobook is economically large, and the importance of such an adjustment has increased with time. Since 1997, the unadjusted market-to-book ratio drifts have drifted upward by 0.04 per year, with the average book-to-market recently exceeding two in the 2010s. After adjusting book equity for missing intangible capital, this upward trend falls by 68%, demonstrating that unadjusted book equity measures are systematically understated. Next, we find a similar impact when exploring the effects of adjusting intangible capital on the return on equity. Adjusted ROEs fall 37% compared to the standard measure, and the final average mirrors the cost of equity capital estimates from the literature (e.g., Graham and Harvey, 2018; Damodaran, 2020). Finally, we show that adjustments to book equity for missing intangible capital shift 32% of firm-month observations away from their original HML portfolio assignment with unadjusted book equity values (Fama and French, 1992, 1993). Returns from an intangible-adjusted HML factor portfolio are higher with lower standard deviations when compared with the standard HML measure, implying that the inclusion of intangible capital increases the precision of HML portfolio sorts.

Given the importance of selection concerns for the representativeness of our parameter estimates, we compare the stocks from our exits price-based estimates to an alternative approach of using trading prices for intangibles' market prices. The parameter estimates we obtain from the publiclytraded prices have no sample selection issues. Repeating all the diagnostic tests of the implied stocks from this sample shows that the Exits parameters are superior (Internet Appendix Section A5). We also examine the quality of our organizational capital parameters against more granular industrylevel estimates based on a profit model from Iqbal, Rajgopal, Srivastava, and Zhao (2022). When paired with the standard BEA-based knowledge capital stocks, the Exits stocks also outperform the Iqbal, Rajgopal, Srivastava, and Zhao (2022) implied organizational stocks. Next, our inability to separately identify parameters requires we assume a fixed depreciation rate used in the literature when estimating the fraction of SG&amp;A that is investment. In a robustness test we find that other parameter estimates do not depend on this assumption (Figure 10). Finally, we provide a battery of robustness checks (Section 7) to assess the role of each major assumption with our sample choice and find that our adjustments to reported goodwill and inclusion of liquidations are important for the estimates' superior performance.

We contribute to three broad literatures. First, we provide parameter estimates to corporate finance researchers that rely on estimates of intangible capital as an input to examine real outcomes in firms (Eisfeldt and Papanikolaou, 2013; Gourio and Rudanko, 2014; Sun and Zhang, 2018). Second, we contribute to a long-standing literature on growth economics that attempts to measure the value of knowledge in the economy. Specifically, our work both re-estimates the knowledge capital accumulation process using market prices and extends these estimates to organizational capital for the first time (Corrado, Hulten, and Sichel, 2009; Corrado and Hulten, 2010; Acemoglu, Akcigit, Alp, Bloom, and Kerr, 2013; Hall, Mairesse, and Mohnen, 2010). Finally, we contribute to an active debate surrounding off-balance sheet intangible capital. Lev (2018) suggests that standard-setters' resistance to recognizing intangibles on firm balance sheets has substantial costs to both firms and the broader economy. In addition to confirming the value-relevance of currently included intangible assets such as goodwill, we provide evidence that estimating the value of internally generated intangible capital is feasible and provides meaningful information to financial statement users.

## 1 A framework for estimating intangible capital

While book values of physical assets are periodically reported on the balance sheet at the original market price of the purchased investment less the asset's total depreciation (i.e., net book value), the same values for intangible assets typically go unreported. Such exclusions come despite the importance of a firm's intangible capital in generating economic value. We present a methodology motivated by the process for measuring physical asset values to accurately estimate intangible capital stocks for U.S. publicly-listed firms.

Physical asset depreciation and the resulting net book value rely on a set of accounting depreciation rates, which are generally industry-level norms (e.g., estimated useful lives for straight-line depreciation). So, we begin by detailing an estimation approach for industry-level intangible depreciation rates-i.e., the fraction of assets depreciated over a year-and combine these parameters with the values of prior intangible investment flows to compute these intangible capital stocks.

<!-- formula-not-decoded -->

Here, an asset in the current period t , K t , evolves by adding current period investment Z t to the previous period stock K t - 1 , net of periodic depreciation D t . Let δ be the periodic depreciation rate for K t - 1 . Assuming geometric depreciation, (1) can be rewritten as:

<!-- formula-not-decoded -->

The identity in (2) provides structure for estimating δ . Assuming K 0 = 0 and via iterative substitution, we arrive at (3), where the intangible capital stock (i.e., the net book value) is the aggregation of all undepreciated intangible investments since firm birth: 9

<!-- formula-not-decoded -->

To estimate the intangible depreciation rate, δ , in (3), we need data for K t and Z t - k . While each firm generally reports values for Z t - k on the income statement, they do not self-report estimates of K t . Ideally, a well-functioning marketplace that reports current prices of these depreciated assets would be a data source of net book values K t . While some marketplaces like these exist for physical assets such as PP&amp;E and real estate, this is generally not the case for intangible assets. Market prices for intangibles are difficult to obtain because many intangibles are unique and developed for internal use. Furthermore, these investments are generally not divulged to competitors for strategic reasons. Section 2 describes how we infer the prices of intangible assets from the market values of firm exit prices to obtain estimates of K t .

Motivated by prior research that bifurcates intangible capital into two sub-components, we express firm i 's total intangible capital stock at time t , K it , as the sum of knowledge capital, G it , and organizational capital, S it . Knowledge capital relates to information learned about processes, plans, or designs that can lead to economic benefits in future periods. Prior literature uses Research and Development (R&amp;D) expenses as a proxy for periodic investment in knowledge capital. While the definition of organizational capital is more vague, 10 the consensus in the literature is to use some fraction ( γ S , discussed further in Section 3 below) of Selling, General, and Administrative Expenses (SG&amp;A) to represent the periodic investment in organizational capital. Total intangible

9 Due to data limitations on intangible expenditures such as unobservable accounting expenditures prior to the firm being publicly-traded, (3) is often modified as follows:

<!-- formula-not-decoded -->

where K t - k is an initial intangible capital stock.

10 Evenson and Westphal (1995) define organizational capital as knowledge used to combine human skills and physical capital into systems for producing and delivering want-satisfying products. Lev and Radhakrishnan (2005) define organizational capital as technologies such as business practices, processes, and designs that give a firm a competitive advantage.

capital can now be written as K it = G it + S it . Because both G and S evolve as in equation (3), we have:

<!-- formula-not-decoded -->

where δ G and δ S are the knowledge and organizational capital depreciation rates, respectively. Recall that if δ G and δ S are unbiased measures of economic depreciation for G and S , we can substitute the net book value with its price (i.e., K it = P I it ). This step assumes that prices for intangible assets are derived from firms which are price-takers with constant returns to scale and thus that average Q will approach a marginal Q of one (Hayashi, 1982). To the extent that there are exceptions, let ξ be the market-to-book ratio. Equation (4) becomes:

<!-- formula-not-decoded -->

From (5), we see that depreciation rates δ G and δ S combine with prior investment flows of R&amp;D and SG&amp;A and the intangible market-to-book ratio to give the total market price of the firm's intangible capital. 11

Finally, adjustments are required before we take (5) to the price data discussed below. To avoid weighting firms by size and without an obvious scaling variable, we take the natural logarithm of (5). Intangible asset prices and investments are likely measured with error, which we capture with the error term ϵ it . The adjustments lead to our baseline estimating equation:

<!-- formula-not-decoded -->

With price ( P I it ) data, the values of periodic investment (R&amp;D it , SG&amp;A it ) and modifications to adapt the model for real-world data, we can estimate parameters using non-linear least squares. The resulting parameters allow us to recapitalize knowledge and organizational capital over a large panel of firms. 12

11 Firms may have zero intangibles and/or zero R&amp;D and SG&amp;A. So we add one to both the left-hand side and to the term in the parentheses in (5).

## 2 Intangible asset market valuations from exit prices

We obtain P I it from a sample of firms whose intangible assets are valued by the market in exits. This sample consists of a set of firms that allow us to derive the market values of intangibles from public firm acquisitions of other public firms and recovery asset values for firms that delisted from publicly traded markets due to bankruptcy. With acquisitions, asset appraisals owing to an acquisition undergo an extensive due diligence process by expert appraisers that result in precise valuations. Accounting regulations (ASC 350) require that intangibles being purchased by the acquirer are directly recorded at market value on the acquirer's balance sheet as either Identifiable Intangible Assets (IIA) or goodwill (GW). Subsequently, P I it is calculated as the sum of IIA and GW. Most importantly, because our model relies on the value of total intangibles, we need only trust the valuation of physical assets and liabilities since the sum of IIA and GW equals the difference between the firm's mark-to-market net (physical) assets and the acquisition purchase price. The valuation of these physical assets and liabilities has a long history with standardized practice. 13

We acknowledge two concerns related to our acquisition setting. The first relates to goodwill. Because our goal is to precisely measure the target firm's stand-alone values of organizational and knowledge capital, and prior studies (e.g. Roll, 1986) have shown goodwill to be related to overpayment and acquisition-specific synergy values, we remove these factors from goodwill. What remains is a value that proxies for unidentifiable intangible assets. Specifically, we use the probability scaling method from Bhagat, Dong, Hirshleifer, and Noah (2005) and apply this to announcement day returns to estimate the synergy and over-payment component of the acquisition. The method-fully detailed in Appendix Section A1.2-uses changes in target and acquirer market valuations in response to the acquisition announcement to estimate synergies. This estimate of acquisition-specific value is subtracted from the goodwill value reported in the purchase price allocation. 14

12 Since the model is in logs, model fit is assessed by comparing the exponent of the error term generated by the model to the exponentiated error term of a model that uses only a constant in the estimation. Because the model does not contain a constant, a negative pseudo R 2 is possible. We calculate standard errors by bootstrap, re-drawing price observations, and thus the full time-series of company investments, with replacement.

13 Section A2 of the Internet Appendix provides several real-world examples found in our data.

The second concern relates to the non-random selection of acquired firms: acquisition targets may not be representative of the full population of firms. For example, empirical evidence suggests that acquirers may target firms with better than average innovation efficiency as part of a firm growth strategy (Phillips and Zhdanov (2013); Bena and Li (2014)). To address this concern, we expand the sample of acquired firms to include firm exits from bankruptcies and liquidations of publicly-traded companies over the sample period. For these exits, we estimate P I it by collecting recovered asset values from Moody's Default and Recovery database (DRD) and multiplying by the average ratio of intangibles scaled by total assets, which we calculate from acquisitions in the same 4-digit SIC code. 15 When the recovered asset values are not available in the DRD, we estimate recovery rates using the modified Fama French 5 industry average recovery rates from the Moody's DRD. This recovery rate, multiplied by the outstanding debt, forms the 'deal value' for these firms.

Ultimately, our goal is to improve the measurement of intangible capitalization parameters that allow us to create more accurate measures of intangible capital stocks than existing methods. We acknowledge that it may be difficult to create a sample of intangibles whose market prices perfectly represent the full population of firms. For example, it may be the case that acquisition targets have unsuccessful prior intangible investments and supplementing the sample with liquidating firms does not remove the sample bias. In such instances, we acknowledge that such bias will be reflected in sub-par performance of our exit-based stocks in validation tests that use the full panel of firms. As such, we allow the efficacy of our adjustments to address noisy goodwill and non-random selection to be dictated by the empirical results of the validation tests we develop in Section 7. Internet Appendix Section A1 provides more details on the goodwill and selection issues with summary statistics on the firms in the sample and the role of goodwill in acquisitions.

14 In 15% of cases where the adjustment exceeds goodwill, the remainder is removed from the IIA valuation.

15 This file covers large public U.S. corporate defaults from 1987-2019, and includes the final recovery of total debt based on 10-K, 10-Q, press releases, and other legal filings. The data field named 'FAMILY RECOVERY' provides the dollar-weighted proportion of debt recovered. We use FF5 industry average recovery rates from the same database for the remaining firms (49% across all firms). This recovery rate multiplied by outstanding debt forms our 'deal value' for this sample of firms.

It is still possible our proposed adjustments to the Exits sample fail to fully address the selection and valuation issues. Therefore, Internet Appendix Section A3 provides nearly all the diagnostic and validation tests below using an alternative measure of intangible asset values that we call 'trading.' Using the universe of CRSP-Compustat public firms, we take the market enterprise value and subtract an estimate of the market value of tangible assets, leaving us with the market value of intangible assets. While this approach can apply to all firms with publicly traded prices, it demands that we estimate the markup of each firm's tangible assets (reported to the books at historical cost) to market value. We follow prior literature from Erickson and Whited (2006, 2012) and Peters and Taylor (2017) and use gross PPE to proxy for the market value of tangible assets in the estimation. This sample of intangible values removes concerns about sample selection bias but comes at the cost of requiring an assumption about the mark-up. Section A5 discusses how the intangible stocks built from the estimated parameters from the trading prices underperform our proposed method.

## 2.1 Data sources

We obtain data for R&amp;D and SG&amp;A from Compustat. Data on acquisitions, liquidations, and bankruptcies come first from Thomson's SDC Merger &amp; Acquisition database. We consider all U.S. public acquirers and public targets for deals that closed between 1996 (the year in which SEC required all firms to provide financial statements to EDGAR) and 2017 with a reported deal size. We drop deals where the acquirer or target has a financial services, resources, real estate, or utility SIC code. 16 We also exclude all deals that use the pooling method pre-2001. We also require data on the acquirer's purchase price allocation of the target's assets to collect prices paid for goodwill and identifiable intangible assets (IIA). When available, these purchase price allocations were found in the acquirer's subsequent 10-K, 10-Q, 8-K, or S-4 filing. We found information on the purchase price allocation for 81% (1,719) of all candidate acquisitions. In the final step, we merge the target and acquirer firms to Compustat and CRSP, leaving us with 1,523 acquisition events. We add to this sample a set of 481 bankruptcy events from CRSP firm delistings between 1996 and 2017. We can find direct matches on asset recoveries from Moody's Default and Recovery Database for 95 of these events and use the estimation process described in Section 2 to estimate asset recovery for the remainder. In total, our panel of exit prices consists of 2,004 firm observations.

16 The excluded SICs are 6000 to 6399, 6700 to 6799, 4900 to 4999, 1000 to 1499.

## 3 Parameter estimation

This section details the remaining assumptions and data issues for the baseline estimation.

## 3.1 SG&amp;A, gamma and delta

Recall that organizational capital stems from capitalizing Selling, General, and Administrative Expenses (SG&amp;A). Because of its broad GAAP definition, SG&amp;A aggregates a variety of spending for various operating activities. Thus, researchers must assume some proportion of total SG&amp;A flows represents organizational capital investments. 17 We define this proportion as γ S ∈ (0 , 1]. Incorporating γ S introduces a complication to any estimation of equation 6. The relative stability of R&amp;D and SG&amp;A within firms over time, along with the multiplicative functional relationship between the parameters, means that we cannot separately identify the parameters γ S and δ S in each capital accumulation process. 18 We address this issue by reducing the parameter space by calibrating a subset of parameters. In particular, we estimate the parameter γ S taking the depreciation of organizational capital δ S as the standard 20% from the literature. 19 The estimating equation becomes:

17 For example, employee training and advertising expenses should be capitalized because their economic benefits extend beyond the current period, while others, such as rent and wage expenses, should not be capitalized since they represent payments for services rendered for a specific period.

<!-- formula-not-decoded -->

## 3.2 Market-to-Book parameterization

We aim to improve upon existing parameters that allow us to capitalize off-balance sheet intangibles. In 2013, there was a comprehensive update of the national accounts whereby the BEA now recognizes R&amp;D expenditures as an investment. Thus, the BEA now requires and publishes the estimated R&amp;D depreciation rates used in the intangible capitalization. Using a forward-looking profits model based on Li and Hall (2020), the BEA estimates depreciation rates based on the decay rate at which a firm's prior intangible investments contribute to firm profits. To map the decline in profits to the depreciation of capital, researchers must assume a rate of return on these intangible investments. Li and Hall assume that the marginal realized rate of return equals the firm's expected return, i.e., they assume zero-excess returns in equilibrium, which is equivalent to the assumption that marginal Q for knowledge capital equals one.

Because our model estimates parameters to allow us to identify the net of depreciation intangible stock and maps them to intangible market prices, we require an assumption about the average Q of our intangible capital stocks. We follow Hall (2005) who assumes that R&amp;D average returns

18 e.g., for SG&amp;A, consider the perpetual inventory equation for a firm i : S it = ∑ k γSG &amp; A i,t - k (1 - δ S ) k . In the extreme, if SG &amp; A it is constant for firm i , SG &amp; A it = SG &amp; A , we have:

<!-- formula-not-decoded -->

Whether within-firm variation in SG&amp;A or R&amp;D is enough to separately identify γ S and δ S is an empirical question. We find that it is not and any estimate of, e.g., γ S , is ultimately tied to its calibrated counterpart.

19 We explore the implications of this assumption by running a sensitivity analysis on varying values of δ S on changes in the magnitudes of intangible capital stocks in Section 7.1 and find that changes in the calibration of δ S are largely offset by changes in the estimated γ S , leaving the resulting model fit and capital stock relatively unchanged.

are equal the cost of capital, tantamount to imposing an average Q of unity. These conditions are identified in Hayashi (1982), where the firm is a price-taker with constant returns to scale. We relax the rigidity of this assumption for any particular firm or year, only imposing that average market-to-book equal one over the full panel. This is done by parameterizing ξ , i.e., industryyear M/B intangible ratios as industry-year fixed effects. The estimation simply requires that the average of the estimated industry-year fixed effects within each industry be one within the sample (technically, the log of the fixed effects is zero). This approach allows for industry-year exceptions (e.g., high industry growth periods (recessions) where firms within a particular industry have a M/B ratio greater (less) than one within the time series. 20 We acknowledge that, to the extent that our assumptions of M/B reflect error for a particular industry-year, that such error will be ultimately reflected in poor performance in the validation tests. 21 Defining the industry-year fixed effect parameterization of ξ as ρ jt , where j is industry, we arrive at the following:

<!-- formula-not-decoded -->

Equation (8) is estimated using non-linear least squares 22 using the intangible prices data (Section 2) and firm-year financial data from Compustat. 23

20 For example, the distribution of M/B within year and across firms is fully flexible. We only require that the mean of these distributions' means are one across years. In fact, no firms could have M/B = 1 and the average could be one. We also estimate the parameters and all validation tests imposing year fixed effects for ρ t , with little quantitative change in the results.

21 For example, if our M/B assumptions were too low, then parameter estimates of δ G ( γ S ) would be biased downward (upward).

22 The estimation minimizes the sum of squared deviations ( ϵ it ) while enforcing the constraint by adding to this objective function the sum (across industries) of the squares of the mean (across years) of the industry-year fixed effects multiplied by a very large number (100,000).

23 If a firm has any acquired intangible assets at the time of acquisition, bankruptcy or calculation of intangible value from trading prices, then we add it as I it to the second term on the right-hand side of (8).

## 3.3 Previous approaches to estimation depreciation parameters

Before presenting our results, it is important to highlight earlier approaches to this empirical problem. We are not the first to estimate the depreciation parameters in intangible asset capitalization, though we are the first to use market-based prices for the estimation. To our knowledge, the only estimate of γ S comes from Hulten and Hao (2008). They estimate it based on descriptions of income statement items from six pharmaceutical firms in 2006, applying the investment share of expensed items from Corrado, Hulten, and Sichel (2006). Conversely, there have been several attempts to estimate the depreciation rate for R&amp;D investments ( δ G ). Most models that estimate R&amp;D depreciation propose a channel through which knowledge capital affects firm behavior or outcomes. Pakes and Schankerman (1984), for example, develop a model by which they infer δ G by examining the decline in patent renewals over time. This assumes that the value from R&amp;D is realized through patents and is directly inferred from patent renewal. Lev and Sougiannis (1996) assume that the depreciation of knowledge capital enters the production function directly and estimates a depreciation model by regressing firms' current period operating income on lagged values of R&amp;D expenditures. The BEA depreciation parameters for knowledge capital are based on a productionfunction-based model in Li and Hall (2020). Their estimated parameters are based on NSF-BEA data and cover a little over half of firm-years in Compustat, thus requiring other assumptions for firms in SIC codes outside these estimations.

In summary, the lack of a consensus for δ S and δ G has led to a wide range of parameters being used to capitalize internally generated intangibles. To benchmark our market-price-based capitalization parameters, we use the current set of published BEA knowledge capital depreciation rates for each 4-digit SIC code-year where available 24 and 15% otherwise, an approach that has become common in recent years (see cites to Peters and Taylor, 2017), while using the estimate that 30% of SG&amp;A represents an investment into organizational capital with a depreciation rate of 20% per year. We refer to this benchmark as 'BEA-HH' in subsequent validation tests.

24 BEA knowledge capital depreciation rates are listed as Asset Code IP00, Intellectual Property Products, and are available at https://apps.bea.gov/national/FA2004/Details/xls/DetailNonres\_rate.xlsx .

## 4 Capitalization parameter estimates

This section presents the results of our estimation of equation (8). Before discussing the parameter estimates for δ G and γ S , Figure 2 reports the distribution of the estimated industry-year fixed effects across the Fama-French 5 Industry Classifications.

Each industry 'violin' represents a mirrored density plot of all time-series observations for a particular industry. The 'dot' reports the median and the 'x' reports the mean of the estimated fixed effects. While the median M/B values across all industries approach one, our flexible estimation approach allows for significant variation within industry-year, with roughly 50% of all industry-year intangible market-to-book ratios either exceeding 1.4 or falling below 0.8.

Table 1 reports Exits parameter estimates from Equation (8) using exit prices. For comparison, columns (1) and (2) report BEA-HH parameters where δ G coefficients are equal-weighted averages for each SIC4-year within the listed FF5 Industry Classification and γ S is 0.30 from Hulten and Hao (2008). Column (3) reports the percentage of firms within each sector of the Compustat sample for which BEA depreciation rates are available (i.e., they are not imputed to 0.15). Recall that δ G represents the depreciation rate of R&amp;D capital, and γ S represents the proportion of SG&amp;A that is to be classified as a long-lived asset. Thus, Equation (8) tells us that lower (higher) values of δ G ( γ S ) will lead to higher levels of G it ( S it ).

Consider first γ S in the 'All' row, relative to the 30% used in the literature. We estimate a similar but slightly smaller value of 28% using the Exits data. Additionally, while prior estimates assume a constant ratio of 30% across all industries, we find a large degree of industry-wide variation in γ S , the fraction of SG&amp;A representing an investment. For the knowledge capital depreciation parameter, δ G , the Exits estimates for 'All' (33%) are significantly higher than the BEA's estimate (23%). Overall the combination of the Exits parameters having a higher δ G and a lower γ S relative to BEA-HH indicates that, on average, Exits stocks will have smaller levels of intangible capital than BEA-HH stocks. To the extent that the Exits parameters developed from market prices more accurately reflect the true values of γ S and δ G , intangible stocks developed from Exits estimates will outperform the stocks developed by BEA-HH parameters when both sets are subjected to the validation tests in Section 5.

## 5 Validation tests

Given our goal of improving upon existing estimates of capitalization parameters, we assess the performance of our Exits parameters against BEA-HH by running an array of validation tests on our resulting capital stocks. In designing such tests, we have two goals. First, the estimated intangible capital stocks should proxy for the expected future benefits the intangibles will provide to their owner. Second, applying the stocks to create new total invested capital should strengthen those stocks' relationship with other cross-sectional measures of intangibles. All these validation tests are out of sample . That is, to avoid circularity that would result in better validation test performance of our stocks over those using the BEA-HH parameters, we exclude from the analysis any firm-years used in the Exits parameter estimation. Using estimates from the industry-level parameters in Table 1, we construct the knowledge and organizational capital stocks G it and S it , as well as total invested capital (including intangible capital) K TOT it using 10-years of trailing R&amp;D and SG&amp;A data from 1976-2018 for the CRSP-Compustat universe of firms. Our accumulation process for knowledge and organizational capital follows (4). Total invested capital is the sum of knowledge and organizational capital stocks, the book value of externally acquired intangibles, and the book value of physical capital.

The following subsections describe the motivation of each test and report the results when comparing stocks of BEA-HH vs Exits parameters. In section 5.4, we summarize the results of these tests.

## 5.1 Explaining market valuations

The first diagnostic test examines changes in the informativeness of book values of invested capital in explaining market enterprise values when total invested capital is adjusted for off-balance sheet intangibles. Connections between a firm's book invested capital and market enterprise value play important roles in the investment-q and asset pricing literatures. Book values, when properly measured, reflect the firm's capital investments that are available to produce future cash flows. Market values reflect investor expectations of these discounted future cash flows. To the extent that intangible capital stocks have been properly measured and are now reflected in total book invested capital, we expect a stronger association between market enterprise value and book invested capital. We use a simple regression of firm enterprise value on measures of total invested capital to evaluate the new intangible asset estimates:

<!-- formula-not-decoded -->

where E it is i 's year t enterprise value (i.e., the sum of end of fiscal year market capitalization, total debt and preferred stock) and K TOT it is the book value of the capital stock (Compustat at ) adjusted for capitalized intangibles. That is, K TOT it is equal to K Phy it + K Int it where K Int it is the sum of externally acquired and internally generated intangibles from Exits and BEA-HH capitalization parameters. More precise measures of intangible capital will be reflected in total invested capital measures that have the strongest associations with market enterprise values.The diagnostic test reports the annual ratio RSS BEA - HH - RSS Exits RSS BEA - HH which reports the degree to which the fit between book invested capital and market enterprise value has improved relative to BEA-HH. Panel (a) of Figure 3 presents the results of the test statistic by year. Panel (b) reports the t-statistic of the hypothesis test for no difference in R 2 between BEA-HH and Exits.

Overall, the Exits capital stocks outperform BEA-HH capital stocks in explaining market enterprise values (panel (a)), while the t-statistics in panel (b) show that the R 2 is statistically larger when we use the Exits stocks across the entire 39-year sample period. Again, these regressions exclude the companies in the estimation (avoiding circularity). Overall, these results demonstrate that the capitalized intangibles using the parameter estimates from Table 1 have the most predictive power for explaining enterprise value.

## 5.2 Validation tests of organizational capital

We employ two diagnostic tests to assess the quality of our organizational capital measures: human capital risk and brand quality.

## 5.2.1 Human capital risk

Eisfeldt and Papanikolaou (2013) propose a model whereby organizational capital is a firm-specific investment that has outputs measured by a firm's key talent. Their model shows that the outside option of the firm's key talent determines the share of the firm's cash flows that accrue to shareholders. Thus shareholders bear more risk for firms with higher levels of organizational capital. They estimate the stock of organizational capital by capitalizing a firm's SG&amp;A expenses and validate their measure by examining the MD&amp;A of firms with higher (lower) levels of organizational capital, and showing that firms with higher (lower) levels are more (less) likely to disclose the potential for key personnel loss as a significant risk factor to the firm. To do so, they seek out references for personnel risk in 10-K filings and argue that any firm sorting by a measure of organizational capital should correlate with such mentions. We follow a similar approach, using over 120,000 10-K filings from 2002-2016. We calculate the fraction of words in the MD&amp;A statement that reference the risk of personnel loss (keywords: 'personnel,' 'talented employee,' or 'key talent').

Because an improved organizational capital measure will more precisely sort firms into the highest (lowest) quintiles of human capital risk, we expect such a measure will have more (less) frequent mentions of personnel loss as a risk factor in the firm's MD&amp;A. Thus, our diagnostic test compares the relative performance of Exits-based organizational capital stocks with Hulten and Hao-based organizational capital stocks that use a constant ratio of SG&amp;A investment to be capitalized, γ s = 0 . 3. Both Exits and HH organizational capital stocks assume δ S = 0 . 2. We sort firms into quintiles based on their estimates of organizational capital stock scaled by assets in each year, then calculate the frequency of mentions between the high and low quintiles by year for both Exits and HH measures of organizational capital. Figure 4 reports the t-statistic by year from the difference in frequency means for the top versus the bottom quintile of firms in these sorts.

With exits-based stocks, the fraction with some reference to personnel risk in the top quintile versus the bottom is 65% and 51%, respectively. This compares to 59% and 52% for the quintiles sorted using the HH ( γ S = 0 . 3) method from the literature. The difference between top and bottom quintiles for Exits are positive in all years of the sample and significant in all but two years of the sample, while the HH stocks are insignificant in seven of the 14 years in the time series, indicating that the exits-based measure of organizational capital stock is better able to identify human capital intensive firms and the subsequent risks associated with these firms.

## 5.2.2 Brand quality

Another well-documented subset of firms' organizational capital is brand quality (Vomberg, Homburg, and Bornemann, 2015; Mizik and Jacobson, 2008). Our second validation test asks whether our organizational capital stocks (and total intangible capital) exhibit stronger associations with brand quality. We collect the top 100 global brands according to Interbrand, a brand consultancy, from 2000 to 2018. 25 We extract the ranking and merge each company (or brand) to U.S. public firms in Compustat. 26 This diagnostic test is a simple fit test where we regress the log of a firm's brand rank on the log of organizational capital (and the log of total intangible capital). Thus, more precise measures of intangible capital will have stronger associations with brand quality, thus leading to higher R 2 in the regression analyses. Table 2 reports the pooled regression results.

Columns (1)-(2) use the log of organizational capital as the independent variable, while columns (3)-(4) use the log of total intangible capital. Results indicate that the coefficients on organizational (total intangible) capital load negatively for both of our price-based stocks as well as stocks based on HH parameters. These findings show that firms with higher organizational capital stocks have higher brand equity. Relative to HH, the Exits price-based stocks show the largest improvement for organizational capital ( R 2 in columns (2)), and a more modest improvement when testing total intangible capital ( R 2 in columns (4)).

[25 Data available at https://www.interbrand.com/best-brands/best-global-brands/previous-years/2000/ .](https://www.interbrand.com/best-brands/best-global-brands/previous-years/2000/)

26 If two brands from the same firm are on the list, we take the average rank within-firm.

## 5.3 Validation tests of total intangible capital

The final three validation tests evaluate outputs associated with investments in both knowledge and organizational capital.

## 5.3.1 Patent valuations

Prior literature (Hall, Jaffe, and Trajtenberg, 2005; Subramaniam and Youndt, 2005; Dakhli and De Clercq, 2004) finds that innovation is related to both knowledge and human capital. We use patent valuations from Kogan, Papanikolaou, Seru, and Stoffman (2017) as a measure of innovation quality and examine the association between our total intangible capital measures and innovation. Let the patent valuation for firm i in year t be Patent it (set to zero if missing). The regression takes the following form:

<!-- formula-not-decoded -->

where X it - 1 is the number of patents held by the firm. This diagnostic test incorporates alternative measures of ˆ G it - 1 and ˆ S it - 1 . Better performance is captured with a higher R 2 from (9). 27 In Panel (a) of Figure 5, we report the ratio of two values of R 2 , where the benchmark (denominator) is the R 2 using estimated intangible capital stocks from the BEA-HH method and the numerator is the R 2 using the exits-based intangible capital stocks. Results show only a modest increase in explanatory power for exits-based intangible capital stocks, although the improvement appears consistent across our entire time-series of patent data.

27 Untabulated, we find that β 2 is positive and significant with all capital stocks.

## 5.3.2 Trademarks

Similar to the patent analyses in Section 5.3.1, the second validation test examines ratios of R 2 from regressions of newly filed trademarks on total intangible capital. The numerator (denominator) is the R 2 from stocks accumulated by the Exits parameters (BEA-HH parameters). The intuition is that firms with higher levels of intangible capital will have, on average, more powerful brands. In order to protect their brand equity, they will file for trademark protection. Using data provided by Heath and Mace (2020), we regress the count of new trademarks on total intangible capital by year. The regression takes the same form as (9) where patents are replaced by a count of trademarks (plus one), and the X it - 1 is the firm's lagged trademark stock. Panel (b) of Figure 5 reports the results. Overall, results appear similar to those discussed in Section 5.3.1, with exits-based intangible capital demonstrating only a marginal improvement over BEA-HH stocks for all sample years when explaining the number of trademarks held by the firm.

## 5.4 Summary of validation tests

Overall, we find that adjusting the firm's invested capital using Exits intangible stocks does a better job of explaining the firm's market enterprise value relative to intangible capital adjustments made using BEA-HH parameters. These improvements are statistically significant (p &lt; 0.01) in all of our sample years from 1978-2017. In further comparisons of Exits intangible capital stocks (relative to BEA-HH) across a wide array of direct outputs from intangible investments, we perform additional validation tests that examine whether exit-based stocks improve explanatory power for human capital risk, patent valuations, trademark counts and brand equity rankings. In these separate tests, the increase in explanatory power is largest for human capital risk, while in other tests the exits stocks perform either no worse than or show marginal improvement versus those derived from BEA-HH parameters. Again, we note that any potential concerns for developing parameters from exit prices (i.e., noisy goodwill, bankruptcy recovery rates, assumptions regarding marginal Q) should not be downplayed but rather weighed against the improved performance in this range of out-of-sample tests. In addition, Internet Appendix Section A3 reports an alternative priced-based estimation using non-selected traded equities and shows that the exits-based stocks exhibit superior performance.

## 6 Descriptive analysis of exits-based intangible stocks

This section provides summary statistics of the exits-based intangible asset stocks.

## 6.1 Comparison to existing methods

Figure 6 presents the percent difference between Exits and BEA-HH estimates of capitalized intangible stocks, scaled by the latter. The differences in our estimated intangible capital stocks relative to BEA-HH vary across industries. For example, while the 'All' line in the figure shows that the new estimate is approximately between 18% and 25% smaller across all firm-years, our intangible stocks are larger, on average, for high-tech firms particularly in the earlier part of the sample. Given the larger estimated depreciation of R&amp;D for Exits healthcare stocks (33%) versus BEA-HH healthcare stocks (17%), the declining relative size of Exits stocks in healthcare across the time series reflects firms' shift from organizational capital to knowledge capital investments. Overall, we document economically meaningful differences in the magnitude of implied stocks across industries compared to BEA-HH.

## 6.2 Intangible capital stocks by industry and time

Figure 7 presents time series trends of intangible capital for the four industries. Each series plots intangible intensity, calculated as the average ratio of intangible capital K int ( S it + G it + I it ) to total assets, e.g., intangible and physical assets (Compustat ppegt ). The increasing levels of intangible asset intensity across all industries match the well-documented expanding role of intangibles in the economy. Consistent with our expectations, intangible intensities are lowest in consumer and manufacturing and highest in healthcare and high tech. These patterns conform to basic predictions about differences across industries and time and validate that our estimates measure real economic assets.

## 6.3 Intangible capitalization's impact on market-to-book and ROE

Next, we re-examine the time series behavior of market-to-book ratios with these new capital stocks and compare them with the time series behavior of unadjusted market-to-book ratios. We calculate the average market-to-book equity ratios from the period 1997-2017 for both sets of capital stocks and run the following regression:

<!-- formula-not-decoded -->

Figure 8 reports two time-series plots with best-fit lines for the unadjusted M/B and the M/B adjusted with the Exits stocks. When off-balance sheet intangibles are not capitalized in book value, the M/B ratio drifts upwards by 0.04 per year. After our adjustments for intangible capital, the slope coefficient becomes 0.013, a decrease of 68%.

A similar result can be seen when adjusting a firm's return on equity (ROE), which is calculated as net income scaled by the book value of common equity (start of the year). Because intangible investments are expensed and do not appear on a firm's balance sheet, both the numerator and denominator of the ratio are biased. The denominator is missing the value of off-balance sheet intangibles, while the numerator nets out the current year's intangible investment while ignoring the depreciation of off-balance sheet capital. The downward bias in the book value of equity results in an upward bias in unadjusted ROEs due to the expensing of intangible capital. Assuming competitive markets, long-term averages of ROE should approach the market's cost of equity capital. While it is beyond the scope of our study to debate the market's cost of equity capital, we rely on some agreement from the literature. Graham and Harvey (2018) surveyed CFOs from 2000-2017 and found an equity risk premium of 4.42%, while Damodaran (2020) finds an implied equity risk premium using a free cash flow to equity model of 4.33% from 1978-2017. Adding these values to the 10-year T-bond rate of 6.16% from 1978-2017 results in expected market-wide returns on equity of 10.58% and 10.49%, respectively.

Figure 9 displays the impact of incorporating intangibles into the ROE calculation across our panel of firms from 1978-2017. It plots the unadjusted average annual ROE across the entire sample (dashed) and the average annual ROE (solid) after adjusting both the numerator and denominator for the capitalization of intangibles. 28 These adjustments for intangible capital lower the average annual ROE from 16.82% to 10.53% (untabulated), a decrease of 37%, and are closely in line with expectations based on Graham and Harvey (2018) and Damodaran (2020). Finally, we note that the degree of ROE bias-the unadjusted ROE less the Exits adjusted ROE (scatter and dotted linear fit)-has steadily risen over time. This rise is consistent with increasing intangible intensity over time and further highlights the importance of capitalizing intangibles.

## 6.4 Asset pricing factors

The multi-factor Fama-French (FF) model (e.g., Fama and French, 1992, 1993) is widely used in calculating expected returns. One key component in the FF model is HML (high-minus-low), the realized returns to a portfolio that is long (short) high (low) book equity-to-market equity firms. Given that current accounting standards prohibit the capitalization of internally generated intangible investments, book equity values will be depressed by the amount of intangible capital. As a result, we expect some proportion of firms in a traditional FF HML portfolio sort to be misclassified relative to an HML sort that uses our exit-price parameters that adjust for intangible capital. Table 3 documents the consequences of these misclassifications on the observed return.

Columns 1 and 2 show that monthly return spreads are 90% larger, 37.3 vs 19.6 basis points (p = 0.02), upon the adjustment for intangible capital to the numerator. Upon further exploration, we find that 68% of firms are correctly sorted to the proper (low, mid, high) B/M portfolio, i.e., they do not move across portfolios after intangible capitalization, and that the return spreads are nearly identical 37.3 vs 38.6 bp) between the adjusted portfolio and the FF portfolio using only properly sorted firms. Thus, the large difference in observed return spreads must be driven by the missorted firms. Column 5 shows that 30% (22%) of firm-month observations in the traditional FF sort have substantially high (low) intangible capital such that they transition out of the short (long) sides of the portfolio. Column 6 shows the returns in each B/M portfolio for these misclassifications and finds that the well-documented HML relationship not only disappears but also exhibits negative return spreads ( - 21 bp). While the conclusive mechanism of why HML is predictive of future returns is beyond the scope of our paper, Korteweg (2010) has shown that higher intangible firms have greater distress risk, while Edmans (2011) has documented that stock market under-reacts to the value of intangible capital. Our empirical results are consistent with such possibilities and highlight the importance of capitalizing intangibles when HML is used in asset pricing tests.

28 Our adjustment to net income is: NI adj it = NI it +(RD it + γ s SGA it - G it δ G - S it δ S )(1 - 0 . 35). The adjustment adds back the capitalized portion of the knowledge and organizational capital investment and subtracts the current year's depreciation of the capitalized asset. Because all the investment flows are before tax, we multiply by 1 - 0.35, where 0 . 35 is an estimated tax rate for our sample.

## 7 Assumption validation and robustness

We perform several robustness analyses beyond those discussed throughout the results above.

## 7.1 Parameter calibration

Given the inherent difficulties in separately identifying both the fraction of SG&amp;A that is an investment ( γ S ) and the rate of depreciation ( δ S ) discussed in Section 3.1, Figure 10 presents the main estimation in the Exits sample under alternative assumptions about the rate of organization capital depreciation rates. We consider a range of [ . 1 , . 3] for the δ S and re-estimate equation 7, reporting the new parameter estimates for γ S and δ G along with the R 2 . The figure shows little variation in the estimate of δ G . As we increase the δ S from 0.1 to 0.3, the estimated γ S increases from 0.18 to 0.4. The R 2 from the model estimation (right axis) remains nearly static across these dynamics, varying by only 2%. We conclude two things from this exercise: (1) that our assumed δ S = 0 . 2 is not driving any of our results, and (2) that the pair of ( γ S , δ S ) is the key assumption for measuring organization capital.

## 7.2 Estimation within time-period sub-samples

We next analyze whether the baseline parameter estimates vary significantly over different estimation windows, estimating γ t S and δ t G for each year using a ten-year rolling window of price data. This allows us to investigate the validity of our assumption that γ S and δ G are constant over time, in addition to whether business cycles or merger waves confound our estimates.The estimation is the same as in Section 3 with one exception: rather than estimate industry-year fixed effects within each time period, the industry-year fixed effects are instead taken from the full sample estimation, reported in Figure 2, and imposed within the non-linear least squares estimation. 29

Internet Appendix Figure A3 reports the coefficients of γ t S and δ t G as estimated over the different time-period sub-samples along with 95% confidence interval bounds and the full sample 'All' estimates from Table 1. The figure shows that for both parameters the sub-sample estimates are not statistically distinguishable from their full-sample counterparts in all years and are uncorrelated with each other. While Panel (a) shows that the γ S estimates are relatively static over time, panel (b) hints at a (perhaps marginally significant) increase in the δ G estimates in the early 2000's.

These results complement a similar exercise in Li and Hall (2020), who present some evidence for declining R&amp;D depreciation rates between 1987 and 2007. Our results do not exhibit such trends and are thus consistent with our baseline assumptions about static depreciation and capitalization parameters over time. Additional research is warranted for this critical assumption.

## 7.3 Unadjusted goodwill and exclusion of bankruptcies

Two assumptions in the use of exit prices are the adjustment to reported goodwill and the use of delisted firms. Recall that the former adjustment attempts to remove acquisition or pair-specific value embedded in goodwill using market reactions to the merger announcement. Columns (5) and (6) of Table 4 report the main estimation including only the 1,523 non-bankruptcy acquisitions. As expected, excluding failed firms from the analysis raises the average fraction ( γ ) of SG&amp;A that represents an investment in long-lived organizational capital from 0.28 to 0.44, an increase of 57%. The point estimates for δ G are lower than those in Table 1, with the full sample implying an average depreciation rate of knowledge capital of 26% per year. Reassuringly, when we repeat each validation test from Section 5 (unreported), the stocks implied by these alternative parameters under-perform those when delistings are included.

29 This leaves in place the identifying assumption from the main estimation that the time-series average marketto-book of intangibles within industry is unity over the entire sample, 1995-2017, rather than within each 10-year window.

Columns (7) and (8) of Table 4 report the main estimation excluding goodwill to examine the impact of unidentifiable intangible assets on our estimation. Results indicate that while δ G increases moderately (from 0.33 to 0.38), γ S falls drastically, by nearly 90% (from 0.28 to 0.03), indicating that only a tiny fraction of SG&amp;A produce identifiable intangible assets, while the majority of SG&amp;A results in higher goodwill or unidentifiable intangible assets. When we re-estimate these stocks and subject them to the full array of validations, they perform worse than the current price that uses identifiable intangible assets and goodwill. While this may seem intuitive (as the majority of SG&amp;A likely results in assets such as human capital, employee culture, and brand equity, many of which cannot be separated from the firm and sold to a third party), it underscores the importance of our inclusion of goodwill in our parameter estimation.

Finally, the last two columns of Table 4 repeat the exits-based parameter estimation without the adjustment to goodwill discussed in Internet Appendix Section A1.2. That is, we include goodwill as reported in the 10-K filing. As expected, the adjustments to goodwill have a large impact on estimates. R&amp;D depreciation rates are 50% higher, and the percentage of SG&amp;A that is investment is 36% lower, with the adjusted goodwill. These changes demonstrate that our adjustments are controlling for a large part of the synergies and overpayment found in raw goodwill. In unreported results, the stocks implied by these parameters underperform the main Exits stocks in all validations.

## 7.4 Trading prices and alternative parameters

As discussed in Section 2, the Exits sample may suffer from selection issues that could limit the generalizability of the results. As an alternative, we collect a set of intangible asset prices that suffer from no sample selection. These prices compare the publicly-traded equity valuations of firms to their physical assets that have been capitalized to the balance sheet, subject to a markup assumption to adjust them from historical cost. The difference between the firm's market capitalization and physical assets thus provides an approximation of the intangible assets of the firm. The approach is described in Internet Appendix Section A3. We estimate equation (6) using these intangible prices and repeat the intangible asset stock creation with the estimated parameters (see Internet Appendix Section A4 and Internet Appendix Table A4). While the estimation sample suffers from no sample selection, Internet Appendix Section A5 shows that the resulting stocks from the estimation under-perform the exit-based stocks. This out-performance does not prove that selection is not a concern; however, it shows that we must weigh potential selection issues against empirical performance.

Finally, recent work by Iqbal, Rajgopal, Srivastava, and Zhao (2022) provides a set of γ S parameters with finer industry granularity. We build organizational stocks with their parameters and combine them with the BEA stocks to create an alternative benchmark. In unreported results, we repeat the main diagnostics using the their stocks where organizational capital is an input. Our stocks outperform in nearly all cases. The Iqbal stocks provide weakly more explanatory power for brand equity and patents in the pre-2000 sample, but have relatively worse explanatory power for human capital risk, do not improve on ROE estimates, and underperform BEA in the market valuation regressions after 2000. Overall, this evidence suggests our organizational capital stocks have better performance than Iqbal, Rajgopal, Srivastava, and Zhao (2022).

## 8 Conclusion

Despite the growing importance of intangible capital in today's economy, the literature lacks consensus about the parameters governing intangible assets' capitalization. We develop and test a model that uses market prices to estimate parameters from firm exits, allowing us to estimate off-balance sheet intangible capital from prior R&amp;D and SG&amp;A spending. We compare the quality of these parameter estimates against commonly used BEA-HH parameters by creating two sets of capitalized intangible stocks and putting them through validation tests. Exit-based capital stocks outperform BEA-HH stocks. We document significant performance improvements in the stocks' ability to explain market enterprise values and human capital risk, while showing similar or marginal improvements in explanatory power for brand rankings, patent values, and trademarks. Incorporating these new intangible asset stock into firms' balance sheets lowers values of market-to-book and return-on-equity that conform better with expectations from extant theory.

## References

- Acemoglu, Daron, Ufuk Akcigit, Harun Alp, Nicholas Bloom, and William R Kerr, 2013, Innovation, reallocation and growth, Discussion paper, National Bureau of Economic Research.
- Aksoy, Lerzan, Bruce Cooil, Christopher Groening, Timothy L Keiningham, and Atakan Yal¸ cın, 2008, The long-term stock market valuation of customer satisfaction, Journal of Marketing 72, 105-122.
- Belo, Frederico, Xiaoji Lin, and Maria Ana Vitorino, 2014, Brand capital and firm value, Review of Economic Dynamics 17, 150-169.
- Bena, Jan, and Kai Li, 2014, Corporate innovations and mergers and acquisitions, The Journal of Finance 69, 1923-1960.
- Bernstein, Jeffrey I, and M Ishaq Nadiri, 1988, Interindustry r&amp;d spillovers, rates of return, and production in high-tech industries, The American Economic Review 78, 429-434.
- Bhagat, Sanjai, Ming Dong, David Hirshleifer, and Robert Noah, 2005, Do tender offers create value? New methods and evidence, Journal of Financial Economics 76, 3-60.
- Chan, Louis KC, Josef Lakonishok, and Theodore Sougiannis, 2001, The stock market valuation of research and development expenditures, The Journal of Finance 56, 2431-2456.
- Corrado, Carol A, and Charles R Hulten, 2010, How do you measure a 'technological revolution'?, American Economic Review 100, 99-104.
- , and Daniel E Sichel, 2006, Intangible capital and economic growth, Working Paper .
- , 2009, Intangible capital and US economic growth, Review of income and wealth 55, 661685.
- Crouzet, Nicolas, and Janice C Eberly, 2019, Understanding weak capital investment: the role of market concentration and intangibles, Working Paper 25869 National Bureau of Economic Research.
- Dakhli, Mourad, and Dirk De Clercq, 2004, Human capital, social capital, and innovation: a multicountry study, Entrepreneurship &amp; regional development 16, 107-128.
- Damodaran, Aswath, 2020, Equity risk premiums: Determinants, estimation and implications-the 2020 edition, NYU Stern School of Business .

- Daniel, Kent, and Sheridan Titman, 2006, Market reactions to tangible and intangible information, The Journal of Finance 61, 1605-1643.
- Eberhart, Allan C, William F Maxwell, and Akhtar R Siddique, 2004, An examination of longterm abnormal stock returns and operating performance following R&amp;D increases, The Journal of Finance 59, 623-650.
- Edmans, Alex, 2011, Does the stock market fully value intangibles? employee satisfaction and equity prices, Journal of Financial Economics 101, 621-640.
- Eisfeldt, Andrea L, and Dimitris Papanikolaou, 2013, Organization capital and the cross-section of expected returns, The Journal of Finance 68, 1365-1406.
- , 2014, The value and ownership of intangible capital, American Economic Review 104, 189-94.
- Erickson, Timothy, and Toni M Whited, 2006, On the accuracy of different measures of q, Financial management 35, 5-33.
- , 2012, Treating measurement error in tobin's q, The Review of Financial Studies 25, 12861329.
- Evenson, Robert E, and Larry E Westphal, 1995, Technological change and technology strategy, Handbook of Development Economics 3, 2209-2299.
- Falato, Antonio, Dalida Kadyrzhanova, Jae Sim, and Roberto Steri, 2022, Rising intangible capital, shrinking debt capacity, and the us corporate savings glut, The Journal of Finance 77, 2799-2852.
- Fama, Eugene F, and Kenneth R French, 1992, The cross-section of expected stock returns, The Journal of Finance 47, 427-465.
- , 1993, Common risk factors in the returns on stocks and bonds, Journal of Financial Economics 33, 3-56.
- Gourio, Francois, and Leena Rudanko, 2014, Customer capital, Review of Economic Studies 81, 1102-1136.
- Graham, John R, and Campbell R Harvey, 2018, The equity risk premium in 2018, Working paper .
- Guti´ errez, Germ´ an, and Thomas Philippon, 2017, Investmentless growth: An empirical investigation, Brookings Papers on Economic Activity p. 89.

- Hall, Bronwyn H, 2005, Measuring the returns to r&amp;d: The depreciation problem, Annales d' ´ Economie et de Statistique pp. 341-381.
- , Adam Jaffe, and Manuel Trajtenberg, 2005, Market value and patent citations, RAND Journal of Economics pp. 16-38.
- Hall, Bronwyn H, Jacques Mairesse, and Pierre Mohnen, 2010, Measuring the returns to R&amp;D, in Handbook of the Economics of Innovation vol. 2 . pp. 1033-1082 (Elsevier).
- Hayashi, Fumio, 1982, Tobin's marginal q and average q: A neoclassical interpretation, Econometrica 50, 213-224.
- Heath, Davidson, and Christopher Mace, 2020, The strategic effects of trademark protection, The Review of Financial Studies 33, 1848-1877.
- Hirshleifer, David, Po-Hsuan Hsu, and Dongmei Li, 2013, Innovative efficiency and stock returns, Journal of Financial Economics 107, 632-654.
- Hulten, Charles R, and Xiaohui Hao, 2008, What is a company really worth? Intangible capital and the 'Market to book value' puzzle, Discussion paper, National Bureau of Economic Research.
- Iqbal, Aneel, Shivaram Rajgopal, Anup Srivastava, and Rong Zhao, 2022, Value of internally generated intangible capital, Working Paper .
- Kogan, Leonid, Dimitris Papanikolaou, Amit Seru, and Noah Stoffman, 2017, Technological innovation, resource allocation, and growth, The Quarterly Journal of Economics 132, 665-712.
- Korteweg, Arthur, 2010, The net benefits to leverage, The Journal of Finance 65, 2137-2170.
- Lev, Baruch, 2018, Ending the accounting-for-intangibles status quo, European Accounting Review forthcoming.
- , and Suresh Radhakrishnan, 2005, Measuring capital in the new economy, in The valuation of organization capital . pp. 73-110 (University of Chicago Press).
- Lev, Baruch, and Theodore Sougiannis, 1996, The capitalization, amortization, and value-relevance of R&amp;D, Journal of Accounting and Economics 21, 107-138.
- Lev, Baruch, and Paul Zarowin, 1999, The boundaries of financial reporting and how to extend them, Journal of Accounting research 37, 353-385.

- Li, Wendy CY, and Bronwyn H Hall, 2016, Depreciation of business r&amp;d capital, Review of Income and Wealth .
- , 2020, Depreciation of business r&amp;d capital, Review of Income and Wealth 66, 161-180.
- Loumioti, Maria, 2012, The use of intangible assets as loan collateral, Available at SSRN 1748675 .
- Mann, William, 2018, Creditor rights and innovation: Evidence from patent collateral, Journal of Financial Economics 130, 25-47.
- Mizik, Natalie, and Robert Jacobson, 2008, The financial value impact of perceptual brand attributes, Journal of Marketing Research 45, 15-32.
- Newey, W.K., and D. McFadden, 1994, Large sample estimation and hypothesis testing, in Handbook of Econometrics vol. 4 . pp. 2111-2245 (Elsevier).
- Pakes, Ariel, and Mark Schankerman, 1984, The rate of obsolescence of patents, research gestation lags, and the private rate of return to research resources, in R&amp;D, patents, and productivity . pp. 73-88 (University of Chicago Press).
- Peters, Ryan H, and Lucian A Taylor, 2017, Intangible capital and the investment-q relation, Journal of Financial Economics 123, 251-272.
- Phillips, Gordon M, and Alexei Zhdanov, 2013, R&amp;D and the incentives from merger and acquisition activity, The Review of Financial Studies 26, 34-78.
- Roll, Richard, 1986, The hubris hypothesis of corporate takeovers, Journal of Business pp. 197-216.
- Shleifer, Andrei, and Robert W Vishny, 1992, Liquidation values and debt capacity: A market equilibrium approach, The Journal of Finance 47, 1343-1366.
- Subramaniam, Mohan, and Mark A Youndt, 2005, The influence of intellectual capital on the types of innovative capabilities, Academy of Management Journal 48, 450-463.
- Sun, Qi, and Mindy X Zhang, 2018, Financing intangible capital, Journal of Financial Economics forthcoming.
- Vomberg, Arnd, Christian Homburg, and Torsten Bornemann, 2015, Talented people and strong brands: The contribution of human capital and brand equity to firm value, Strategic Management Journal 36, 2122-2131.
- Williamson, Oliver E, 1988, Corporate finance and corporate governance, The Journal of Finance 43, 567-591.

## 9 Figures and tables

Figure 1: Capital expenditures and R&amp;D: 1977-2018

The figure reports average Research and Development Expense (R&amp;D) and Capital Expenditures (CAPEX) as a fraction of lagged total assets (without internally generated intangibles) for Compustat firms from 1977-2018.

<!-- image -->

Figure 2: Estimated industry-year fixed effects

The figure reports industry-year estimated market-to-book ratios, ρ jt , as the estimated fixed effects from Equation (8). The estimation allows for the market-to-book ratios to vary across industry-years, only requiring that the average of the industry-year fixed effects be one across the entire sample. Each 'violin' reports the mirrored distribution of the estimated fixed effects for each year in each Fama-French 5 industry split. The dot reports the median fixed effect and the 'x' reports the mean.

<!-- image -->

Figure 3: Explanatory power of assets for market enterprise value

Panel (a) of the figure reports the explanatory power of the estimated capital stock relative to a BEA-HH capital stock measurement in annual regressions of the firm's log market enterprise value (market capitalization plus debt and preferred stock) on the log of book value of capital stock:

<!-- formula-not-decoded -->

where E it firm i 's year t enterprise value and K TOT it is the standard book value of capital stock (Compustat at ). To avoid mechanical outperformance over BEA-HH, this analysis excludes any firm-years used in the parameter estimation of Equation 8 (i.e. acquisition targets and delisted firms in the exits-based sample and the randomly selected firm-years from the Trading sample).

Relative explanatory power is plotted by year, and calculated as excess residual variance explained:

<!-- formula-not-decoded -->

where RSS represents the residual sum of squares from the regression models.

The baseline (i.e. ' RSS BEA - HH ') is the benchmark 'BEA-HH' model that uses the parameters reported in columns (1) and (2) of Table 1. ' RSS Exits ' reflects the use of an alternate model based on exit prices. A ratio greater than zero indicates that the market-price estimated capital stocks have stronger explanatory power.

Using the same regressions described in Panel (a), Panel (b) reports the t-statistics from the test of the hypothesis that the R 2 using the Exits-based capital stock alternative is the same as the R 2 from BEA-HH. The test statistic uses the influence function method (Newey and McFadden (1994)) to compare the two separate model statistics. The horizontal lines represent t-statistics of 1.96 and -1.96.

<!-- image -->

(a) Residual sum of squares comparison

(b) T-test for R 2 differences

## Figure 4: Human capital risk

In each fiscal year, we sort firms into quintiles based on their estimated organizational capital stock using parameter estimates from Table 1. In each firm-year, we set a variable equal to one if the firm's 10-K mentions 'personnel', 'key talent' or 'talented employee,' zero otherwise. The figure reports the t-statistics (each year) for the difference in mean test for the top vs. bottom quintiles sorted by each estimation of organizational capital. The red horizontal line is at t = 1 . 96. 'HH' (Hulten and Hao) estimates organizational capital using γ S from column (1) of Table 1. 'Exits' estimates organizational capital using γ S column (4). All estimates assume δ S = 0 . 2.

<!-- image -->

Figure 5: Patent valuations and trademark counts

The figure reports the ratio of R 2 from the following yearly regressions estimated using the BEA-HH parameters in columns (1) and (2) of Table 1 (denominator) and those from the Exits approach (numerator):

<!-- formula-not-decoded -->

where Y it is either (panel a) the patent valuation from Kogan, Papanikolaou, Seru, and Stoffman (2017) (set to zero if there are no patents in the year) or (panel b) the log of the number of trademarks (plus 1) held by the firm at time t . The sum ˆ G it + ˆ S it + I it is the estimated total intangibles and X it is the lagged stock of the dependent variable. The market-price-based alternative to BEA-HH is the Exits samples (see Section 2.1) with the organizational capital using γ S column (4). All estimates assume δ S = 0 . 2.

<!-- image -->

(a) Patent valuations

(b) Trademark counts The figure reports average percentage difference between the intangible capital stocks constructed using BEA-HH and Exits-based (see Section 2.1) parameter estimates across all firms and by industry. A positive percentage difference implies that the alternative measure of intangible stock is larger than BEA-HH. Averages by year and within-industry are reported.

Figure 6: Differences in the size of estimated intangibles versus BEA-HH

<!-- image -->

Figure 7: Intangible asset intensity

The figure reports the average ratio of total intangibles - capitalized using the Exits parameters (Table 1) and those on the balance sheet - scaled by total capital stock (PPE + intangibles): K int K int + K phy . The averages are calculated across all firms within each industry-year. K int is the sum of knowledge and organizational capital using the estimates from Table 1 and a firm's previous 10 years of R&amp;D and SG&amp;A expenditures and its externally acquired goodwill and intangibles. K phy is the firm's PPE (gross). The 'All' line reports the mean across all firms. The 'Other' industry is not reported separately, but included in the 'All' series.

<!-- image -->

Figure 8: Market-to-book ratios with and without adjusted intangibles: 1977-2017

The figure reports the average (2.5% tail winsorized) market-to-book ratios for Compustat firms outside of financials, mining, real estate, utilities and all acquiring firms in our sample. To avoid mechanical outperformance over BEA-HH, this analysis also excludes any firm-years used in the parameter estimation of Equation 6 (i.e., acquisition targets and delisted firms in the Exits sample). The numerator in both series is the sum of the market value of equity at the end of the fiscal year, total liabilities and book preferred stock. For the blue circle series, the denominator is total assets (including acquired intangibles). For the green diamond series, the denominator also includes the knowledge and organizational capital stocks estimated using the Exits-based parameters in Columns (5) and (5) of Table 1. The two dotted red lines present the linear fit of each time series.

<!-- image -->

Figure 9: Return on equity (ROE) with intangibles adjustment

The figure reports the average return on equity (ROE) using two alternative measures for public firms in the S&amp;P 500. 'Unadjusted' uses the standard ROE definition of net income scaled by lagged book equity. The 'Exits' time series adjusts book equity for knowledge and organizational capital using the Exits parameter estimates. The scatter plot reports the average of the difference between the two measures (with its linear fit).

<!-- image -->

Figure 10: Estimation sensitivity under different organizational stock depreciation assumptions

The figure reports the results of re-estimating the main model for different values of the organizational stock depreciation parameter δ S . Recall that our main results assume that δ S = . 2. Here we vary this parameter and present the estimated γ S (fraction of SG&amp;A that is investment), δ G (the knowledge capital depreciation rate), and the R 2 from the estimation. The vertical red line indicates the main model assumption. The left y-axis reports the parameter estimates and the right y-axis reports the R 2 .

<!-- image -->

## Table 1: Parameter estimates from non-linear least squares estimation

Parameter estimates are based on non-linear least squares regressions of the price of intangible firm assets on accumulated intangible assets:

<!-- formula-not-decoded -->

where P I it is the price of the firm's total intangible capital as discussed in Section 2.1 and I it is the target's externally-acquired intangibles reported to the balance sheet. The industry-year fixed effects ( ρ jt ) are constrained to an average of zero (log of 1) across all years within-industry. The 'All' row reports the pooled sample estimates, while all other rows are separate estimations for the modified Fama-French 5 industry classifications. Firms can have up to ten years of financial data.

Columns (1) and (2) summarize the parameters used in the BEA-HH methodology discussed in Section 3.3 while Column (3) displays the proportion of SIC-4 industry-years for which the BEA publishes the knowledge capital depreciation rate. Columns (4) and (5) summarize the Exits-based parameters estimated from market based exit prices.

In each set of columns, the first reports the estimates of γ S , the fraction of SG&amp;A that is investment. The δ S is assumed to be 0 . 2 (i.e., not estimated). The δ G column reports the estimate of the R&amp;D depreciation rate. Pseudo R 2 estimates are calculated as the percent improvement in the exponentiated root mean squared error relative to a model which includes only a constant. Column (2) reports the average R&amp;D depreciation rates from Li and Hall (2020) for SIC codes in each of the major industry groups (one obs. per SIC). Bootstrapped (1000 replications at the firm-level) standard errors reported in parentheses. N reports the number of unique firms in the estimation.

̸

|               |   BEA-HH - (1) γ S |   BEA-HH - (2) δ G | BEA-HH - (3) = . 15   | Exits - (4) γ S   | Exits - (5) δ G   |
|---------------|--------------------|--------------------|-----------------------|-------------------|-------------------|
| All           |               0.30 |               0.23 | 52%                   | 0.28 (0.024)      | 0.33 (0.034)      |
| Consumer      |               0.30 |               0.21 | 43%                   | 0.20 (0.039)      | 0.43 (0.175)      |
| Manufacturing |               0.30 |               0.19 | 42%                   | 0.21 (0.078)      | 0.50 (0.162)      |
| High Tech     |               0.30 |               0.28 | 62%                   | 0.37 (0.084)      | 0.42 (0.147)      |
| Health        |               0.30 |               0.17 | 80%                   | 0.51 (0.221)      | 0.33 (0.093)      |
| Other         |               0.30 |               0.28 | 49%                   | 0.21 (0.077)      | 0.35 (0.149)      |
| Pseudo- R 2   |                    |                    |                       | 0.542             | 0.542             |
| N             |                    |                    |                       | 2,004             | 2,004             |

## Table 2: Brand ranking incorporating intangible assets

The table reports the OLS estimates from a regression of log brand ranking on measures of intangible capital. Brand rankings are from the Interbrand listings, which are merged with Compustat U.S. public companies. A unit of observation is a firm-year. 'Log org. cap. S (BEA-HH)' is the log of organizational capital using the BEA-HH parameters from Table 1. 'Log org. cap. S (Exits)' shows the same estimated stocks using the Exits parameter estimates. 'Exits' estimates organizational capital using γ S column (4). All estimates assume δ S = 0 . 2. 'Log total intan. K' is the sum of externally acquired intangibles, estimated knowledge capital, and estimated organizational capital. 'Year FE' are fixed effects for fiscal year. Robust standard errors reported in parentheses. We use ∗∗∗ , ∗∗ , and ∗ to denote significance at the 1%, 5%, and 10% level.

Table 3: The value premium: including intangibles in book value

|                             | Log of brand ranking - (1)   | Log of brand ranking - (2)   | Log of brand ranking - (3)   | Log of brand ranking - (4))   |
|-----------------------------|------------------------------|------------------------------|------------------------------|-------------------------------|
| Log org. cap. S (HH)        | -0.044 ∗∗∗ (0.0080)          |                              |                              |                               |
| Log org cap. S (EPW)        |                              | -0.052 ∗∗∗ (0.0084)          |                              |                               |
| Log total intan. K (BEA-HH) |                              |                              | -0.22 ∗∗∗ (0.027)            |                               |
| Log total intan. K (EPW)    |                              |                              |                              | -0.23 ∗∗∗ (0.027)             |
| Observations                | 1122                         | 1122                         | 1122                         | 1122                          |
| R 2                         | 0.014                        | 0.022                        | 0.10                         | 0.12                          |
| Year FE?                    | Y                            | Y                            | Y                            | Y                             |

The table reports summary statistics for HML portfolio returns from 1976 through 2017. The unadjusted portfolios are constructed as in Fama and French (1992). The adjusted portfolios are constructed similarly, with the measure of book equity augmented by the intangible capital stocks implied by the parameters in Table 1, columns (5) and (6). Returns are reported in percentage points per month.

|                               | (1) Unadjusted Portfolios     | (2) Adjusted Portfolios       | (3) Correctly Sorted (%)   |   (4) Return Cor- rectly Sorted | (5) Missorted (%)   |   (6) Return Missorted |
|-------------------------------|-------------------------------|-------------------------------|----------------------------|---------------------------------|---------------------|------------------------|
| Low B/M                       | 0.876                         | 0.839                         |                            |                           0.829 |                     |                  1.105 |
| (# firm-months)               | 730,696                       | 640,171                       | 70%                        |                         512,574 | 30%                 |                218,122 |
| Mid B/M                       | 0.969                         | 0.999                         |                            |                           0.952 |                     |                  1.000 |
| (# firm-months)               | 710,488                       | 706,404                       | 55%                        |                         391,751 | 45%                 |                318,737 |
| High B/M                      | 1.072                         | 1.212                         |                            |                           1.215 |                     |                  0.892 |
| (# firm-months)               | 714,267                       | 808,876                       | 78%                        |                         559,934 | 22%                 |                154,333 |
| Hi - Lo                       | 0.196                         | 0.373                         |                            |                           0.386 |                     |                -0.2139 |
| Total Firm-Month Observations | Total Firm-Month Observations | Total Firm-Month Observations | 2,155,451                  |                                 |                     |                        |

## Table 4: Parameter estimates from non-linear least squares estimation: alternative assumptions

Parameter estimates are based on non-linear least squares regressions of the price of intangible firm assets on accumulated intangible assets:

<!-- formula-not-decoded -->

where P I it is the price of the firm's total intangible capital as discussed in Section 2.1 and I it is the target's externally-acquired intangibles reported to the balance sheet. The industry-year fixed effects ( ρ jt ) are constrained to an average of zero (log of 1) across all years within-industry. The sample is as described in Table 1, but adjusted in three ways. Columns (1) and (2) report the main BEA-HH parameters, while columns (3) and (4) report the baseline estimates from Table 1. Columns (5) and (6) present the estimates from a sample without liquidations, columns (7) and (8) consider all exits but exclude goodwill from prices, and columns (9) and (10) report the full sample estimate without the adjustment to goodwill for synergies or over-payment.

|               |   BEA-HH - (1) - γ S |   BEA-HH - (2) - δ G | Exits - (3) - γ S   | Exits - (4) - δ G   | Excl. liquid. - (5) - γ S   | Excl. liquid. - (6) - δ G   | No goodwill - (7) - γ S   | No goodwill - (8) - δ G   | Unadj. goodwill - (9) - γ S   | Unadj. goodwill - (10) - δ G   |
|---------------|----------------------|----------------------|---------------------|---------------------|-----------------------------|-----------------------------|---------------------------|---------------------------|-------------------------------|--------------------------------|
| All           |                 0.30 |                 0.23 | 0.28 (0.024)        | 0.33 (0.034)        | 0.44 (0.040)                | 0.26 (0.036)                | 0.03 (0.005)              | 0.38 (0.021)              | 0.44 (0.035)                  | 0.22 (0.029)                   |
| Consumer      |                 0.30 |                 0.21 | 0.20 (0.039)        | 0.43 (0.175)        | 0.37 (0.077)                | 0.43 (0.187)                | 0.03 (0.014)              | 0.25 (0.133)              | 0.26 (0.044)                  | 0.10 (0.149)                   |
| Manufacturing |                 0.30 |                 0.19 | 0.21 (0.078)        | 0.50 (0.165)        | 0.31 (0.093)                | 0.19 (0.204)                | 0.05 (0.024)              | 0.37 (0.148)              | 0.57 (0.108)                  | 0.33 (0.167)                   |
| High Tech     |                 0.30 |                 0.28 | 0.37 (0.084)        | 0.42 (0.147)        | 0.55 (0.095)                | 0.41 (0.109)                | 0.16 (0.065)              | 0.50 (0.135)              | 0.73 (0.102)                  | 0.38 (0.119)                   |
| Health        |                 0.30 |                 0.17 | 0.51 (0.221)        | 0.33 (0.093)        | 0.96 (0.264)                | 0.38 (0.095)                | 0.14 (0.133)              | 0.27 (0.089)              | 0.72 (0.228)                  | 0.19 (0.079)                   |
| Other         |                 0.30 |                 0.28 | 0.21 (0.077)        | 0.35 (0.149)        | 0.43 (0.24)                 | 0.04 (0.178)                | 0.04 (0.026)              | 0.24 (0.088)              | 0.43 (0.107)                  | 0.25 (0.166)                   |
| Pseudo- R 2   |                      |                      | 0.542               | 0.542               | 0.461                       | 0.461                       | 0.536                     | 0.536                     | 0.557                         | 0.557                          |
| N             |                      |                      | 2,004               | 2,004               | 1,523                       | 1,523                       | 2,004                     | 2,004                     | 2,004                         | 2,004                          |

## Internet Appendix

## A1 Details on acquisition sample construction

## A1.1 Sample construction

We require data availability of the acquirer's purchase price allocation of the target's assets in order to collect the prices paid for goodwill and identifiable intangible assets (IIA). When available, these purchase price allocations were found in the acquirer's subsequent 10-K, 10-Q, 8-K, or S-4 filing. We found information on the purchase price allocation for 81% (1,719) of all candidate acquisitions. 1 In the final step, we merge the target and acquirer firms to Compustat and CRSP. For each target firm merged with Compustat, we gather up to 10 years of the firm's past R&amp;D and SG&amp;A expenditures along with any pre-acquisition acquired intangibles on its balance sheet. 2,3 The final sample includes 1,523 events (70%). Below we describe how these deals differ from those lost in the data collection process.

Any remaining selection issues after incorporating bankruptcies take one of two forms. If most acquisition targets are low productivity innovators (e.g., Bena and Li (2014)), then we may estimate too high a depreciation rate and too low a value of γ . Alternatively, acquired firms may, on average, represent firms with successful innovation projects or that are purchased at the peak of their innovative productivity. In this case, we would estimate too low a depreciation rate and/or too high a fraction of organizational capital investment ( γ ). It is not clear which source of selection issues dominates, so we use the well-identified parameter estimates from Li and Hall (2016) to help judge our estimates. Since their estimation of depreciation parameters for R&amp;D is derived from a representative set of firms (from a small set of industries), a lack of systematic differences with our estimates would indicate that our sample selection is not severe. 4

## A1.2 Synergy and over-payment: adjusting goodwill

Acquisitions may be motivated by pair-specific synergy values, and prior research has documented that managers may overpay for a target due to agency frictions or hubris (e.g., Roll (1986)). These issues could potentially affect the representativeness of our imputed parameter estimates when applied to the full population of firms. Extending our parameter estimates to all publicly listed firms requires that the prices paid for intangible capital in our sample represent a public or market value. Fortunately, the purchase price allocation process directly separates intangible assets that can be identified via either a separability criterion or a previously established contractual legal criterion. Thus, pair-wise values arising from the acquisition - synergies - will be recorded as goodwill. Because we are interested in the stand-alone value of assets, our analyses adjust goodwill accordingly.

1 Some filings lacked the footnote for the acquisition (e.g., the acquisition was immaterial), or we could not identify any filing for the acquiring firm (e.g., the firm has a unique registration type with the SEC).

2 If Compustat has less than 10 years of data and the firm is older than 10 years old, then we impute any missing R&amp;D and SG&amp;A using observed growth rates for the same age firms with non-missing data. All results are robust to excluding these imputed data.

3 We also lose acquisitions because we either failed to find a Compustat identifier or the firm did not have stock price data in CRSP (e.g., it was traded on the OTC markets).

4 We run all analyses with and without the bankrupt firms and show that the estimates change as predicted.

To make these adjustments, we apply the market's assessment of synergy value and under/overpayment of the target firm by using changes in the target and acquirer's market valuation around the acquisition event date. We follow the Bhagat, Dong, Hirshleifer, and Noah (2005) framework for the estimation of merger value creation as an adjustment to goodwill. Specifically, using this probability scaling method for announcement day returns, we estimate the synergy and over-payment component of the acquisition value and then remove this estimate from goodwill valuations from the purchase price allocation. 5 This estimate is removed from goodwill valuations from the purchase price allocation. 6

For each acquisition event, we first calculate the [ - 5 , 5] day change cumulative abnormal return for both the target and acquirer. 7 Multiplying by the pre-deal ( t = - 6) market value of each gives the abnormal change in market valuation at deal announcement. Next, as the market's response incorporates expectations about merger failures, we weight them by the inverse of the probability of acquisition success implied by the end-of-period market price of the target compared to the offer price in the deal. 8 The sum of the target and acquirer's changes - the expected synergy

- is subtracted from goodwill. 9 We remove the acquirer's change in valuation as it incorporates under/over-payment. Here, a decline in the acquirer's market value would signal over-payment for the target, leading to goodwill that is abnormally large when compared to payment at fair market value; as such, this over-payment must be removed from goodwill. We find the goodwill adjustments to be substantial, with the average (median) deal adjustment resulting in a 34% (21%) decline in goodwill. 10

5 We cannot easily implement the second 'intervention method' with our relatively small sample size.

6 In cases where the adjustment exceeds goodwill (less than 15% of deals), the remainder is removed from the IIA valuation.

7 The estimates below are robust to 2, 4, and 30-day event windows.

8 That is, the probability of a successful merger is P 1 - P 0 P offer - P 0 , where P 1 is the end-of-day target share price, P 0 is the pre-announcement share price and P offer is the original offer price. For example, if the pre-announcement price is 100 and the tender offer is 200, an end-of-day share price of 170 implies a 70% probability of deal completion. When this is unavailable or outside the unit interval, we use the observed success rate in SDC over our sample period (78%).

9 If the result is negative, then the remainder is subtracted from the identifiable intangible assets.

10 Internet Appendix Figure A2 reports the percentage of acquisition deal size allocated to goodwill and IIA after these adjustments. The prevalence of goodwill in deal size falls in all years (see the green arrows), which has an

## A1.3 Main variables

Figure A1 (a) shows the prevalence of goodwill and IIA for our acquisition sample. It reports the percentage of all deals that have some amount of either asset in the purchase price allocation. We observe an upward trend in these components since the mid-1990s, with over 85% of deals containing goodwill or IIA since 2004. To ensure that our observations are not driven by smaller acquisitions, Figure A1 (b) repeats the analysis but replaces the y-axis with a dollar-weighted measure, which is the sum of all IIA and goodwill in the sample, scaled by the sum of all acquisition deal sizes in the sample. The patterns remain. Figure A2 asks how much of the total enterprise value is comprised of goodwill and IIA. The latter represents 25% of total transaction value over the sample period, while the former accounts for approximately 35% of the typical deal size over the full sample period. This suggests that intangibles play a major role in the U.S. acquisition market.

## A1.4 Summary statistics

Panel A of Table A2 presents summary statistics on deals and the parties. All dollar values are in 2012 dollars. The average deal year is 2005, with an average (median) deal size of $ 2.3b ( $ 426m). Deal size as measured by enterprise value (thus including assumed liabilities) averages $ 2.5b. We assign firm industries using the Fama-French 5 industry classification. Consumer firms represent 18% of targets, while the average target has an EBITDA of $ 142m. Over one-quarter of the acquirers are headquartered in California, which is slightly above the rate for all public firms. This is likely a consequence of both our focus on acquisitions and our requirements for observability of the purchase price allocation for intangibles. We also see that goodwill is on average $ 1.1b with a much lower median of $ 159m. 11 IIA comprises 38% of total intangible capital (goodwill plus IIA) on average. Finally, total intangibles represent 75% of enterprise deal size on average. In 281 acquisitions, the total intangible capital exceeds the enterprise value of the firm. We randomly checked 20 acquisitions in this sub-sample and verified that this is a result of the target's net tangible assets being less than zero. Correspondingly, we found that these targets tended to be high-tech or healthcare targets with very high R&amp;D and SG&amp;A expenditures and very low levels of PP&amp;E on their balance sheets.

impact on the total intangible value in acquisitions.

11 In a few observations, total intangibles (identifiable intangible assets and goodwill) is negative. These instances, while rare, occur because goodwill can take on negative values and in these cases, the negative value is larger than the value of identifiable intangible assets. Since goodwill is the plug variable that equates the balance sheet, negative goodwill occurs when the acquirer is able to purchase the target at a price that is below the fair value of net tangible assets that is measured during the due diligence appraisal. This negative goodwill is immediately recorded to the income statement as an extraordinary gain.

We allow goodwill to be negative, but because the estimation is done in logs we bottom code total intangibles to zero.

Panel B of Table A2 summarizes the acquisitions in the bankrupt firm sample. The average failure date in our sample is earlier than the acquisition date (2002 vs. 2004). In fact, over a quarter of the delistings in our sample occur in years 2000 and 2001, the burst of the e-commerce dot-com bubble. In contrast to acquired firms, These firms are more to be in the consumer industry (34% vs. 18%). Not surprisingly, the average failed firm tends to be small and unprofitable, with an average asset size of $ 252m and net loss of $ 80m. Total intangibles - which are estimated as a function of the 'deal size' defined in the previous section - are small with an average of $ 35m, keeping in mind that we make no assumption about the breakdown of goodwill or identifiable intangibles, only the total.

## A1.5 Selection of acquisitions

Our final acquisition sample (excluding delistings from bankruptcies) excludes 588 deals in which an extensive search failed to find the purchase price allocation. Thus, inferences derived using this final acquisition sample should address these potential sample selection issues. Fortunately, Table A3 shows that our sample of acquisitions is reasonably similar to those excluded. The rightmost columns present the excluded acquisitions. These acquisitions occurred earlier in the sample, are less likely to be in manufacturing, and have a smaller median deal size ( $ 177 vs. $ 385m). The smaller size implies these acquisitions are more likely to be immaterial to the acquirer and, consequently, not to have a purchase price allocation in their filings. Reassuringly, the targets are not significantly smaller in the excluded group when measured by pre-acquisition assets or net sales. Overall, Table A3 shows that our acquisition sample likely tilts toward larger deals and more recent events. The inclusion of delisted firms - with low assumed 'acquisition' values and no time period constraints - helps to balance many of these differences out.

## A2 Real-world purchase price allocation examples

## Matrix Pharmaceutical, February 20, 2002

## Note 4 - Acquisition of Matrix Pharmaceutical, Inc.

On February 20, 2002, Chiron acquired Matrix Pharmaceutical, Inc., a company that was developing tezacitabine, a drug to treat cancer. As of March 31, 2002, Chiron acquired substantially all of the outstanding shares of common stock of Matrix Pharmaceutical at $ 2.21 per share, which, including estimated acquisition costs, resulted in a total preliminary purchase price of approximately $ 67.1 million. Matrix Pharmaceutical is part of Chiron's biopharmaceuticals segment. Tezacitabine expanded Chiron's portfolio of cancer therapeutics.

Chiron accounted for the acquisition as an asset purchase and included Matrix Pharmaceutical's operating results, including the seven business days in February 2002, in its consolidated operating results beginning on March 1, 2002. The components and allocation of the preliminary purchase price, based on their fair values, consisted of the following (in thousands):

| Consideration and acquisition costs:                |          |
|-----------------------------------------------------|----------|
| Cash paid for common stock                          | $ 49,986 |
| Cash paid for options on common stock               | 1,971    |
| Common stock tendered, not yet paid                 | 8,751    |
| Options on common stock, not yet paid               | 260      |
| Acquisition costs paid as of March 31, 2002         | 3,323    |
| Acquisition costs not yet paid as of March 31, 2002 | 2,796    |
| Total purchase price                                | $ 67,087 |
| Allocation of preliminary purchase price:           |          |
| Cash and cash equivalents                           | $ 17,337 |
| Assets held for sale                                | 2,300    |
| Deferred tax asset                                  | 10,000   |
| Other assets                                        | 1,469    |
| Write-off of purchased in-process technologies      | 54,781   |
| Accounts payable                                    | (2,898)  |
| Accrued liabilities                                 | (15,902) |
| Total purchase price                                | $ 67,087 |

## A3 Trading prices as alternative market prices

As an alternative to exit-based prices used in the main paper, we also use intangible valuations - hereafter, 'Trading' prices - from market prices of publicly-traded common equity. Publiclytraded equity reflects the market's valuation of a firm's net assets values, which are composed of both physical and intangible assets less preferred stock and liabilities. Given values for physical assets, preferred stock, and liabilities, we can infer the firm's intangible asset value. A primary advantage of this approach is that the sample of firms used to estimate the accumulation parameters is representative of the population where researchers will most likely use them: public firms. We arrive at the market value of intangibles by solving for P I it in the decomposition of total assets. Here, P Total it reflects the sum of physical and intangible assets and is financed by common equity, preferred equity, and debt:

<!-- formula-not-decoded -->

For publicly-traded firms, we observe market values of equity but only book values of liabilities, preferred stock, and total assets. We follow prior literature and assume that market values of preferred stock and debt are well-approximated by their book values. We also require an assumption about the market value of physical assets since accounting rules mandate that the balance sheet report them at their original purchase prices, and the assets cannot be marked to market. We follow Erickson and Whited (2006, 2012) and Peters and Taylor (2017) and use the sum of gross PPE, current assets and 'other' (physical) assets. 12 Ultimately, any measurement error in the markups will be reflected in the dependent variable P I it and lower the precision of our parameter estimates δ G and γ S , and ultimately the precision of G it and S it .

One advantage of the trading sample is that those prices are unlikely to be subject to selection issues, as the intangible market price can be calculated for nearly all publicly-traded firms. However, the benefits of the representativeness of this sample of prices must be weighed against any potential noise in the markup estimation for physical assets. The following section summarizes the estimation of depreciation parameters and the results of validation tests using the implied stocks. To summarize, we find that while the 'trading' estimates outperform the BEA-HH in most cases, the Exits-based stocks outperform both. Thus, we conclude that while selection is a limitation of the exit-based method, the empirical performance of these implied stocks minimizes such concerns.

## A4 Trading sample estimation

Internet Appendix Table A4 presents the results of the estimation using trading prices. The table reports the benchmark BEA-HH and the main estimation from the Exits prices. Two differences stand out when comparing the trading and Exits results. The γ S estimate is significantly larger in the former, while the δ G is significantly larger in the Exits estimate. This implies that the Exits stocks will have relatively smaller stocks of both knowledge and organizational capital. It is interesting to reconcile the different resulting parameters between Trading and Exits in context with our previously mentioned selection concerns, particularly with regard to positive selection of acquisition targets. Positive selection would predict that the Exits-based stocks be larger than those using parameters estimated from a selection-free sample. Given the estimated parameters in Table A4, this does not appear to be a first-order issue with the exits-based approach. The validation tests in the next section will allow us to evaluate the relative accuracy of these measured stocks.

12 As an alternative, we estimate the assumption of gross markup to reflect Erickson and Whited (2006) who use the compounded rate of inflation to estimate the markup of net PPE. Untabulated results from validation tests indicate that using gross PPE as a markup tool outperforms this alternative markup assumption.

## A5 Trading-based intangible stock validations

We construct knowledge and organizational capital stocks using the estimated depreciation parameters in Table A4 and re-run all the validation tests reported in Section 5. The goal here is to assess whether the trading sample improves upon BEA-HH stock and, more importantly, how it performs relative to Exits-based stocks. To summarize, the Exits-based stocks perform better in all validation tests. First, Internet Appendix Figure A4 reports the market valuation fit tests for the Exits and the trading intangible stocks. Panel (a) shows that trading provides less explanatory power than Exits but even more striking, relatively worse explanatory power than BEA-HH in many years. Next, Internet Appendix Figure A5 reports the tests explaining human capital risks across firms. In only one year do the trading stocks provide a better separation of the cross-section of human capital risk than the Exits-based stocks. They notably outperform the HH stocks in all years. Finally, in unreported results, we also find that the stocks using the trading parameters under-perform relative to Exits in all tests presented in Section 5. These exercises provide reassurance that the Exits-based stocks - and the collection of assumptions that it rests on - provide superior intangible asset stocks.

## A1 Internet Appendix figures and tables

Table A1: Variables and definitions of terms

The table presents variable and term definitions used throughout the paper.

| Variable/Term              | Definition                                                                                                                                                                                                                                                                                                                                                    |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Deal effective year        | Year the acquisition was completed.                                                                                                                                                                                                                                                                                                                           |
| Year announced             | The year that the acquisition was announced to the public.                                                                                                                                                                                                                                                                                                    |
| Services firm (target)     | An indicator equal to one if the acquisition target is in the services sector.                                                                                                                                                                                                                                                                                |
| Value of transaction (mil) | The total value of the acquisitions (in 2012, USD millions) as reported in SDC.                                                                                                                                                                                                                                                                               |
| Target Net Sales LTM (mil) | The last twelve month net sales for the target firm at the time of acquisition (2012 USD).                                                                                                                                                                                                                                                                    |
| Target EBITDA LTM (mil)    | The last twelve month EBITDA for the target firm at the time of acquisition (2012 USD).                                                                                                                                                                                                                                                                       |
| Target total assets        | Total assets of the acquired firm at the time of acquisition (2012 USD).                                                                                                                                                                                                                                                                                      |
| CA HQ (acq.)               | An indicator variable that is equal to one if the firm is headquartered in California.                                                                                                                                                                                                                                                                        |
| NY HQ                      | An indicator variable that is equal to one if the firm is headquartered in New York state.                                                                                                                                                                                                                                                                    |
| Intangible assets (IIA)    | The total identified intangible assets from the acquisition revealed through the purchase price allocation. Reported in millions (2012 USD).                                                                                                                                                                                                                  |
| Goodwill (mil)             | The total goodwill allocated in the acquisition (2012 USD).                                                                                                                                                                                                                                                                                                   |
| Goodwill (adj., mil)       | The total goodwill net of an estimate of synergy and any over/under-payment of the target by the acquirer. The former is approximated by the sum of the product of 2-day window cumulative abnormal (CAR) and pre-deal market value for both target and acquirer, while the latter is the negative of the acquirer's CAR times the pre-deal market valuation. |
| All stock                  | An indicator variable equal to one if the acquisition was an all-stock deal.                                                                                                                                                                                                                                                                                  |
| All cash                   | An indicator variable equal to one if the acquisition was an all-cash deal.                                                                                                                                                                                                                                                                                   |
| Balance sheet intan.       | The total intangible assets already on the balance sheet of the firm, typically from past acquisitions of intangibles and goodwill.                                                                                                                                                                                                                           |
| Organizational capital     | The capitalization of some fraction γ of SG&A expenditures by a firm. It is meant to capture the knowledge used to combine human skills and tangible capital into systems for producing and delivering want-satisfying products.                                                                                                                              |
| Knowledge capital          | The consensus proxy for the flows of a firm's knowledge capital in the intan- gibles literature is its periodic disclosure of research and development expen- ditures.                                                                                                                                                                                        |
| BEA-HH                     | The acronym for the depreciation parameter assumptions using R&D depre- ciation rates published by U.S. Bureau of Economic Analysis for knowledge capital from Li and Hall (2016) and the fraction of SG&A that is investment from Hulten and Hao (2008).                                                                                                     |

Figure A1: Percentage of acquisition deals with non-zero intangible assets or goodwill

The figure in Panel A reports the percentage of all acquisitions in the sample (see Section 2.1) that have non-zero intangible assets or goodwill acquired. The deals included are those where we could find a purchase price allocation in the target's 10-K, 10-Q, S-4, or 8-K. Panel B reports the percentage of all deal dollars in our sample of acquisitions (see Section 2.1) associated with deals that have non-zero goodwill or intangible assets acquired. So the 'Goodwill' figure is the annual sum of transactions with some positive goodwill divided by the total amount of transaction dollars in that year.

## (a) Prevalence of IIA and goodwill

<!-- image -->

Figure A2: Percentage of acquisition deal size for intangible assets

The figure reports the average percentage of an acquisition deal size (i.e., the enterprise value of the deal) attributed to goodwill, intangible assets (IIA), and their sum. The sample is the subset of acquisitions (see Section 2.1) associated with deals that have non-zero goodwill or intangible assets acquired.

<!-- image -->

Figure A3: Rolling Estimates of Parameter Values in 10-Year Windows

The figure reports estimates of γ S (the fraction of SG&amp;A which represents an investment in long-lived organizational capital; panel a) and δ G (the depreciation rate of knowledge capital; panel b) from the non-linear least squares estimation of equation (6) run on rolling 10-year windows of events. The horizontal axis reports the first year of the sub-sample window. The red horizontal lines represent the full-sample point estimates of γ S and δ G , respectively, from Table 1. Each panel also reports the 95% confidence interval of each rolling estimate.

<!-- image -->

- (a) Organizational capital investment rate
- (b) Knowledge capital depreciation

Figure A4: Explanatory power of assets for market enterprise value: trading

The figure repeats the analysis in Figure 3 with the addition of the trading sample estimates described in Section A4.The test statistic uses the influence function method (Newey and McFadden (1994)) to compare the two separate model statistics. The horizontal lines represent t-statistics of 1.96 and -1.96.

<!-- image -->

- (a) Residual sum of squares comparison
- (b) T-test for R 2 differences

Figure A5: Human capital risk: trading estimates

The figure repeats the analysis in Figure 4 including the organizational capital stocks from the trading estimates in Table A4. All estimates assume δ S = 0 . 2.

<!-- image -->

Table A2: Summary statistics for sample of found deals in model estimation.

Summary statistics for observable characteristics of deals, targets and acquirers for the sample of acquisitions in the estimation. Panel A reports the characteristics of the acquisition sample and Panel B reports the characteristics of the failure sample. Variable definitions found in Internet Appendix Table A1.

|                 | Std dev   | 6.02 6.01 0.31 0.42                                               |           | 0.49                                                                                 | 9577.42 8324.64            |                                     | 718.37 4356.91                                             | 3761.24 0.45 0.24 0.43 0.29 3477.84                                                      | 2805.47 7994.19 7522.62 0.32                                                                                       | 11.08                                                                              | 0.29                                                                                        | 0.96 0.28                                         |
|-----------------|-----------|-------------------------------------------------------------------|-----------|--------------------------------------------------------------------------------------|----------------------------|-------------------------------------|------------------------------------------------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|---------------------------------------------------|
| (acquisitions)  | Max       | 2017.00 2017.00                                                   | 1.00 1.00 | 1.00                                                                                 | 235456.90                  | 213642.28 14080.56                  | 66446.29 67343.40                                          | 1.00 1.00 1.00 1.00 52730.25                                                             | 36460.48 170875.33 167889.61                                                                                       | 1.00 411.69                                                                        | 1.00 35.41                                                                                  | 1.00                                              |
| in model sample | Median    | 2004.00 2004.00                                                   | 0.00 0.00 | 0.00                                                                                 | 440.24                     | 384.80 13.75                        | 200.65 192.59                                              | 0.00 0.00 0.00 0.00 160.74 67.21                                                         | 272.10 172.82                                                                                                      | 0.34 0.85                                                                          | 0.72 0.77                                                                                   | 0.70                                              |
| A: Deals        | Min.      | 1996.00 1995.00                                                   | 0.00 0.00 | 0.00                                                                                 | 0.80                       | 0.59 -7430.78                       | 0.43 -35.17                                                | 0.00 0.00 0.00 0.00 -5.54 -2985.72                                                       | -5.54 -1231.19                                                                                                     | 0.00 -0.11                                                                         | -0.11 -0.10                                                                                 | -0.10                                             |
| Panel           | Mean      | 2005.03                                                           | 0.23      | 0.40                                                                                 | 2519.05                    | 2143.14                             | 1203.76 1111.67                                            | 0.28 0.06 0.24 0.10                                                                      | 771.09 2032.71                                                                                                     | 1.31                                                                               | 0.64 0.75                                                                                   | 0.63                                              |
|                 | Obs       | 2004.73 1,523                                                     | 0.11      | 1,523 1,523                                                                          | 1,523                      | 142.73                              | 1,491                                                      | 1,523 1,523 1118.38                                                                      | 1685.42                                                                                                            | 0.38                                                                               | 1,523                                                                                       |                                                   |
|                 |           | Deal effective year 1,523 Year announced 1,523 Manufacturing firm | (target)  | Consumer firm (target) High-tech firm (target) Enterprise value of transaction (mil) | Value of Transaction (mil) | 1,523 Target EBITDA LTM (mil) 1,459 | Target Total Assets (mil) 1,505 Target Net Sales LTM (mil) | CA HQ (target) NY HQ (target) CA HQ (acq.) 1,523 NY HQ (acq.) 1,523 Goodwill (mil) 1,523 | Adjusted goodwill (mil) 1,523 Total intangibles (IIA + GW, mil) 1,523 Total intangibles (IIA + Adj. HW, mil) 1,523 | IIA / IIA + GW (if positive) 1,468 Total intangibles / Total deal size (all) 1,523 | Total intangibles / Total deal size ( < 1) 1,052 Total intangibles / Total ent. value (all) | Total intangibles / Total ent. value ( < 1) 1,244 |

| Std dev             | 5.50        | 0.30               | 0.48          | 0.41           | 627.55                  | 536.55 58.21                            |
|---------------------|-------------|--------------------|---------------|----------------|-------------------------|-----------------------------------------|
| (failures) Max      | 2017.00     | 1.00               | 1.00          | 1.00           | 6562.82                 | 95.52 661.06                            |
| model sample Median | 2001.00     | 0.00               | 0.00          | 0.00           | 64.57                   | -10.49 1.57                             |
| B: Deals Min.       | 1996.00     | 0.00               | 0.00          | 0.00           | 0.31                    | -9919.61 0.00                           |
| Mean                | 2003.00     | 0.10               | 0.37          | 0.22           | 252.23                  | -80.33 19.71                            |
| Obs                 | 481         | 481                | 481           | 481            | 471                     | 446 453                                 |
|                     | Year failed | Manufacturing firm | Consumer firm | High-tech firm | Total assets (2012 USD) | Net income (2012 USD) Total intangibles |

Table A3: Summary statistics for sample of acquisitions in and out of sample.

Summary statistics of deal characteristics of acquisition deals in our sample and those that were excluded. Excluded deals are generally those acquisitions where we could not find the purchase price allocation in the acquirer's financial statements. The starting sample of potential acquisitions were all U.S.-based public firm acquisitions or public targets outside of finance, mining, real estate, and utilities from 1996-2017 where we could match both firms to Compustat.

| Std dev             | 5.61                                                                                      | 5.65                |   0.33 |   0.45 | 0.47 6849.67                          | 6023.14                    | 1605.84                 | 4206.15                   | 3519.38                    | 0.41           | 0.28           | 0.36         | 0.33         |
|---------------------|-------------------------------------------------------------------------------------------|---------------------|--------|--------|---------------------------------------|----------------------------|-------------------------|---------------------------|----------------------------|----------------|----------------|--------------|--------------|
| acquisitions Median | 2001.00                                                                                   | 2001.00             |   0.00 |   0.00 | 0.00 227.84                           | 178.55                     | 10.23                   | 151.64                    | 125.16                     | 0.00           | 0.00           | 0.00         | 0.00         |
| Excluded Mean       | 2002.61                                                                                   | 2002.28             |   0.12 |   0.28 | 0.32 1947.90                          | 1591.27                    | 208.19                  | 1251.23                   | 1016.31                    | 0.21           | 0.09           | 0.16         | 0.13         |
| Obs                 | 586                                                                                       | 586                 |    586 |    586 | 586 586                               | 586                        | 524                     | 553                       | 540                        | 586            | 586            | 586          | 586          |
| Std dev             | 6.02                                                                                      | 6.01                |   0.31 |   0.42 | 0.49 9577.42                          | 8324.64                    | 718.37                  | 4356.91                   | 3761.24                    | 0.45           | 0.24           | 0.43         | 0.29         |
| acquisitions Median | 2004.00                                                                                   | 2004.00             |   0.00 |   0.00 | 0.00 440.24                           | 384.80                     | 13.75                   | 200.65                    | 192.59                     | 0.00           | 0.00           | 0.00         | 0.00         |
| Included Mean       | 2005.03                                                                                   | 2004.73             |   0.11 |   0.23 | 0.40 2519.05                          | 2143.14                    | 142.73                  | 1203.76                   | 1111.67                    | 0.28           | 0.06           | 0.24         | 0.10         |
| Obs                 | 1,523                                                                                     | 1,523               |  1,523 |  1,523 | 1,523 1,523                           | 1,523                      | 1,459                   | 1,505                     | 1,491                      | 1,523          | 1,523          | 1,523        | 1,523        |
|                     | Year announced Manufacturing firm (target) Consumer firm (target) High-tech firm (target) | Deal effective year |        |        | Enterprise value of transaction (mil) | Value of Transaction (mil) | Target EBITDA LTM (mil) | Target Total Assets (mil) | Target Net Sales LTM (mil) | CA HQ (target) | NY HQ (target) | CA HQ (acq.) | NY HQ (acq.) |

Table A4: Parameter estimates from non-linear least squares estimation: trading sample

Parameter estimates are based on non-linear least squares regressions of the price of intangible firm assets on accumulated intangible assets:

<!-- formula-not-decoded -->

where P I it is the price of the firm's total intangible capital as discussed in Section 2.1 and I it is the target's externally-acquired intangibles reported to the balance sheet. The industry-year fixed effects ( ρ jt ) are constrained to an average of zero (log of 1) across all years within-industry. The 'All' row reports the pooled sample estimates, while all other rows are separate estimations for the modified Fama-French 5 industry classifications. Firms can have up to ten years of financial data. The table repeats the analysis in Table 1, but adds the trading sample estimates (See Internet Appendix Section A3 for details) in columns (6) and (7). Bootstrapped (1000 replications at the firm level) standard errors reported in parentheses. N reports the number of unique firms in the estimation.

̸

|             |   BEA-HH - (1) γ S |   BEA-HH - (2) δ G | BEA-HH - (3) = . 15   | Exits - (4) γ S   | Exits - (5) δ G   | Trading - (6) γ S   | Trading - (7) δ G   |
|-------------|--------------------|--------------------|-----------------------|-------------------|-------------------|---------------------|---------------------|
| All         |               0.30 |               0.23 | 52%                   | 0.28 (0.025)      | 0.32 (0.032)      | 0.45 (0.030)        | 0.13 (0.033)        |
| Consumer    |               0.30 |               0.21 | 43%                   | 0.19 (0.039)      | 0.29 (0.180)      | 0.34 (0.046)        | 0.38 (0.115)        |
| Manufacturi |               0.30 |               0.19 | 42%                   | 0.26 (0.079)      | 0.36 (0.156)      | 0.63 (0.089)        | 0.27 (0.040)        |
| High Tech   |               0.30 |               0.28 | 62%                   | 0.43 (0.093)      | 0.49 (0.177)      | 0.40 (0.121)        | 0.32 (0.149)        |
| Health      |               0.30 |               0.17 | 80%                   | 0.54 (0.205)      | 0.30 (0.099)      | 0.69 (0.129)        | 0.13 (0.074)        |
| Other       |               0.30 |               0.28 | 49%                   | 0.24 (0.089)      | 0.26 (0.148)      | 0.74 (0.142)        | 0.02 (0.070)        |
| Pseudo- R 2 |                    |                    |                       | 0.542             | 0.542             | 0.374               | 0.374               |
| N           |                    |                    |                       | 2,004             | 2,004             | 10,348              | 10,348              |