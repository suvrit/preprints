"""Verify archived n4--12 and new certificates using exact rational arithmetic.

No optimizer or external numerical package is imported by this verifier.
The sparse model has precisely the archived row and column ordering.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,time
from sparse_extend import build,verify
from spectral_model import partitions
from fast_adapter import profile_dp
ROOT=Path(__file__).resolve().parent.parent

def main():
    gamma={2:Q(0),3:Q(0)};records=[]
    for n in range(4,30):
        p=ROOT/'certificates'/(f'recursive_cert_{n}.json' if n<8 else f'dual_{n}.json')
        if not p.exists():break
        t=time.time();cert=json.loads(p.read_text())
        used={int(k):Q(v) for k,v in cert['gammas'].items()}
        assert all(k in gamma and g<=gamma[k] for k,g in used.items())
        m=build(n,used);value=verify(m,list(map(Q,cert['dual'])))
        assert value==Q(cert['objective'] if n<8 else cert['lower'])
        if n<8:
            x=list(map(Q,cert['primal']));assert len(x)==len(m['c']) and min(x)>=0
            assert all(sum(v*x[j] for j,v in row.items())==b for row,b in zip(m['A'],m['b']))
            assert sum(c*a for c,a in zip(m['c'],x))==value
        gamma[n]=value if n<8 else Q(cert['floor'])
        assert value>=gamma[n]
        assert gamma[n]>=-Q(1,n),('bound not useful',n)
        records.append({'n':n,'floor':str(gamma[n]),'exact_dual_value':str(value),'rows':len(m['A']),'variables':len(m['c']), 'nonzeros':sum(map(len,m['A']))})
        print('VERIFIED',n,str(gamma[n]),'seconds',round(time.time()-t,3),flush=True)
    # Independent direct combinatorial formula (not using dynamic programming).
    from itertools import combinations
    from math import comb
    cases=0
    for n in range(2,10):
        for lam in partitions(n):
            padded=lam+(0,)*(n-len(lam))
            for k in range(1,n//2+1):
                sums=[sum(padded[i] for i in I) for I in combinations(range(n),k)]
                direct=tuple(Q(sum(comb(s,j) if s>=j else 0 for s in sums),comb(n,k)) for j in range(n+1))
                assert direct==profile_dp(lam,k);cases+=1
    # Independent expanded Vandermonde differentiation through total degree 7.
    from radial_schur import radial,directional
    from radial_exact import radial_fast,diagonal_derivative
    dcases=0
    for degree in range(8):
        for mu in partitions(degree):
            for k in range(1,max(2,degree+1)):
                if len(mu)>k:continue
                assert radial(mu,k)==radial_fast(mu,k)
                assert directional(mu,k)==diagonal_derivative(mu,k)
                dcases+=1
    out={'all_passed':True,'certificates':records,'direct_profile_checks':cases,'independent_derivative_checks':dcases}
    (ROOT/'finite_verification_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('ALL EXACT CHECKS PASSED',cases,'profile cases',dcases,'derivative cases',flush=True)
if __name__=='__main__':main()
