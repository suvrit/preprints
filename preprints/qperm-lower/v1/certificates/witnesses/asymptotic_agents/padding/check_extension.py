from fractions import Fraction as F
from math import factorial,comb
import sys
sys.path.insert(0,'polarization_result')
from verify import contract,simple_map

def coherent(c,r,n,q):
 d=dict(c)
 for a in range(n):
  for b in range(n):
   if a>=r or b>=r:
    d[a,b,a,b]=1 if a>=r and b>=r else q # q = cross multiplier; use rational squared below
 return d

def qj(c,r,j):
 import itertools
 if j==0:return 1
 z=F(0)
 for R in itertools.combinations(range(r),j):
  for C in itertools.combinations(range(r),j):
   d={(a,b,i,k):c.get((R[a],C[b],R[i],C[k]),0) for a in range(j) for b in range(j) for i in range(j) for k in range(j)}
   z+=contract(j,d)
 return z

def fall(n,k):return factorial(n)//factorial(n-k) if k<=n else 0

for r in [1,2,3]:
 c=simple_map(r,F(1,3),F(1,4))
 Q=[qj(c,r,j) for j in range(r+1)]
 for n in range(r+1,min(r+4,7)):
  s=n-r;q=F(1,3)
  actual=contract(n,coherent(c,r,n,q))/factorial(n)
  pred=F(factorial(s),factorial(n))*sum(fall(s,r-j)*q**(2*(r-j))*Q[j] for j in range(r+1))
  assert actual==pred,(r,n,actual,pred,Q)
print('coherent Qj formula passed 9 exact tests')

# Independently check the general fixed-corner coefficient formula with
# invertible and singular, non-scalar diagonal K.
def add_maps(a,b,t=F(1)):
 d=dict(a)
 for key,v in b.items():d[key]=d.get(key,F(0))+t*v
 return d

def ad_diagonal(diag):
 return {(a,b,a,b):x*y for a,x in enumerate(diag) for b,y in enumerate(diag) if x*y}

def polynomial_values_to_coeff(values):
 out=[F(0)]*len(values)
 basis=[F(1)]
 diff=list(values)
 for k in range(len(values)):
  for j,z in enumerate(basis):out[j]+=z*diff[0]/factorial(k)
  diff=[diff[i+1]-diff[i] for i in range(len(diff)-1)]
  new=[F(0)]*(len(basis)+1)
  for j,z in enumerate(basis):new[j]-=k*z;new[j+1]+=z
  basis=new
 return out

checks=0
for diag in [(F(1,2),F(2,3)),(F(0),F(3,4)),(F(0),F(1,3),F(2,3))]:
 r=len(diag)
 p=simple_map(r,F(1,5),F(1,3))
 base=ad_diagonal(diag)
 bj=polynomial_values_to_coeff([contract(r,add_maps(base,p,F(t)))/factorial(r) for t in range(r+1)])
 for n in [r+1,r+2]:
  actual=contract(n,add_maps(ad_diagonal(diag+(F(1),)*(n-r)),p))/factorial(n)
  predicted=sum(bj[j]*F(fall(r,j),fall(n,j)) for j in range(r+1))
  assert actual==predicted,(diag,n,actual,predicted)
  checks+=1
print('general coefficient formula passed',checks,'exact tests')
