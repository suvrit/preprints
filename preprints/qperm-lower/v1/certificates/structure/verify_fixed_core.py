"""Exact calibration of the fixed-core formulas (Python standard library only).
The all-dimensional inequalities are proved in PROOFS.md; these finite checks
verify normalizations and identities and are not substitutes for the proofs.
"""
from fractions import Fraction as F
from math import factorial, comb
from itertools import combinations
from collections import defaultdict
import json
from pathlib import Path


def falling(n, j):
    ans = 1
    for k in range(j):
        ans *= n-k
    return ans


def elementary(values, degree):
    ans = F(0)
    for subset in combinations(values, degree):
        product = F(1)
        for value in subset:
            product *= value
        ans += product
    return ans


def contract_polynomial(n, C, D=None, input_order=False):
    """Return Gamma_n(C+zD), using exact three-mask antisymmetrization."""
    D = D or {}
    rows = [[] for _ in range(n)]
    for a,b,i,j in C.keys() | D.keys():
        row = i if input_order else a
        indices = (a,b,j) if input_order else (b,i,j)
        rows[row].append((indices, (C.get((a,b,i,j),0),D.get((a,b,i,j),0))))
    states = {(0,0,0): [F(1)]}
    for entries in rows:
        nxt = {}
        for masks, values in states.items():
            for indices, polynomial in entries:
                if any(mask >> index & 1 for mask,index in zip(masks,indices)):
                    continue
                sign = (-1)**sum((mask >> (index+1)).bit_count()
                                  for mask,index in zip(masks,indices))
                key = tuple(mask | (1 << index) for mask,index in zip(masks,indices))
                target = nxt.setdefault(key,[F(0)]*(len(values)+1))
                for k,value in enumerate(values):
                    target[k] += sign*value*polynomial[0]
                    target[k+1] += sign*value*polynomial[1]
        states = {key:value for key,value in nxt.items() if any(value)}
    return states.get(((1 << n)-1,)*3,[F(0)]*(n+1))


def ad_diagonal(k):
    return {(a,b,a,b): k[a]*k[b] for a in range(len(k)) for b in range(len(k))
            if k[a]*k[b]}


def core_example(r):
    # A = Id/2 + transpose/3 + depolarizing/6.
    A = defaultdict(F)
    for a in range(r):
        for b in range(r):
            A[a,b,a,b] += F(1,2)
            A[a,b,b,a] += F(1,3)
        for i in range(r):
            A[a,a,i,i] += F(1,6*r)
    k = [F(i+1,8*r) for i in range(r)]
    K = ad_diagonal(k)
    B = {key:A.get(key,0)-K.get(key,0) for key in A.keys()|K.keys()}
    B = {key:value for key,value in B.items() if value}
    # Positivity certificate: Delta/6 - Ad_K is positive since
    # ||K||^2 <= 1/(6r); the remaining two summands are positive.
    assert max(x*x for x in k) <= F(1,6*r)
    return dict(A),k,K,B


def full_extension(A,k,n):
    r=len(k); T=dict(A)
    for a in range(r,n):
        for b in range(r,n):
            T[a,b,a,b]=F(1)
    for a in range(r):
        for b in range(r,n):
            T[a,b,a,b]=k[a]
            T[b,a,b,a]=k[a]
    return T


def main():
    results=[]
    for r in range(1,5):
        A,k,K,B=core_example(r)
        p=contract_polynomial(r,K,B)
        assert p==contract_polynomial(r,K,B,input_order=True)
        q=[p[j]/factorial(r-j) for j in range(r+1)]
        for j in range(r+1):
            assert abs(q[j]) <= falling(r,j)*elementary([x*x for x in k],r-j)
        for n in [r,r+1,r+2,2*r+3]:
            exact=sum(q[j]/falling(n,j) for j in range(r+1))
            # Gamma(shape=n-r+1) moment identity, integrated term by term.
            gamma=sum(q[j]*F(factorial(n-j),factorial(n-r))
                      for j in range(r+1))/falling(n,r)
            assert gamma==exact
            envelope=F(1)
            for x in k:
                envelope*=x*x+F(r,n)
            assert abs(exact)<=envelope
            if n<=r+1:
                direct=contract_polynomial(n,full_extension(A,k,n))[0]/factorial(n)
                assert direct==exact
            results.append({'r':r,'n':n,'Phi':str(exact),'envelope':str(envelope)})
    # Signed-coefficient calibration: R_2(X)=tr(X)I-X, Q=I.
    R=defaultdict(F)
    for a in range(2):
        for i in range(2): R[a,a,i,i]+=1
    for a in range(2):
        for b in range(2): R[a,b,a,b]-=1
    R={k:v for k,v in R.items() if v}
    pp=contract_polynomial(2,ad_diagonal([F(1),F(1)]),R)
    qq=[pp[j]/factorial(2-j) for j in range(3)]
    assert qq==[1,-2,2]
    out={'status':'all exact assertions passed','number_of_dimension_checks':len(results),
         'reduction_2_noncentral_coefficients':list(map(str,qq)),
         'checks':results,
         'scope':'Finite identities and calibrations only; see PROOFS.md for theorems.'}
    target=Path(__file__).with_name('fixed_core_verification.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
