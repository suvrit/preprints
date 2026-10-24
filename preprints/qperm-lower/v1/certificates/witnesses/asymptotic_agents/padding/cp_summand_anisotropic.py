from fractions import Fraction as F
from math import factorial,comb
import sys,json
sys.path.insert(0,'polarization_result')
from verify import contract,seed_raw
sys.path.insert(0,'asymptotic_agents/padding')
from check_extension import polynomial_values_to_coeff
R=seed_raw()
edges=[(0,6),(1,7),(5,0),(6,1),(7,2)]
Q={(a,b,i,j):4 for a,i in edges for b,j in edges}
def mixed(t):
 c=dict(Q)
 for key,v in R.items():c[key]=c.get(key,0)+t*v
 return c
vals=[F(2*contract(8,mixed(t)),8**8*factorial(8)) for t in range(9)]
c=polynomial_values_to_coeff(vals)
b=[sum(c[k]*comb(8-k,j-k)*(-1)**(j-k) for k in range(j+1)) for j in range(9)]
print('c coefficients Phi(Q+tH8):',[str(z) for z in c])
print('b coefficients Phi(Q+t(H8-Q)):',[str(z) for z in b])
obj={'c':[str(z) for z in c],'b':[str(z) for z in b]}
open('asymptotic_agents/padding/cp_summand_anisotropic.json','w').write(json.dumps(obj,indent=2))

def fall(n,j):
 return factorial(n)//factorial(n-j) if j<=n else 0

def bracket(m,alpha):
 return (alpha**5*fall(m,5)/4096+25*alpha**4*fall(m,4)/4096
         +41*alpha**3*fall(m,3)/1024+45*alpha**2*fall(m,2)/1024
         -51*alpha*m/512-F(33,512))

# With alpha=1/4, pull out the output congruence diag(D/sqrt8,I).
# The resulting raw extension has integer upper corner R, identity lower
# corner, and off-block coefficient K0. This permits an independent exact
# direct determinant contraction in dimensions 9,10,11.
for n in [9,10,11]:
 d=dict(R)
 for a in range(8,n):
  for b in range(8,n):d[a,b,a,b]=1
 for a,i in edges:
  for b in range(8,n):
   d[a,b,i,b]=1
   d[b,a,b,i]=1
 actual=F(2*contract(n,d),8**8*factorial(n))
 predicted=bracket(n-8,F(1,4))/fall(n,8)
 assert actual==predicted,(n,actual,predicted)

limiting=[F(1,4096),F(25,4096),F(41,1024),F(45,1024),F(-51,512),F(-33,512)]
u=F(3,5)
value=sum(a*u**(5-j) for j,a in enumerate(limiting))
assert value==F(-4947,50000)
for m in range(1,51):
 assert bracket(m,u/m)<=value
print('Three exact higher-dimensional contractions passed.')
print('Rational limiting certificate at u=3/5:',str(value))
