"""Small numerical regression checks for Stata semantics; run with python3."""
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
from sample import lag, winsor, stock_fields, WORK
import fig01_rd_capex as f01
import fig09_roe as f09

d=pd.DataFrame({'gvkey':[1,1,1,2],'fyear':[1975,1976,1978,1977],'x':[2.,3.,4.,9.]})
assert lag(d,'x').tolist()[1]==2
assert lag(d,'x').isna().tolist()==[True,False,True,True]
x=pd.Series([0.,1.,2.,3.,100.,np.nan])
np.testing.assert_allclose(winsor(x,.025).iloc[[0,4]], [.1,90.3])
assert pd.isna(winsor(x,.025).iloc[5])
assert winsor(x,.025,highonly=True).iloc[0]==0
p=pd.DataFrame({'gvkey':[1,1,1],'fyear':[1975,1977,1978], 'G2':[10.,20.,30.],'S2':[5.,8.,10.],'knowDepr':[.4]*3,'gamma':[.2]*3,'sic':[2000]*3,'industry5':[1]*3,'cpidef':[2.]*3,'intan':[2.,2.,2.],'ppegt':[20.,20.,20.]})
with tempfile.TemporaryDirectory(dir=WORK) as tmp:
    path=Path(tmp)/'panel.csv'
    p.to_csv(path,index=False)
    s=stock_fields(path)
    np.testing.assert_allclose(s.G2depr,[0.,1.6,8.])
    np.testing.assert_allclose(s.S2depr,[0.,.2,1.6])
    assert pd.isna(s.intensity2.iloc[1])
    np.testing.assert_allclose(s.intensity2.iloc[2],29/39)
# Missing numerator becomes zero even when the observed lag denominator is zero.
r=pd.DataFrame({'gvkey':[1,1],'fyear':[1976,1977],'at':[0.,2.],'xrd':[np.nan,np.nan],'xsga':[np.nan,np.nan],'capx':[np.nan,np.nan]})
assert f01.compute(r).rdAssets.iloc[0]==0
# Membership exclusions must occur before the ROE lag, preventing a false bridge.
r=pd.DataFrame({'gvkey':[1,1,1],'fyear':[1977,1978,1979],'sp500':[1,0,1], 'ceq':[10.]*3,'G2':[2.]*3,'S2':[3.]*3,'ni':[1.]*3,'xrd':[1.]*3,'xsga':[2.]*3,'gamma':[.2]*3,'S2depr':[.2]*3,'G2depr':[.4]*3,'marginal_tax_after_int':[.35]*3})
assert f09.compute(r).roe_inc2.isna().all()
print('Numerical checks passed: calendar lags, winsorization, depreciation across gaps, intensity timing, missing numerators and membership-screen timing.')
