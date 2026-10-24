"""Exact checks for the rational-envelope structure theorem.

Python standard library only. Inherited finite dual certificates are separate
proof inputs; --seeds reconstructs and verifies all of them through rank 18.
The default verifies the new identities and all finite comparisons.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import comb, factorial
import sys, json, argparse
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'finite/checks'))
from sparse_extend import build,verify,load_gammas
from mixed_model import mixed_rows
from spectral_model import partitions

def K(k,g): return Q((k-1)*(1+k*g),1-g)
def h(n,kappa): return -Q(n-1-kappa,n*(n-1)+kappa)
def clean(n): return -Q(n-2,n*n+4*n+8)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',action='store_true');args=ap.parse_args()
    seeds=load_gammas(18)
    if args.seeds:
        for n in range(4,19):
            name=f'recursive_cert_{n}.json' if n<8 else f'dual_{n}.json'
            cert=json.loads((ROOT.parent/'finite/certificates'/name).read_text())
            gam={int(k):Q(v) for k,v in cert['gammas'].items()}
            assert all(v<=seeds[k] for k,v in gam.items())
            model=build(n,gam)
            value=verify(model,list(map(Q,cert['dual'])))
            assert value==Q(cert['objective'] if n<8 else cert['lower'])
            assert value>=seeds[n]
            print('verified inherited seed',n,flush=True)
    comparisons=[]
    for n in range(4,19):
        assert seeds[n]>=clean(n)
        comparisons.append({'n':n,'certified_floor':str(seeds[n]),'clean_floor':str(clean(n))})
    # Exact all-dimensional comparison numerator:
    # clean(n)-[-5n/(5n^2+31n+190)] is nonpositive for n>=8.
    # Its opposite has numerator n^2+88n-380.
    assert 8*8+88*8-380>0
    # The integer-wide absolute floor follows from (n-6)(n-7)>=0.
    for n in range(2,250):
        assert clean(n)>=-Q(1,17)
        assert n*n+4*n+8-17*(n-2)==(n-6)*(n-7)
        if n>=8:
            old=-Q(5*n,5*n*n+31*n+190)
            assert old-clean(n)==Q(n*n+88*n-380,(5*n*n+31*n+190)*(n*n+4*n+8))>0
    cases=0;entries=0
    for n in range(4,11):
        ps=tuple(partitions(n));N=n*(n-1)
        for k in range(2,n):
            m=n-k
            for g in (Q(0),-Q(1,2*k),-Q(1,k)):
                rows=mixed_rows(n,ps,{k:g})
                for kap in (Q(2),K(k,g),K(k,g)+1):
                    w=[Q(0)]*len(ps)
                    w[ps.index((1,)*n)]=Q(kap,N+kap)
                    w[ps.index((2,)+(1,)*(n-2))]=Q(N,N+kap)
                    assert sum(w)==1
                    score=sum(Q((-1)**(n-len(p)),comb(n,len(p)))*v for p,v in zip(ps,w))
                    assert score==h(n,kap)
                    f=Q(factorial(k),N+kap)
                    expected={
                      (k,(),(1,)*m):f*(1-g)*(kap-K(k,g)),
                      (k,(1,),(1,)*(m-1)):f*(k+1)*(Q(1,k)-g),
                    }
                    if m>=2:expected[k,(),(2,)+(1,)*(m-2)]=f*(1-g)
                    for key in rows.keys()|expected.keys():
                        actual=sum(a*b for a,b in zip(rows.get(key,[Q(0)]*len(ps)),w))
                        assert actual==expected.get(key,Q(0)),(n,k,g,kap,key,actual,expected.get(key))
                        entries+=1
                    assert all(v>=0 for v in expected.values())==(kap>=K(k,g))
                    cases+=1
        for kap in (Q(2),Q(31,5),Q(n-1)):
            assert Q(kap,N+kap)>=Q(factorial(n),n**n)
            k=n//2
            c=Q(k*(n-k),N+kap)
            assert (c<=Q(1,4))==(kap>=4*k*(n-k)-N)
    # A single polynomial passes every proper-dimensional zero-seed row.
    growing_seed_entries=0
    for n in range(4,13):
        ps=tuple(partitions(n));N=n*(n-1);kap=n-2
        w=[Q(0)]*len(ps)
        w[ps.index((1,)*n)]=Q(kap,N+kap)
        w[ps.index((2,)+(1,)*(n-2))]=Q(N,N+kap)
        assert sum(Q((-1)**(n-len(p)),comb(n,len(p)))*v for p,v in zip(ps,w))==-Q(1,n*n-2)
        for k in range(2,n):
            rows=mixed_rows(n,ps,{k:Q(0)})
            for row in rows.values():
                assert sum(a*b for a,b in zip(row,w))>=0
                growing_seed_entries+=1
    # Strict residuals in the all-dimensional transport certificate.
    strict_cases=0
    def fall(n,j):
        ans=1
        for a in range(j):ans*=n-a
        return ans
    for k in range(3,10):
        for n in range(k+3,k+9):
            for g in (Q(0),-Q(1,2*k),-Q(1,k)):
                kap=K(k,g); a=1-g; den=a*(n*(n-1)+kap)
                t=Q(n*n-1,den); eta=(Q(1,n)+h(n,kap)) if n%2==0 else Q(0)
                for part in partitions(n):
                    J=Q(0)
                    if part.count(1)>=n-k:
                        mu=list(part)
                        for _ in range(n-k):mu.remove(1)
                        j=k-len(mu);s0=k-mu.count(1)
                        J=Q(fall(k,s0),fall(n,s0))*(Q((-1)**j,comb(k,j))-g)
                    R=Q(1,n-1) if part==(n-1,1) else -Q(1) if part==(n,) else Q(0)
                    residual=Q((-1)**(n-len(part)),comb(n,len(part)))-h(n,kap)-t*J-eta*R
                    assert residual>=0
                    zero_shapes={(1,)*n,(2,)+(1,)*(n-2)}
                    if n%2==0:zero_shapes.add((n,))
                    if g>-Q(1,k):assert (residual==0)==(part in zero_shapes)
                    strict_cases+=1
    # The rank-five endpoint has a short rank-three-only certificate.
    n=5;ps=tuple(partitions(n));rows=mixed_rows(n,ps,{3:Q(0)})
    residual=[]
    for i,p in enumerate(ps):
        v=Q((-1)**(n-len(p)),comb(n,len(p)))+Q(1,11)
        v-=Q(1,55)*rows[3,(2,),()][i]+Q(2,11)*rows[3,(),(1,1)][i]
        assert v>=0;residual.append(str(v))
    out={'status':'passed','coefficient_identity_parameter_cases':cases,
         'individual_coefficient_checks':entries,'uniform_floor_comparisons':comparisons,
         'all_inherited_seeds_reverified':bool(args.seeds),
         'rank_five_residuals':residual,'transport_residual_checks':strict_cases,'all_proper_zero_seed_coefficient_checks':growing_seed_entries,
         'scope':'The all-dimensional claims are proved in PROOFS.md; finite checks calibrate the formulas.'}
    (ROOT/'rational_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','coefficient_identity_parameter_cases','individual_coefficient_checks','all_inherited_seeds_reverified']},indent=2))
if __name__=='__main__':main()
