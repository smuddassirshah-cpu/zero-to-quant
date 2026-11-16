import numpy as np
rng=np.random.default_rng(7)
R=1500; sds=[]; gaps=[]; mins=[]
for r in range(R):
    X=rng.normal(size=(3000,4)); y=X@np.array([1,.5,-.5,.2])+rng.normal(0,.9,3000)
    m=[]
    for s in range(16):
        p=rng.permutation(3000); te,tr=p[:600],p[600:]
        A=np.c_[np.ones(2400),X[tr]]; b=np.linalg.lstsq(A,y[tr],rcond=None)[0]
        m.append(np.mean((y[te]-np.c_[np.ones(600),X[te]]@b)**2))
    m=np.array(m); sds.append(m.std(ddof=1)); mins.append(m.min()); gaps.append(m.mean()-m.min())
print('sd across 16 resplits of one data set',np.mean(sds),'formula',.81*np.sqrt(2/600),'x sqrt(.8)',.81*np.sqrt(2/600)*np.sqrt(.8))
print('mean best of 16',np.mean(mins),'mean gap below the 16-split average',np.mean(gaps),'share of 0.81',np.mean(gaps)/.81, '1-min/0.81', 1-np.mean(mins)/.81)
