# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 08:13:48 2021

@author: 57611

This file is to estimate intangible assets from Ewens.
"""
import os, pandas as pd, gc,numpy as np, datetime, math, matplotlib.pyplot as plt,pickle#math for log(),
from pandas.tseries.offsets import *  ##to use MonthEnd(0)
from itertools import repeat #to place ME
from scipy.stats import kurtosis, skew
from interval import Interval
from tqdm import tqdm
from statistics import stdev
import pandas_datareader, cpi#for adjusting cpi
from scipy.stats import mstats
import statsmodels.formula.api as smf #it ignores np.nan automatically
from dateutil.relativedelta import relativedelta
print(os.getcwd())
gc.collect() ##release the space

#%% estimate R&D, SG&A for years missing in Compustat, the approach follows Peters.
with open(os.getcwd()+"/dataraw/funda.data","rb") as f:
    funda=pickle.load(f)
with open(os.getcwd()+"/dataraw/company.data","rb") as f:
    company=pickle.load(f)
funda=pd.merge(funda,company, how="left",on=["gvkey"]) #gvkey==1035, 1976,1976, all nan
#sich is historial time series data, when it is missing, no way but to use sic which is header information (only most recent information)
funda['sich']=np.where(np.isnan(funda.sich),funda.sic, funda.sich)
funda['gvkey']=funda.gvkey.astype(int)
funda=funda[funda.gvkey!=175650]
funda=funda[(funda.indfmt.values=="INDL") & (funda.datafmt.values=="STD")]
funda['ipodate']=pd.to_datetime(funda.ipodate)
funda['datadate']=pd.to_datetime(funda.datadate)
funda['firstcomp']=funda.groupby('gvkey',as_index=False).fyear.transform(min)
funda=funda.dropna(subset=['fyear'],axis=0)
#xsga sometimes is negative, but still keep these records
funda[['gvkey','sich']]=funda[['gvkey','sich']].astype(int)
funda=funda.sort_values(by=['gvkey','datadate'])
funda['atnan']=np.where(np.isnan(funda['at']),1,0)
#%% We set xsga, xrd, and rdip to zero when missing. For R&D and SG&A, we make exceptions in years when the firm’s assets are also missing. For these years, we interpolate these two variables using their nearest non-missing values. We use these interpolated values to compute capital stocks but not regressions’ dependent variables
#%% for xsga, interpolate over all periods.
fxsga=[]
funda=funda.reset_index(drop=True)
funda['indexl']=funda.index.values
for i in funda.gvkey.unique():
    #gvkey==1065,1072, especially 1072 is a good example to check this for loop.
    a=funda[funda.gvkey==i].copy()
    a['xsgaf']=a.xsga
    if a.atnan.sum()>=1:
        for idx in a[(a.atnan==1)&np.isnan(a.xsga)].indexl:
            idx2=a[a.indexl<=idx].xsga.last_valid_index()
            if idx2 is None:
                b=np.nan
            else:
                b=a[a.indexl==idx2].xsga.values
                distb=idx-idx2 ##need to make sure the index is continuous
                
            idx3=a[a.indexl>idx].xsga.first_valid_index()
            if idx3 is None:
                c=np.nan
            else:
               c=a[a.indexl==idx3].xsga.values
               distc=idx3-idx
            try:
                a['xsgaf']=np.where((a.indexl==idx)&(distb<=distc),b,a.xsgaf)
                a['xsgaf']=np.where((a.indexl==idx)&(np.isnan(a.xsgaf)),c,a.xsgaf)
            except NameError:
                a['xsgaf']=np.where(a.indexl==idx,b,a.xsgaf)
                a['xsgaf']=np.where((a.indexl==idx)&(np.isnan(a.xsgaf)),c,a.xsgaf)                
    else:
        a=a
    fxsga.extend(a.xsgaf)
funda['xsga']=fxsga  

##for xrd, interpolate after 1977
fxrd=[] 
fundalater=funda[funda.fyear>=1977]
funda=funda.drop(funda[funda.fyear>=1977].index)
fundalater=fundalater.reset_index(drop=True)
fundalater['indexl']=fundalater.index.values
for i in fundalater.gvkey.unique():
    
    a=fundalater[fundalater.gvkey==i].copy()
    a['xrdf']=a.xrd
    if a.atnan.sum()>=1:
        #idx=a[a.atnan==1].indexl.tail(1)
        for idx in a[(a.atnan==1)&np.isnan(a.xrd)].indexl:
            idx2=a[a.indexl<=idx].xrd.last_valid_index()
            if idx2 is None:
                b=np.nan
            else:
                b=a[a.indexl==idx2].xrd.values
                distb=idx-idx2
            idx3=a[a.indexl>idx].xrd.first_valid_index()
            if idx3 is None:
                c=np.nan
            else:
               c=a[a.indexl==idx3].xrd.values
               distc=idx3-idx
            try:
                a['xrdf']=np.where((a.indexl==idx)&(distb<=distc),b,a.xrdf)
                a['xrdf']=np.where((a.indexl==idx)&(np.isnan(a.xrdf)),c,a.xrdf)
            except NameError:
                a['xrdf']=np.where(a.indexl==idx,b,a.xrdf)
                a['xrdf']=np.where((a.indexl==idx)&(np.isnan(a.xrdf)),c,a.xrdf)
    else:
        a=a
    fxrd.extend(a.xrdf)
fundalater['xrd']=fxrd 
funda=pd.concat([funda,fundalater],ignore_index=True)
funda=funda.sort_values(by=['gvkey','fyear'])
funda=funda.reset_index(drop=True)
funda['indexl']=funda.index.values
###We start in 1977 to give firms two years to comply with FASB’s 1975 R&D reporting requirement. If we see a firm with R&D equal to zero or missing in 1977, we assume the firm was typically not an R&D spender before 1977, so we set any missing R&D values before 1977 to zero. Otherwise, before 1977, we either interpolate between the most recent nonmissing R&D values (if such observations exist) or we use the method in Appendix A (if those observations do not exist). Starting in 1977, we make exceptions in cases in which the firm’s assets are also missing. These are likely years when the firm was privately owned. In such cases, we interpolate R&D values using the nearest non-missing values.
def xrd1977(g):
    ##if 1977 xrd is 0, all previous is 0 or missing, make values before 1977 is also 0. 
    a=g[g.fyear==1977].xrd
    if a.shape[0]!=0:
        if np.isnan(a.values[0]):
            b=np.where((g.fyear<1977)&(np.isnan(g.xrd)),0,g.xrd)
            b=np.where((g.fyear>=1977)&(np.isnan(g.xrd)),0,b)
        elif a.values[0]==0:
            b=np.where((g.fyear<1977)&(np.isnan(g.xrd)),0,g.xrd)
            b=np.where((g.fyear>=1977)&(np.isnan(g.xrd)),0,b)
        else:
            b=np.where((g.fyear>=1977)&(np.isnan(g.xrd)),0,g.xrd)
#    else:#either interpolating or backward filling later.
#after 1977, missing xrd is set to be 0 because previously we have interpolated xrd after 1977 when at is also missing.
#            else:
#                b=np.where((g.fyear>=1977)&(np.isnan(g.xrd)),0,g.xrd)
    else:
        b=np.where((g.fyear>=1977)&(np.isnan(g.xrd)),0,g.xrd)
    return b
c=[]
for i in tqdm(sorted(funda.gvkey.unique())):
    #gvkey=1010,1000,65499 are good examples
    g=funda[funda.gvkey==i]
    c.extend(xrd1977(g))
funda['xrd']=c

#%%https://github.com/edwardtkim/intangiblevalue/blob/main/2_gen_int.R
funda['xsga1']=np.where(np.isnan(funda.xsga),0,funda.xsga)-np.where(np.isnan(funda.xrd),0,funda.xrd)-np.where(np.isnan(funda.rdip),0,funda.rdip)
funda['xsga2']=np.where((np.where(np.isnan(funda.cogs),0,funda.cogs)>np.where(np.isnan(funda.xrd),0,funda.xrd)) & (np.where(np.isnan(funda.xrd),0,funda.xrd)>np.where(np.isnan(funda.xsga),0,funda.xsga)),np.where(np.isnan(funda.xsga),0,funda.xsga),funda.xsga1) 
funda['xsga3']=np.where(np.isnan(funda.xsga),np.where(np.isnan(funda.xsga),0,funda.xsga),funda.xsga2)
funda['xsga']=funda.xsga3
#######################################################################
funda['count']=funda.groupby(['gvkey']).cumcount()
funda['ageipo']=funda.fyear-funda.ipodate.dt.year
#%% calculate growth rate
#negative values exist, say gvkey=23978, year=1999
def step1(variablen):
    growthrates=pd.DataFrame(columns=['grate'])
    for i in range(1,int(funda.ageipo.max())+1):
        a=funda[funda.ageipo==i]
        b=funda[funda.ageipo==(i-1)]
        c=pd.merge(a,b[['gvkey',variablen,'ageipo']],on=['gvkey'],how='left')
        d=c[(c[variablen+'_x']>0)&(c[variablen+'_y']>0)]
        growthrates.loc[i,'grate']=(np.log(d[variablen+'_x'])-np.log(d[variablen+'_y'])).mean()
    return growthrates        
step1g_xsga=step1('xsga')
step1g_xrd=step1('xrd')
def step2(variablen):
    growthrates=pd.DataFrame(columns=['grate'])
    for i in range(1,3):
        a=funda[funda.ageipo==(i-2)]
        b=funda[funda.ageipo==(i-3)]
        c=pd.merge(a,b[['gvkey',variablen,'ageipo']],on=['gvkey'],how='left')
        d=c[(c[variablen+'_x']>0)&(c[variablen+'_y']>0)]
        growthrates.loc[i,'grate']=(np.log(d[variablen+'_x'])-np.log(d[variablen+'_y'])).mean()
    return growthrates   
step2g_xsga=step2('xsga').mean()
step2g_xrd=step2('xrd').mean()

#%% interpolating or filling missing R&D observations.
funda=funda.sort_values(by=['gvkey','fyear'])
funda=funda.reset_index(drop=True)
funda['indexl']=funda.index.values
fxrd=[] 
fundabefore=funda[funda.fyear<=1977]
funda=funda.drop(funda[funda.fyear<=1977].index)
for i in fundabefore.gvkey.unique():
    g=fundabefore[fundabefore.gvkey==i].copy()
    g['xrdf']=g.xrd
    a=g[g.fyear==1977].xrd
    if a.shape[0]!=0:
        if a.values[0]>0:
            for idx in g[np.isnan(g.xrd)].indexl:
                idx2=g[g.indexl<=idx].xrd.last_valid_index()
                if idx2 is None:
                    b=np.nan
                else:
                    b=g[g.indexl==idx2].xrd.values
                    distb=idx-idx2
                idx3=g[g.indexl>idx].xrd.first_valid_index()
                if idx3 is None:
                    c=np.nan
                else:
                   c=g[g.indexl==idx3].xrd.values
                   distc=idx3-idx
                try:
                    g['xrdf']=np.where((g.indexl==idx)&(distb<=distc),b,g.xrdf)
                    g['xrdf']=np.where((g.indexl==idx)&(np.isnan(g.xrdf)),c,g.xrdf)
                except NameError:
                    g['xrdf']=np.where(g.indexl==idx,b,g.xrdf)
                    g['xrdf']=np.where((g.indexl==idx)&(np.isnan(g.xrdf)),c,g.xrdf)          
    else:
        g=g
    fxrd.extend(g.xrdf.values)
fundabefore['xrd']=fxrd 
funda=pd.concat([funda,fundabefore],ignore_index=True)

###estimate R&D in step1
fundadj=funda[(funda.firstcomp<1977)&(np.isnan(funda.xrd))]
allnan=fundadj.groupby('gvkey').xrd.all(np.nan) ##for these, all xrd are empty, no need to do the adjustment to r&d step1.
funda['xsga']=np.where(np.isnan(funda.xsga),0,funda.xsga)
funda['xrd']=np.where(np.isnan(funda.xrd),0,funda.xrd)
funda=funda.drop(columns=['indexl','xsga1','xsga2','xsga3'])

#%% adding estimated values between IPO year and first compustat, step 4
gv=funda[funda.ageipo>0].gvkey.unique()        
fy=funda[funda.ageipo>0].groupby('gvkey',as_index=False).ipodate.apply(lambda x: x.dt.year.unique())
cusip=funda[funda.ageipo>0].groupby('gvkey').cusip.unique().apply(lambda x: np.unique(x)[0])
a=pd.DataFrame({'gvkey':gv,'fyear':fy.ipodate,'cusip':cusip.values})
funda=funda.append(a)
funda=funda.sort_values(by=['gvkey','fyear']).drop_duplicates(subset=['fyear','gvkey'],keep='last')
funda.index=pd.to_datetime(funda.fyear, format='%Y')
funda=funda.groupby('gvkey',as_index=False).resample("Y").ffill() 
funda['fyear']=funda.index.get_level_values('fyear')  
funda['fyear']=funda.fyear.dt.year
funda=funda.reset_index(drop=True)
funda=funda.sort_values(by=['gvkey','fyear'])
funda['indexl']=funda.index.values
#####################################################

funda=pd.merge(funda,step1g_xrd,left_on='ageipo',right_index=True,how='left')
funda=pd.merge(funda,step1g_xsga,left_on='ageipo',right_index=True,how='left')

funda['logxsga']=np.where(funda.xsga>=0,np.log(funda.xsga),funda.xsga)
funda['logxrd']=np.where(funda.xrd>=0,np.log(funda.xrd),funda.xrd)

c=[]
for i in funda.gvkey.unique():
    #for negative xrd values, they are not transformed to log, but still use grate to add or subtract as grate is not that large.
    g=funda[funda.gvkey==i]
    a=g[np.isnan(g.xrd)].indexl
    if a.shape[0]!=0:
        for idx in sorted(a,reverse=True):#reverse makes idx start form the newest missing value
            idx2=g[g.indexl>idx].xrd.first_valid_index()
            b=g[g.indexl==idx2].logxrd.values-g[(g.indexl<=idx2) & (g.indexl>idx)].grate_x.sum()
            g['logxrd']=np.where(g.indexl==idx,b,g.logxrd)
    else:
        g=g
    c.extend(g.logxrd)
funda['logxrd']=c

c=[]
for i in funda.gvkey.unique():
    #for negative xrd values, they are not transformed to log, but still use grate to add or subtract as grate is not that latge.
    g=funda[funda.gvkey==i]
    a=g[np.isnan(g.xsga)].indexl
    if a.shape[0]!=0:
        for idx in sorted(a,reverse=True):#reverse makes idx start form the newest missing value
            idx2=g[g.indexl>idx].xsga.first_valid_index()
            b=g[g.indexl==idx2].logxsga.values-g[(g.indexl<=idx2) & (g.indexl>idx)].grate_y.sum()
            g['logxsga']=np.where(g.indexl==idx,b,g.logxsga)
    else:
        g=g
    c.extend(g.logxsga)
funda['logxsga']=c

#%% combine founding information
ftable=pd.read_excel(os.getcwd()+'/dataraw/foundingyear.xlsx',usecols=['CUSIP','Offer Date','Founding'],dtype={'Offer Date':str,'CUSIP':str})
ftable['Founding']=np.where(ftable.Founding==-99, np.nan, ftable.Founding)
ftable['Founding']=np.where(ftable.Founding==-9, np.nan, ftable.Founding)
ftable['Founding']=np.where(ftable.Founding==201, 2013, ftable.Founding)

ftable.dropna(inplace=True)
ftable['Founding']=ftable.Founding.astype('int32')
funda['CUSIP']=funda.cusip.astype(str)
funda=pd.merge(funda,ftable,on='CUSIP',how='left')

funda.loc[funda['ipodate'].notnull(),'foundingf']=funda.firstcomp-(funda.ipodate.dt.year-8)
funda['foundingf']=np.where(funda.foundingf<=0,funda.firstcomp, (funda.ipodate.dt.year-8))
##merged by CUSIP, gvkey==19538, Founding=2016, while firstcomp=1987.
funda['Founding']=np.where(funda.Founding>funda.firstcomp,np.nan,funda.Founding)
funda['Founding']=np.where(np.isnan(funda.Founding),funda.foundingf,funda.Founding)
funda['Founding']=np.where(np.isnan(funda.Founding),funda.firstcomp,funda.Founding)
funda=funda.sort_values(by=['gvkey','fyear'])

gv=funda.gvkey.unique()         
fy=funda.groupby('gvkey',as_index=False)['Founding'].first()
cusip=funda.groupby('gvkey').cusip.unique().apply(lambda x: np.unique(x)[0])
a=pd.DataFrame({'gvkey':gv,'fyear':fy.Founding,'cusip':cusip.values})
funda=funda.append(a)
funda=funda.sort_values(by=['gvkey','fyear','count'],ascending=True,na_position='first').drop_duplicates(subset=['fyear','gvkey'],keep='last')
funda.index=pd.to_datetime(funda.fyear, format='%Y')
funda=funda.groupby('gvkey',as_index=False).resample("Y").ffill()    

funda['fyear']=funda.index.get_level_values('fyear')  
funda['fyear']=funda.fyear.dt.year
funda=funda.reset_index(drop=True)
funda=funda.sort_values(by=['gvkey','fyear'],ascending=True,na_position='last').drop_duplicates(subset=['gvkey','fyear'],keep='first')
funda=funda.reset_index(drop=True)
funda['indexl']=funda.index.values

funda['step2g_xrd']=step2g_xrd[0]
funda['step2g_xsga']=step2g_xsga[0]
funda['firstcomp']=funda.groupby('gvkey',as_index=False).firstcomp.bfill()
funda['ipodate']=funda.groupby('gvkey',as_index=False).ipodate.bfill()


c=[]
for i in funda.gvkey.unique():
    g=funda[funda.gvkey==i]
    a=g[np.isnan(g.logxrd)].indexl
    if a.shape[0]!=0:
        for idx in sorted(a,reverse=True):#reverse makes idx start form the newest missing value
            idx2=g[g.indexl>idx].logxrd.first_valid_index()
            b=g[g.indexl==idx2].logxrd.values-g[(g.indexl<=idx2) & (g.indexl>idx)].step2g_xrd.sum()
            g['logxrd']=np.where(g.indexl==idx,b,g.logxrd)
    else:
        g=g
    c.extend(g.logxrd)
funda['logxrd']=c

c=[]
for i in funda.gvkey.unique():
    #for negative xrd values, they are not transformed to log, but still use grate to add or subtract as grate is not that latge.
    g=funda[funda.gvkey==i]
    a=g[np.isnan(g.logxsga)].indexl
    if a.shape[0]!=0:
        for idx in sorted(a,reverse=True):#reverse makes idx start form the newest missing value
            idx2=g[g.indexl>idx].logxsga.first_valid_index()
            b=g[g.indexl==idx2].logxsga.values-g[(g.indexl<=idx2) & (g.indexl>idx)].step2g_xsga.sum()
            g['logxsga']=np.where(g.indexl==idx,b,g.logxsga)
    else:
        g=g
    c.extend(g.logxsga)
funda['logxsga']=c

funda['logxsga']=funda.logxsga.astype('float')
funda['xsga']=np.where(~(funda.xsga<0),np.exp(funda.logxsga),funda.xsga)
funda['logxrd']=funda.logxrd.astype('float')
funda['xrd']=np.where(~(funda.xrd<0),np.exp(funda.logxrd),funda.xrd)
funda=funda.sort_values(by=['gvkey','fyear','count'],ascending=True,na_position='first').drop_duplicates(subset=['fyear','gvkey'],keep='last')

##################################################
##parameters for d_{XRD} from Ewens   
sicg1=[3714,3716,3750,3751,3792,4813,4812,4841,4833,4832]+list(range(100,1000))+list(range(2000,2400))+list(range(2700,2750))+list(range(2770,2800))+list(range(3100,3200))+list(range(3940,3990))+list(range(2500,2520))+list(range(2590,2600))+list(range(3630,3660))+list(range(3710,3712))+list(range(3900,3940))+list(range(3990,4000))+list(range(5000,6000))+list(range(7200,7300))+list(range(7600,7700))+list(range(8000,8100))
sicg2=list(range(2520,2590))+list(range(2600,2700))+list(range(2750,2770))+list(range(2800,2830))+list(range(2840,2900))+list(range(3000,3100))+list(range(3200,3570))+list(range(3580,3622))+list(range(3623,3630))+list(range(3700,3710))+list(range(3712,3714))+list(range(3715,3716))+list(range(3717,3750))+list(range(3752,3792))+list(range(3793,3800))+list(range(3860,3900))+list(range(1200,1400))+list(range(2900,3000))+list(range(4900,4950))
sicg3=[3622,7391]+list(range(3570,3580))+list(range(3660,3693))+list(range(3694,3700))+list(range(3810,3840))+list(range(7370,7380))+list(range(8730,8735))+list(range(4800,4900))
sicg4=list(range(2830,2840))+list(range(3693,3694))+list(range(3840,3860))

def genkcap(g):
    "Be sure the first column of g is desired intangible capital, second column is parameter for knowledge depreciation rate, third column if current period variable (eg, xrd)."
    n=len(g.xrd)
    for i in range(1,n):
        g.iloc[i,0]=g.iloc[i-1,0]*(1-g.iloc[i,1])+g.iloc[i,2] #warning checked, no problem.
    return g

def genocap(g):
    "Be sure the first column of g is desired intangible capital, second column is parameter for contribution rate, third column if current period variable (eg, sg&a)."
    n=len(g['xsga'])
    for i in range(1,n):
        g.iloc[i,0]=g.iloc[i-1,0]*0.8+g.iloc[i,2]*g.iloc[i,1] #warning checked, no problem.
    return g

funda["theta_g2"]=np.where(funda['sich'].isin(sicg1), 0.33,np.where(
        funda['sich'].isin(sicg2), 0.42,np.where(
                funda['sich'].isin(sicg3), 0.46,np.where(
                        funda.sich.isin(sicg4),0.34,0.3))))

funda['gamma_o2']=np.where(funda['sich'].isin(sicg1), 0.19,np.where(
        funda['sich'].isin(sicg2), 0.22,np.where(
                funda['sich'].isin(sicg3), 0.44,np.where(
                        funda.sich.isin(sicg4),0.49,0.34))))
funda['kcap_v2']=0
funda['ocap_v2']=0
funda['kcap_v2']=funda.groupby('gvkey',as_index=False)[['kcap_v2','theta_g2','xrd']].apply(genkcap).kcap_v2
funda['ocap_v2']=funda.groupby('gvkey',as_index=False)[['ocap_v2','gamma_o2','xsga']].apply(genocap).ocap_v2
##################################################
funda=funda[funda['count']>=0]
tokeep=funda[['gvkey','fyear','kcap_v1','kcap_v2','ocap_v1','ocap_v2']]
tokeep.to_csv(os.getcwd()+"/pipeline/Peter&Ewens.csv")


#%% to compare with Ewens data
#above 0.99
tokeep=pd.read_csv(os.getcwd()+"/pipeline/Peter&Ewens.csv")
with open(os.getcwd()+"/dataraw/peters.data","rb") as f:
    peters=pickle.load(f)
Intassets=pd.read_csv(os.getcwd()+"/dataraw/intangibleCapital_122919.csv")
merged=pd.merge(tokeep, Intassets[["fyear","gvkey","orgCapital","knowCapital"]], on=["gvkey","fyear"],how="left")
merged1=merged.dropna(subset=['knowCapital','kcap_v1'],how='any')
np.corrcoef(merged1.kcap_v2,merged1.knowCapital)
merged2=merged.dropna(subset=['orgCapital','ocap_v1'],how='any')
np.corrcoef(merged2.ocap_v2,merged2.orgCapital)
