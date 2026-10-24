"""Independent contraction in INPUT-row order, using integer polynomial arithmetic.
No dependencies other than the Python standard library.
"""
from collections import defaultdict
from fractions import Fraction
from math import factorial
import json

# c[a,b,i,j] is the coefficient of X_ij in the (a,b) output cell.
def tensor(a=0,b=0):
 n=9; c=defaultdict(int)
 # Build B_6 from its definition, independently of the other programs.
 J=[[0]*6 for _ in range(6)]
 for i in range(3):J[i][i+3]=1;J[i+3][i]=-1
 for o in range(6):
  for p in range(6):
   for i in range(6):
    for j in range(6):
     c[o,p,i,j]+=int(o==p and i==j)-int(o==i and p==j)-J[o][j]*J[p][i]
 # A=|1><3| tensor I3; B=|3><1| tensor I3;
 # C=|2><3| tensor I3; D=|3><2| tensor I3.
 partials=[[(i,6+i)for i in range(3)],[(6+i,i)for i in range(3)],
           [(3+i,6+i)for i in range(3)],[(6+i,3+i)for i in range(3)]]
 for typ,blocks,coh in [(0,partials[:2],a),(1,partials[2:],b)]:
  for k,A in enumerate(blocks):
   for l,B in enumerate(blocks):
    fac=4*(1 if k==l else coh)
    for o,i in A:
     for p,j in B:
      ii,jj=(j,i)if typ else(i,j)
      c[o,p,ii,jj]+=fac
 return {k:v for k,v in c.items()if v}

def contraction_input(n,c):
 # Input row i is fixed in successive stages. Antisymmetrize output
 # rows, output columns, and input columns, in that order.
 stages=[[]for _ in range(n)]
 for (a,b,i,j),v in c.items(): stages[i].append((a,b,j,v))
 ans={((),(),()):1}
 for stage in stages:
  nxt=defaultdict(int)
  for (A,B,J),value in ans.items():
   for a,b,j,c in stage:
    if a in A or b in B or j in J:continue
    sign=(-1)**(sum(x>a for x in A)+sum(x>b for x in B)+sum(x>j for x in J))
    key=(tuple(sorted(A+(a,))),tuple(sorted(B+(b,))),tuple(sorted(J+(j,))))
    nxt[key]+=value*c*sign
  ans={k:v for k,v in nxt.items()if v}
 full=tuple(range(n));return ans.get((full,full,full),0)

def predicted(a,b):
 x,y=a*a,b*b
 return Fraction(-3,256)*(4+9*(x+y)+x*x+y*y+16*x*y+x*y*(x+y))

if __name__=='__main__':
 import time
 start=time.time();values={}
 for a,b in [(0,0),(1,0),(0,1),(1,1),(-1,1),(2,3),(-2,2)]:
  N=tensor(a,b)
  g=Fraction(contraction_input(9,N),8**9)
  assert g==predicted(a,b),(a,b,g,predicted(a,b))
  assert all(v==N.get((bb,aa,j,i),0)for(aa,bb,i,j),v in N.items())
  for i in range(9):
   for j in range(9):
    assert sum(N.get((a1,a1,i,j),0)for a1 in range(9))==8*int(i==j)
    assert sum(N.get((i,j,a1,a1),0)for a1 in range(9))==8*int(i==j)
  q=Fraction(sum(v*v for v in N.values()),64)
  assert q==Fraction(81,8)+Fraction(9,2)*(a*a+b*b)
  values[str((a,b))]={'Gamma':str(g),'Phi':str(g/factorial(9)),'q':str(q)}
  print(a,b,g,flush=True)
 # Identity and trace map normalization checks in low dimensions.
 for n in range(1,5):
  ident={(a,b,a,b):1 for a in range(n)for b in range(n)}
  trace={(a,a,i,i):1 for a in range(n)for i in range(n)}
  assert contraction_input(n,ident)==factorial(n)
  assert contraction_input(n,trace)==factorial(n)
 report={'status':'passed','seconds':time.time()-start,'independent_input_row_contractions':values,'scope':'Exact algebra. Positivity and the extremal parameter range are established analytically in the proof note.'}
 print(json.dumps(report,indent=2))
 from pathlib import Path
 Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
