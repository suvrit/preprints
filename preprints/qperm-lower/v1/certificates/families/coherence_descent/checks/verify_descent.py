"""Exact algebraic checks for coherence descent. No numerical positivity sampling."""
from fractions import Fraction
from math import factorial
from random import Random
from pathlib import Path
import json
from pinching_checks import contraction
from compression_scan import compress
from verify_input_order import tensor,contraction_input

rng=Random(20261008)
report={}

def phi(n,c):return Fraction(contraction(n,c),factorial(n))
def scale_cut(c,cut,t,axis='in'):
    p,q=(2,3)if axis=='in'else(0,1)
    return {k:v*(t if ((k[p]in cut)!=(k[q]in cut)) else 1)for k,v in c.items() if v and (t or ((k[p]in cut)==(k[q]in cut)))}

# Polynomial identity is valid even for tensors not representing positive maps.
for n in [2,3,4]:
    c={}
    for a in range(n):
      for b in range(n):
       for i in range(n):
        for j in range(n):
         key=(a,b,i,j);mate=(b,a,j,i)
         if key not in c:c[key]=c[mate]=rng.randint(-2,2)
    c={k:v for k,v in c.items()if v}
    f=phi(n,c)
    for axis in ['in','out']:
     for cut in [{0},{n-1}]:
      aa=phi(n,scale_cut(c,cut,0,axis));bb=f-aa
      for t in [-2,-1,0,1,2,3]:
       assert phi(n,scale_cut(c,cut,t,axis))==aa+bb*t*t
    if n==4:
     cut={0,1};v=[phi(n,scale_cut(c,cut,t))for t in [0,1,2]]
     aa=v[0];cc=(v[2]-4*v[1]+3*aa)/12;bb=v[1]-aa-cc
     for t in [-3,-2,-1,0,1,2,3]:assert phi(n,scale_cut(c,cut,t))==aa+bb*t*t+cc*t**4
    report[f'dense_rank_{n}']='input/output quadratic identities passed; all entries integral'

# Basic valid controls.
for n in range(2,5):
    ident={(a,b,a,b):1 for a in range(n)for b in range(n)}
    assert phi(n,ident)==1
    assert phi(n,scale_cut(ident,{0},0))==Fraction(1,n)
    trace={(a,a,i,i):1 for a in range(n)for i in range(n)}
    assert phi(n,trace)==1
    assert scale_cut(trace,{0},2)==trace

# Rank-eight family: exact second contraction and SOS identity for rational parameters.
ins=tuple(range(8));outs=(0,1,2,3,4,6,7,8)
weights=[1,1,2,1,1,1,1,1]
vals={}
for a,b in [(0,0),(1,0),(0,1),(1,1),(-1,1),(Fraction(3,4),0),(2,3)]:
    c=compress(tensor(a,b),ins,outs)
    g=Fraction(2,8**8)*contraction(8,c)
    assert g==Fraction(2,8**8)*contraction_input(8,c)
    pred=(8*a**4-9*a*a-21*b*b-34*a*a*b*b-10)/Fraction(1024)
    assert g==pred
    gap_num=(1-b*b)*(21+34*a*a)+27*(1-a*a)+8*(1-a*a)**2
    assert g+Fraction(33,512)==gap_num/Fraction(1024)
    q=Fraction(sum(weights[i]*weights[j]*v*v for(i,j,x,y),v in c.items()),64)
    assert q==Fraction(31,4)+3*(a*a+b*b)
    for i in range(8):
     for j in range(8):
      assert sum(weights[o]*c.get((o,o,i,j),0)for o in range(8))==8*int(i==j)
    vals[str((a,b))]={'Gamma8':str(g),'Phi8':str(g/factorial(8)),'q':str(q)}
report['rank8_family']=vals
report['independent_contraction_algorithms']='fixed output-row bitmask and fixed input-row tuple recurrences'
# Strict ordinary positivity with margin 1/800 and negative invariant.
c=compress(tensor(1,1),ins,outs)
strict={k:198*v for k,v in c.items()}
for o in range(8):
 for i in range(8):
  strict[o,o,i,i]=strict.get((o,o,i,i),0)+(1 if o==2 else 2)
strict={k:v for k,v in strict.items()if v}
g=contraction(8,strict)
assert g==contraction_input(8,strict)
strict_phi=Fraction(2*g,1600**8*factorial(8))
assert strict_phi==Fraction(-7271299899816808843,5872025600000000000000000)
report['strict_rank8']={'map':'(99/100)T_11+(1/100)Delta8','margin':'1/800','Phi':str(strict_phi),'raw_Gamma':g}
report['status']='passed' 
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
