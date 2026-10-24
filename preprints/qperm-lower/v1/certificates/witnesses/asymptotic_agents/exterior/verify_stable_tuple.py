"""Exact fixed-frame obstruction and independent PSD-tuple evaluations."""
from fractions import Fraction as F
from collections import defaultdict
from math import comb, factorial
from pathlib import Path
import json
import numpy as np

def poly_multiply(p,q):
    ans=defaultdict(F)
    for a,x in p.items():
        for b,y in q.items():
            ans[tuple(i+j for i,j in zip(a,b))]+=x*y
    return dict(ans)

def exact_polynomial(n):
    m=n-1
    top={}
    for j in range(n):
        exp=tuple(int(i==j) for i in range(n))
        top[exp]=F(1,2) if j==0 else F(1,2*m)
    bottom={tuple(int(i!=0 and i!=j) for i in range(n)):F(1,m)
            for j in range(1,n)}
    return poly_multiply(poly_multiply(top,top),bottom)

def phi_diagonal_map(n,poly):
    # All nonidentity determinant-differential terms contain an offdiagonal derivative.
    return poly.get((1,)*n,F(0))/factorial(n)

table=[]
for n in range(2,11):
    m=n-1
    p=exact_polynomial(n)
    assert sum(p.values())==1
    assert all(sum(exp[i]*c for exp,c in p.items())==1 for i in range(n))
    masses=defaultdict(F)
    for exp,c in p.items():
        masses[n-sum(x>0 for x in exp)]+=c
    expected={0:F(1,2*m),1:F(3,4)-F(1,4*m*m),2:F((m-1)**2,4*m*m)}
    assert all(masses[k]==expected[k] for k in expected)
    L=sum((-1)**k*c/comb(n,k) for k,c in masses.items())
    formula=F(-m**3+4*m*m-3*m+2,4*m**3*(m+1))
    assert L==formula
    assert phi_diagonal_map(n,p)==F(1,2*m*factorial(n))
    table.append({'n':n,'score':str(L),'n_times_score':float(n*L),
                  'true_Phi':str(phi_diagonal_map(n,p))})

numerical_checks=0
for n in range(2,10):
    m=n-1
    # Explicit orthonormal coordinates on the simplex hyperplane.
    if m==1:
        basis=np.zeros((m,0))
    else:
        mat=np.eye(m)[:,:m-1]-np.eye(m)[:,[m-1]]
        basis=np.linalg.qr(mat)[0]
    vs=basis.T
    aa=[]
    a=np.zeros((n,n));a[:2,:2]=np.eye(2)/2;aa.append(a)
    for j in range(m):
        a=np.zeros((n,n));a[:2,:2]=np.eye(2)/(2*m)
        a[2:,2:]=np.outer(vs[:,j],vs[:,j]);aa.append(a)
    assert np.linalg.norm(sum(aa)-np.eye(n))<1e-10
    assert all(abs(np.trace(a)-1)<1e-10 for a in aa)
    assert all(np.linalg.eigvalsh(a).min()>-1e-10 for a in aa)
    val=0.
    for mask in range(1<<n):
        total=np.zeros((n,n))
        for j in range(n):
            if mask>>j&1:total+=aa[j]
        k=mask.bit_count()
        val+=(n+1)*(-1)**(n-k)*np.linalg.det(total)/(k+1)
    exact=F(-m**3+4*m*m-3*m+2,4*m**3*(m+1))
    assert abs(val-float(exact))<1e-10,(n,val,float(exact))
    numerical_checks+=1

for n in range(5,1000):
    m=n-1
    assert -m**3+4*m*m-3*m+2<0

result={'status':'passed','exact_expansion_cases':9,
        'numerical_explicit_matrix_subset_checks':numerical_checks,'table':table}
Path(__file__).with_name('stable_tuple_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='table'},indent=2))
