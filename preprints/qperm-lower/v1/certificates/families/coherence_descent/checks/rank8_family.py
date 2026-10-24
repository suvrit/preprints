from compression_scan import compress
from verify_input_order import tensor
from collections import defaultdict
from fractions import Fraction
from math import factorial
from pathlib import Path
import json

ins=tuple(range(8));outs=(0,1,2,3,4,6,7,8)
c0=compress(tensor(0,0),ins,outs)
c1=compress(tensor(1,0),ins,outs)
c2=compress(tensor(0,1),ins,outs)
rows=[[]for _ in range(8)]
for key in set(c0)|set(c1)|set(c2):
 a,b,i,j=key
 for x,y,v in [(0,0,c0.get(key,0)),(1,0,c1.get(key,0)-c0.get(key,0)),(0,1,c2.get(key,0)-c0.get(key,0))]:
  if v:rows[a].append((1<<b,1<<i,1<<j,b+1,i+1,j+1,x,y,v))
d={(0,0,0,0,0):1}
for row in rows:
 e=defaultdict(int)
 for(B,I,J,x,y),v in d.items():
  for bb,ii,jj,b,i,j,u,w,z in row:
   if B&bb or I&ii or J&jj:continue
   s=-1 if ((B>>b).bit_count()+(I>>i).bit_count()+(J>>j).bit_count())%2 else 1
   e[B|bb,I|ii,J|jj,x+u,y+w]+=s*v*z
 d={k:v for k,v in e.items()if v}
pol={(x,y):v for(B,I,J,x,y),v in d.items()}
print('raw polynomial',pol)
print('Gamma balanced coeffs',{xy:Fraction(2*v,8**8)for xy,v in pol.items()})
print('Phi balanced coeffs',{xy:Fraction(2*v,8**8*factorial(8))for xy,v in pol.items()})
Path(__file__).with_suffix('.json').write_text(json.dumps({str(k):str(Fraction(2*v,8**8))for k,v in pol.items()},indent=2)+'\n')
