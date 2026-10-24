"""Exact coefficient certificates for all-dimensional transport.

Polynomial arrays are in increasing powers; all arithmetic is rational.  The
certified shift coefficients prove nonnegativity for every real N >= k+1,
not only for the finite dimensions printed in the note.
"""
from fractions import Fraction as Q
from math import comb, factorial




def trim(p):
    p = list(map(Q,p))
    while len(p)>1 and p[-1]==0:p.pop()
    return p

def add(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,x in enumerate(p):out[i]+=x
    for i,x in enumerate(q):out[i]+=x
    return trim(out)

def scale(p,a):return trim([a*x for x in p])

def mul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return trim(out)

def falling(offset,count):
    out=[Q(1)]
    for i in range(count):out=mul(out,[-offset-i,1])
    return out

def shift(p,a):
    out=[Q(0)]*len(p)
    for i,c in enumerate(p):
        for j in range(i+1):out[j]+=c*comb(i,j)*a**(i-j)
    return trim(out)

def evaluate(p,x):
    v=Q(0)
    for c in reversed(p):v=v*x+c
    return v

def parameters(k,gamma):
    a=1-gamma; b=(k-1)*(1+k*gamma)
    return a,b,b/a

def target(n,kappa):
    return -Q(n-1-kappa, n*(n-1)+kappa)

def cleared_polynomial(mu,k,gamma):
    j=k-len(mu); s=k-mu.count(1)
    a,b,kappa=parameters(k,gamma)
    D=[b,-a,a]
    out=scale(mul(D,falling(j,s-j)),(-1)**j*factorial(j))
    out=add(out,mul([-a-b,a],falling(0,s)))
    factor=Q((-1)**j,comb(k,j))-gamma
    falling_k=factorial(k)//factorial(k-s)
    out=add(out,scale([-1,0,1],-falling_k*factor))
    return trim(out)

def mixed_row(n,k,gamma,lam):
    tail=n-k
    if lam.count(1)<tail:return Q(0)
    # Remove the prescribed inactive square-free part.
    mu=tuple(lam[:len(lam)-tail]) if tail else lam
    assert sum(mu)==k
    j=k-len(mu);s=k-mu.count(1)
    ratio=Q(factorial(k)*factorial(n-s),factorial(k-s)*factorial(n))
    return ratio*(Q((-1)**j,comb(k,j))-gamma)

def rank_two_row(n,lam):
    if lam==(n,):return Q(-1)
    if lam==(n-1,1):return Q(1,n-1)
    return Q(0)


# Every selected coefficient depends only on j=k-length(mu), s=k-m_1(mu).
# These representatives realize all possible pairs.
def representatives(k):
    yield (1,)*k
    for j in range(1,k):
        for s in range(j+1,min(2*j,k)+1):
            r=s-j
            yield (2+j-r,)+(2,)*(r-1)+(1,)*(k-s)

def certify_seed(k,gamma,n0):
    a,b,K=parameters(k,gamma)
    assert -Q(1,k)<=gamma<=0
    assert 0<=K<n0
    assert (n0-3-K)*n0*(n0-1)>=2*K
    rows=[]
    for mu in representatives(k):
        poly=cleared_polynomial(mu,k,gamma)
        cs=shift(poly,n0)
        assert min(cs)>=0,(k,gamma,mu,n0,cs)
        # Independently check polynomial against the original rational residual.
        for n in (max(n0,k+1),max(n0,k+1)+2):
            lam=tuple(sorted(mu+(1,)*(n-k),reverse=True))
            h=target(n,K);t=Q(n*n-1,a*n*(n-1)+b)
            residual=Q((-1)**(n-len(lam)),comb(n,len(lam)))-h-t*mixed_row(n,k,gamma,lam)
            s=k-mu.count(1)
            multiplier=(a*n*(n-1)+b)*Q(factorial(n),factorial(n-s))
            assert evaluate(poly,n)==residual*multiplier
        rows.append({'j':k-len(mu),'s':k-mu.count(1),'shifted_coefficients':list(map(str,cs))})
    # The only selected coefficient possibly changed by the parity correction.
    for n in (n0,n0+1,n0+2):
        if n%2:continue
        N=n*(n-1);h=target(n,K);t=Q(n*n-1,a*N+b)
        eta=Q(1,n)+h
        assert eta>=0 and -Q(1,n)-h+eta==0
        lam=(n-1,1)
        c=Q(2,N)-h-t*mixed_row(n,k,gamma,lam)-eta/Q(n-1)
        if n==k+1:
            expected=Q(n+1,n*(N+K))*(1-gamma*(n*n-3*n+3))/(1-gamma)
        else:
            expected=Q((n+1)*(n-K),n*(N+K))
        assert c==expected>0
    return {'k':k,'gamma':str(gamma),'kappa':str(K),'kappa_decimal':float(K),'minimum_dimension':n0,'rows':rows}

def check_general_endpoints():
    # These basic finite tests supplement, rather than prove, the analytic theorem.
    checks=0
    for k in range(3,16):
        for gamma in (Q(-1,k),Q(0),Q(-1,2*k)):
            a,b,K=parameters(k,gamma)
            for n in (k+3,k+4,2*k+1):
                N=n*(n-1);h=target(n,K);t=Q(n*n-1,a*N+b)
                assert h<=-Q(2,N)
                for mu in representatives(k):
                    lam=tuple(sorted(mu+(1,)*(n-k),reverse=True))
                    residual=Q((-1)**(n-len(lam)),comb(n,len(lam)))-h-t*mixed_row(n,k,gamma,lam)
                    assert residual>=0,(k,gamma,n,mu,residual)
                    checks+=1
                if n%2==0:
                    eta=Q(1,n)+h
                    assert eta>=0
                    assert -Q(1,n)-h+eta==0
                    c=Q(2,N)-h-eta/Q(n-1)
                    assert c==Q((n+1)*(n-K),n*(N+K))>0
                # Re-transporting the same closed bound preserves kappa.
                assert parameters(n,h)[2]==K
    return checks

if __name__=='__main__':
    import argparse,json,pathlib
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed-dir',type=pathlib.Path)
    ap.add_argument('--output',type=pathlib.Path)
    args=ap.parse_args()
    seeds={12:Q(-1084543,25000000)}
    if args.seed_dir:
        for file in sorted(args.seed_dir.glob('dual_*.json')):
            dat=json.loads(file.read_text());k=int(dat['n'])
            if k>=12 and -Q(1,k)<=Q(dat['floor'])<=0:seeds[k]=Q(dat['floor'])
    result={'general_endpoint_checks':check_general_endpoints(),'certificates':[]}
    for k,gamma in sorted(seeds.items()):
        cert=certify_seed(k,gamma,k+1)
        result['certificates'].append(cert)
        print('k=',k,'gamma=',gamma,'kappa=',cert['kappa'],'=',cert['kappa_decimal'],'n>=',k+1,flush=True)
    if 16 in seeds and seeds[16]>=Q(-3,82):
        clean=certify_seed(16,Q(-3,82),17)
        result['clean_kappa6_certificate']=clean
        print('Clean kappa=6 certificate PASSED for all n>=17')
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',result['general_endpoint_checks'],'direct endpoint checks; exact all-dimensional certificates built')
