"""Exact checks for the asymptotic and polarization note. Standard library only."""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial, prod
import json
from pathlib import Path


def contract(n, c, input_order=False):
    rows = [[] for _ in range(n)]
    for (a,b,i,j),v in c.items():
        if v:
            rows[i if input_order else a].append((a,b,j,v) if input_order else (b,i,j,v))
    states = {(0,0,0): 1}
    for row in rows:
        nxt = defaultdict(F)
        for masks,v in states.items():
            for i,j,k,w in row:
                indices = (i,j,k)
                if any(mask >> index & 1 for mask,index in zip(masks,indices)):
                    continue
                parity = sum((mask >> (index+1)).bit_count() for mask,index in zip(masks,indices)) % 2
                key = tuple(mask | (1 << index) for mask,index in zip(masks,indices))
                nxt[key] += (-1 if parity else 1)*v*w
        states = {key:v for key,v in nxt.items() if v}
    return states.get(((1<<n)-1,)*3, F(0))


def seed_raw():
    J = [[0]*6 for _ in range(6)]
    for i in range(3):
        J[i][i+3] = 1
        J[i+3][i] = -1
    c = defaultdict(int)
    for a in range(5):
        for b in range(5):
            for i in range(6):
                for j in range(6):
                    c[a,b,i,j] += int(a==b and i==j)-int(a==i and b==j)-J[a][j]*J[b][i]
    cp = [(0,6),(1,7),(5,0),(6,1),(7,2)]
    co = [(3,6),(4,7),(5,3),(6,4),(7,5)]
    for edges,trans in [(cp,False),(co,True)]:
        for a,i in edges:
            for b,j in edges:
                c[a,b,j if trans else i,i if trans else j] += 4
    return {key:v for key,v in c.items() if v}


def simple_map(n,a,b):
    # a Id + b transpose + (1-a-b) Delta; parameters are nonnegative.
    c = {}
    for r in range(n):
        for s in range(n):
            for i in range(n):
                for j in range(n):
                    v=a*(r==i and s==j)+b*(r==j and s==i)+(1-a-b)*F(1,n)*(r==s and i==j)
                    if v:
                        c[r,s,i,j]=v
    return c


def direct_sum(c,r,d,s):
    out=dict(c)
    out.update({tuple(x+r for x in key):v for key,v in d.items()})
    return out


def radius_F(n,r):
    return sum(r**k*((1-r)/n)**(n-k) for k in range(n+1))


def lower_q_radius(n,r,q):
    return (F(2,n**n)+F(n+1,2*n**(n-1))*r*r
            +F(q-1,2*(n-1)*n**(n-1))-radius_F(n,r))


def main():
    c=seed_raw()
    d2=[1,1,2,1,1,1,1,1]
    for a in range(8):
        for b in range(8):
            assert sum(c.get((a,b,i,i),0) for i in range(8)) == (8//d2[a] if a==b else 0)
    for i in range(8):
        for j in range(8):
            assert sum(d2[a]*c.get((a,a,i,j),0) for a in range(8)) == 8*(i==j)
    raw=contract(8,c)
    assert raw == contract(8,c,True) == -540672
    phi8=F(raw*prod(d2),8**8*factorial(8))
    assert phi8 == F(-11,6881280)

    block_tests=0
    for r,s in [(1,1),(1,2),(2,2),(2,3),(3,3)]:
        c=simple_map(r,F(1,3),F(1,6))
        d=simple_map(s,F(1,2),F(1,4))
        actual=contract(r+s,direct_sum(c,r,d,s))/factorial(r+s)
        predicted=contract(r,c)*contract(s,d)/factorial(r+s)
        assert actual == predicted
        block_tests += 1

    radius_tests=0
    for n in range(2,5):
        for a,b in [(F(0),F(0)),(F(1,10),F(1,10)),(F(1,3),F(1,6)),(F(1,2),F(1,2)),(F(1),F(0)),(F(0),F(1))]:
            c=simple_map(n,a,b)
            phi=contract(n,c)/factorial(n)
            q=sum(v*v for v in c.values())
            rho=a+b
            assert abs(phi) <= radius_F(n,rho)
            assert phi >= lower_q_radius(n,rho,q)
            if n==2:
                assert phi == lower_q_radius(n,rho,q)
            if b==0:
                assert phi == radius_F(n,rho)
            radius_tests+=1
    # Independent exact expansion of the scalar/traceless Fischer norm polynomial.
    for n in range(2,41):
        a=[sum(F((-1)**(j-k)*comb(n-k,j-k),n**(n-k)) for k in range(j+1)) for j in range(n+1)]
        assert a[0]==F(1,n**n) and a[1]==0 and a[2]==F(n+1,2*n**(n-1))
        assert all(v>=0 for v in a)

    magn=-phi8
    first=next(n for n in range(8,60) if magn/comb(n,8)>F(factorial(n),n**n))
    assert first==33
    assert magn*factorial(8)==F(33,512)
    # Monotonicity after 33 is proved in the note, not inferred from this table.
    table=[]
    for n in [8,17,20,30,32,33,40,50,100]:
        padded=phi8/comb(n,8)
        target=-F(factorial(n),n**n)
        table.append({'n':n,'padded_exact':str(padded),'padded_decimal':float(padded),
                      'factorial_exact':str(target),'factorial_decimal':float(target)})
    result={'status':'passed','raw_Gamma8':str(raw),'Phi8':str(phi8),
            'block_factorization_checks':block_tests,'radius_checks':radius_tests,
            'Fischer_coefficient_checks':'n=2,...,40','first_factorial_failure':first,
            'comparison':table}
    Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='comparison'},indent=2))


if __name__=='__main__':
    main()
