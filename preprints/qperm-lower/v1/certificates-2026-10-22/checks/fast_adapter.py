"""Exact interface adapter and accelerations for the archived model.

profile_dp computes exactly the same uniform subset sums as profile(), by the
integer coefficient array of product_i (1+u z^{lambda_i}).
"""
from fractions import Fraction as Q
from math import comb
from functools import lru_cache
import spectral_model

@lru_cache(None)
def profile_dp(lam,k):
    n=sum(lam);dp={(0,0):1}
    for a in lam+(0,)*(n-len(lam)):
        nd=dp.copy()
        for (r,s),v in dp.items():
            if r<k:nd[r+1,s+a]=nd.get((r+1,s+a),0)+v
        dp=nd
    dist={s:v for (r,s),v in dp.items() if r==k}
    assert sum(dist.values())==comb(n,k)
    return tuple(Q(sum(v*comb(s,j) for s,v in dist.items() if s>=j),comb(n,k)) for j in range(n+1))

def asdict(m):
    return {'A':m.matrix,'b':m.rhs,'c':m.objective,'parts':m.partitions}

def sparse_rows(m):return [[(j,v) for j,v in enumerate(row) if v] for row in m['A']]

def rational_dual(m,result,denominator=10**18):
    rows=sparse_rows(m)
    y=[Q(round(float(v)*denominator),denominator) for v in result.eqlin.marginals]
    col=[[] for _ in m['c']]
    for i,row in enumerate(rows):
        for j,v in row:col[j].append((i,v))
    for j in range(len(m['parts']),len(m['c'])):
        if len(col[j])==1 and col[j][0][1]<0 and m['c'][j]==0:
            i=col[j][0][0];y[i]=max(Q(0),y[i])
    simplexes=[]
    for i,row in enumerate(rows):
        if m['b'][i]==1 and row and all(v==1 for j,v in row):
            y[i]=0;simplexes.append((i,[j for j,v in row]))
    residual=m['c'].copy()
    for row,v in zip(rows,y):
        if v:
            for j,a in row:residual[j]-=a*v
    for i,group in simplexes:
        y[i]=min(residual[j] for j in group)
        for j in group:residual[j]-=y[i]
    assert min(residual)>=0,min(residual)
    return sum(b*v for b,v in zip(m['b'],y)),y

def verify_dual(m,y):
    assert len(y)==len(m.matrix),(len(y),len(m.matrix))
    residual=m.objective.copy()
    for row,v in zip(m.matrix,y):
        if v:
            for j,a in enumerate(row):
                if a:residual[j]-=a*v
    assert min(residual)>=0,min(residual)
    return sum(b*v for b,v in zip(m.rhs,y))
