from compression_scan import compress
from verify_input_order import tensor,contraction_input
from pinching_checks import contraction
from fractions import Fraction
from math import factorial
import json
from pathlib import Path

I=tuple(range(8));O=(0,1,2,3,4,6,7,8)
c=compress(tensor(1,1),I,O)
g=contraction(8,c)
assert g==contraction_input(8,c)==-540672
weights=[1,1,2,1,1,1,1,1]
# Exact output filter D=diag(1,1,sqrt(2),1,1,1,1,1).
# In diagonal contractions it acts by the integer squared weights.
for a in range(8):
 for b in range(8):
  val=sum(c.get((a,b,i,i),0)for i in range(8))
  assert (weights[a]*val if a==b else val)==8*int(a==b)
for i in range(8):
 for j in range(8):
  assert sum(weights[a]*c.get((a,a,i,j),0)for a in range(8))==8*int(i==j)
q=Fraction(sum(weights[a]*weights[b]*v*v for(a,b,i,j),v in c.items()),64)
Gamma=Fraction(2*g,8**8);Phi=Gamma/factorial(8)
assert Gamma==Fraction(-33,512)
assert Phi==Fraction(-11,6881280)
print('rank8',Gamma,Phi,float(Phi),'q=',q)
report={'input_indices_zero_based':I,'output_indices_zero_based':O,'output_filter_squared':weights,'raw_Gamma':g,'Gamma':str(Gamma),'Phi':str(Phi),'q':str(q),'marginals':'both exactly I8','proof_of_positivity':'CP input/output compression and congruence of analytically positive Hcoh','independent_contractions':'output-row bitmask DP and input-row tuple DP agree'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
