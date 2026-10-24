"""Independent exact checks of the new projection and exterior formulas.

No radial/Schur model builder is imported. All arithmetic is rational.
These finite checks calibrate the manuscript proofs; they are not a proof
of its infinite-dimensional families of inequalities.
"""
from fractions import Fraction as Q
from itertools import permutations, combinations
from math import factorial, prod
from pathlib import Path
import json
from verify_fixed_core import core_example


def sign(p):
    return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))


def minor_pair(B,I,J,K,L):
    j=len(I); ps=list(permutations(range(j))); total=Q(0)
    for p in ps:
        for q in ps:
            for t in ps:
                total+=sign(p)*sign(q)*prod(B.get((I[a],K[t[a]],J[p[a]],L[q[t[a]]]),Q(0)) for a in range(j))
    return total


def antisymmetric_entry(B,I,J,K,L):
    j=len(I); ps=list(permutations(range(j))); total=Q(0)
    for p in ps:
        for q in ps:
            for t in ps:
                for u in ps:
                    total+=sign(p)*sign(q)*sign(t)*sign(u)*prod(B.get((I[p[a]],K[q[a]],J[t[a]],L[u[a]]),Q(0)) for a in range(j))
    return total/Q(factorial(j)**2)


def multiply(p,q):
    ans=[Q(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):ans[i+j]+=a*b
    return ans


def power(p,d):
    ans=[Q(1)]
    for _ in range(d):ans=multiply(ans,p)
    return ans


def add(p,q,scale=1):
    ans=p+[Q(0)]*max(0,len(q)-len(p))
    for i,a in enumerate(q):ans[i]+=scale*a
    return ans


def elementary_poly(values,d):
    ans=[Q(0)]
    for subset in combinations(values,d):
        term=[Q(1)]
        for p in subset:term=multiply(term,p)
        ans=add(ans,term)
    return ans


def main():
    exterior_checks=0
    for r in range(1,4):
        A,ks,K,B=core_example(r)
        # Id, transpose, and the admissible non-CP residual give distinct
        # covariance patterns; direct Wick pairings and antisymmetrization
        # are evaluated independently.
        maps=[{(a,b,a,b):Q(1) for a in range(r) for b in range(r)},
              {(a,b,b,a):Q(1) for a in range(r) for b in range(r)},B]
        for M in maps:
            for j in range(1,r+1):
                sets=list(combinations(range(r),j))
                for I in sets:
                    for J in sets:
                        for K0 in sets:
                            for L in sets:
                                assert minor_pair(M,I,J,K0,L)==factorial(j)*antisymmetric_entry(M,I,J,K0,L)
                                exterior_checks+=1
    projection_checks=0
    for n in range(4,12):
        N=n*(n-1)
        for kap in (Q(2),Q(31,5),Q(n-2),Q(n),Q(n+1)):
            for a in range(1,n):
                values=[[Q(1),Q(1)]]*a+[[Q(0),Q(1)]]*(n-a)
                en=elementary_poly(values,n)
                e1=elementary_poly(values,1)
                en1=elementary_poly(values,n-1)
                actual=[x/(N+kap) for x in add(multiply(e1,en1),en,-(n-kap))]
                expect=multiply(multiply(power([Q(0),Q(1)],n-a-1),power([Q(1),Q(1)],a-1)),[Q(a*(n-a),N+kap),Q(1),Q(1)])
                assert actual==expect,(n,a,kap)
                projection_checks+=1
    phase_checks=0
    for r in range(2,6):
        # Reduction map normalized to be bistochastic; beta<=1 is certified.
        B={(a,a,i,i):Q(1,r-1) for a in range(r) for i in range(r)}
        for a in range(r):
            for b in range(r):B[a,b,a,b]=B.get((a,b,a,b),Q(0))-Q(1,r-1)
        for ks in ([Q(i+1,2*r) for i in range(r)], [Q(0)]+[Q(1,3)]*(r-1)):
            P=prod(ks);ss=[prod(ks[a] for a in range(r) if a!=i) for i in range(r)]
            c1=sum(ss[i]*ss[j]*B.get((i,j,i,j),Q(0)) for i in range(r) for j in range(r))
            R=sum(B.get((i,i,h,h),Q(0))*prod(ks[a] for a in range(r) if a not in (i,h)) for i in range(r) for h in range(r) if i!=h)
            e= sum(prod(ks[a]**2 for a in subset) for subset in combinations(range(r),r-2))
            assert c1>=-P*R
            assert R*R<=2*r*e
            for n in (r,r+1,2*r+3):
                assert P*P+c1/n>=-Q(r,2*n*n)*e
                phase_checks+=1
    out={'status':'passed','exact_minor_Wick_antisymmetry_checks':exterior_checks,
         'exact_projection_polynomial_checks':projection_checks,
         'signed_phase_and_square_checks':phase_checks,
         'scope':'Finite independent algebra controls; see manuscript for general proofs.'}
    Path(__file__).with_name('independent_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
