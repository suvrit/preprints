"""Sparse exact LP extension; deterministic rational model, floating proposal.
All accepted certificates are checked using Fraction only.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import lcm
import json,time,sys
import mixed_model,spectral_model
from radial_schur import radial,directional
from fast_adapter import profile_dp
mixed_model.radial_fast=radial;mixed_model.diagonal_derivative=directional
spectral_model.profile=profile_dp
ROOT=Path(__file__).resolve().parent.parent

def build(n,gamma):
    m=spectral_model.build_strengthened(n)
    A=[{j:v for j,v in enumerate(row) if v} for row in m.matrix]
    b=m.rhs;c=m.objective;meta=m.row_metadata
    for key,row in mixed_model.mixed_rows(n,m.partitions,gamma).items():
        if min(row)>=0:continue
        mult=lcm(*(v.denominator for v in row));ints=[int(v*mult) for v in row];scale=max(map(abs,ints))
        rr={j:Q(v,scale) for j,v in enumerate(ints) if v}
        rr[len(c)]=Q(-1);A.append(rr);b.append(Q(0));c.append(Q(0));meta.append(['mixed_small_rank',key])
    return {'A':A,'b':b,'c':c,'parts':m.partitions,'meta':meta}

def solve(m,method='highs',spectral_degree=8):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    r=[];co=[];v=[];scales=[];used=[]
    for i,row in enumerate(m['A']):
        if m['meta'][i][0]=='spectral' and m['meta'][i][2]>spectral_degree: continue
        ii=len(used);used.append(i)
        sc=max(map(abs,row.values()));scales.append(sc)
        for j,a in row.items():r.append(ii);co.append(j);v.append(float(a/sc))
    A=coo_matrix((v,(r,co)),shape=(len(used),len(m['c']))).tocsr()
    result=linprog(list(map(float,m['c'])),A_eq=A,b_eq=[float(b/sc) for b,sc in zip([m['b'][i] for i in used],scales)],bounds=(0,None),method=method,options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'small_matrix_value':1e-12})
    if not result.success:raise RuntimeError(result.message)
    result.original_dual=[0.0]*len(m['A'])
    outscales=[Q(1)]*len(m['A'])
    for j,i in enumerate(used):result.original_dual[i]=result.eqlin.marginals[j];outscales[i]=scales[j]
    return result,outscales

def dual_bound(m,result,scales,denominator=10**16):
    y=[Q(round(float(v)*denominator),denominator)/s for v,s in zip(result.original_dual,scales)]
    col=[[] for _ in m['c']]
    for i,row in enumerate(m['A']):
        for j,v in row.items():col[j].append((i,v))
    for j in range(len(m['parts']),len(m['c'])):
        if len(col[j])==1 and col[j][0][1]<0 and m['c'][j]==0:
            i=col[j][0][0];y[i]=max(Q(0),y[i])
    simplexes=[]
    for i,row in enumerate(m['A']):
        if m['b'][i]==1 and row and all(v==1 for v in row.values()):
            y[i]=0;simplexes.append((i,list(row)))
    residual=m['c'].copy()
    for row,v in zip(m['A'],y):
        if v:
            for j,a in row.items():residual[j]-=a*v
    for i,group in simplexes:
        y[i]=min(residual[j] for j in group)
        for j in group:residual[j]-=y[i]
    assert min(residual)>=0
    return sum(b*v for b,v in zip(m['b'],y)),y

def verify(m,y):
    assert len(y)==len(m['A'])
    r=m['c'].copy()
    for row,v in zip(m['A'],y):
        if v:
            for j,a in row.items():r[j]-=a*v
    assert min(r)>=0,min(r)
    return sum(b*v for b,v in zip(m['b'],y))

def load_gammas(maxn=12):
    gamma={2:Q(0),3:Q(0)}
    for n in range(4,maxn+1):
        cert=json.loads((ROOT/'certificates'/(f'recursive_cert_{n}.json' if n<8 else f'dual_{n}.json')).read_text())
        gamma[n]=Q(cert['objective'] if n<8 else cert['floor'])
    return gamma

def main():
    startn=int(sys.argv[1]) if len(sys.argv)>1 else 13
    endn=int(sys.argv[2]) if len(sys.argv)>2 else 17
    gamma=load_gammas(startn-1)
    for n in range(startn,endn+1):
        t=time.time();m=build(n,gamma)
        print('built sparse',n,'rows',len(m['A']),'vars',len(m['c']),'nonzero',sum(map(len,m['A'])),'seconds',round(time.time()-t,3),flush=True)
        degree=int(sys.argv[3]) if len(sys.argv)>3 else 10
        result,scales=solve(m,spectral_degree=degree);value,y=dual_bound(m,result,scales)
        assert verify(m,y)==value
        floor=Q(value.numerator*10**10//value.denominator,10**10)
        destination=ROOT/'certificates'/f'dual_{n}.json'
        if destination.exists():
            previous=json.loads(destination.read_text())
            previous_floor=Q(previous['floor'])
            if floor<=previous_floor:
                gamma[n]=previous_floor
                print('RETAINED stronger existing certificate',n,'floor',str(previous_floor),'candidate',str(floor),'LP',result.fun,flush=True)
                continue
        assert floor >= -Q(1,n), 'Numerical repair gave no useful bound; refusing to replace a certificate'
        cert={'n':n,'gammas':{str(k):str(v) for k,v in gamma.items()},'lower':str(value),'floor':str(floor),'dual':list(map(str,y)),'status':'exact feasible dual certificate, no optimality assertion'}
        destination.write_text(json.dumps(cert,indent=2)+'\n')
        kappa=(n-1)*(1+n*floor)/(1-floor)
        print('CERTIFIED',n,'floor',str(floor),'decimal',float(floor),'kappa',str(kappa),float(kappa),'LP',result.fun,'seconds',round(time.time()-t,3),flush=True)
        gamma[n]=floor
if __name__=='__main__':main()
