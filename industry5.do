/*

  This file assigns a modified version of the five industry classification of Fama and French.  The modifications are switching SICs in 
healthcare into consumer (hospitals) and radio/TV/providers in high-tech into consumer.

*/
gen industry5 = .
 
replace industry5 = 2 if ///Manuf  Manufacturing, Energy, and Utilities
sic >= 2520 & sic <= 2589 | ///
sic >= 2600 & sic <= 2699 | ///
sic >= 2750 & sic <= 2769 | ///
sic >= 2800 & sic <= 2829 | ///
sic >= 2840 & sic <= 2899 | ///
sic >= 3000 & sic <= 3099 | ///
sic >= 3200 & sic <= 3569 | ///
sic >= 3580 & sic <= 3621 | ///
sic >= 3623 & sic <= 3629 | ///
sic >= 3700 & sic <= 3709 | ///
sic >= 3712 & sic <= 3713 | ///
sic >= 3715 & sic <= 3715 | ///
sic >= 3717 & sic <= 3749 | ///
sic >= 3752 & sic <= 3791 | ///
sic >= 3793 & sic <= 3799 | ///
sic >= 3860 & sic <= 3899 | ///
sic >= 1200 & sic <= 1399 | ///
sic >= 2900 & sic <= 2999 | ///
sic >= 4900 & sic <= 4949 

replace industry5 = 3 if ///HiTec  Business Equipment, Telephone and Television Transmission
sic >= 3570 & sic <= 3579 | ///
sic >= 3622 & sic <= 3622 | ///
sic >= 3660 & sic <= 3692 | ///
sic >= 3694 & sic <= 3699 | ///
sic >= 3810 & sic <= 3839 | ///
sic >= 7370 & sic <= 7372 | ///
sic >= 7373 & sic <= 7373 | /// 
sic >= 7374 & sic <= 7374 | ///
sic >= 7375 & sic <= 7375 | ///
sic >= 7376 & sic <= 7376 | ///
sic >= 7377 & sic <= 7377 | ///
sic >= 7378 & sic <= 7378 | ///
sic >= 7379 & sic <= 7379 | ///
sic >= 7391 & sic <= 7391 | ///
sic >= 8730 & sic <= 8734 | ///
sic >= 4800 & sic <= 4899

replace industry5 = 4 if ///Hlth   Healthcare, Medical Equipment, and Drugs
sic >= 2830 & sic <= 2839 | ///
sic >= 3693 & sic <= 3693 | ///
sic >= 3840 & sic <= 3859 

replace industry5 = 1 if ///Cnsmr  Consumer Durables, NonDurables, Wholesale, Retail, and Some Services (Laundries, Repair Shops) and Hospitals and some of the 48*** that are actually services companies
sic >= 0100 & sic <= 0999 | ///
sic >= 2000 & sic <= 2399 | ///
sic >= 2700 & sic <= 2749 | ///
sic >= 2770 & sic <= 2799 | ///
sic >= 3100 & sic <= 3199 | ///
sic >= 3940 & sic <= 3989 | ///
sic >= 2500 & sic <= 2519 | ///
sic >= 2590 & sic <= 2599 | ///
sic >= 3630 & sic <= 3659 | ///
sic >= 3710 & sic <= 3711 | ///
sic >= 3714 & sic <= 3714 | ///
sic >= 3716 & sic <= 3716 | ///
sic >= 3750 & sic <= 3751 | ///
sic >= 3792 & sic <= 3792 | ///
sic >= 3900 & sic <= 3939 | ///
sic >= 3990 & sic <= 3999 | ///
sic >= 5000 & sic <= 5999 | ///
sic >= 7200 & sic <= 7299 | ///
sic >= 7600 & sic <= 7699 | ///
sic >= 8000 & sic <= 8099 | sic == 4813 | sic == 4812 | sic ==  4841 | sic == 4833 | sic == 4832



replace industry5 = 5 if industry5 == . 

