from fractions import Fraction as Q
from itertools import permutations,product
from math import factorial,comb,prod
from functools import lru_cache

@lru_cache(None)
def monomials(mu,k):
 return tuple(sorted(set(permutations(mu+(0,)*(k-len(mu))))))
def parity(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
@lru_cache(None)
def vandermonde(k):
 # determinant x_i^(k-1-j)
 return tuple((tuple(k-1-j for j in p),parity(p)) for p in permutations(range(k)))

def sparseadd(d,m,v):
 if not v:return
 v+=d.get(m,0)
 if v:d[m]=v
 elif m in d:del d[m]

@lru_cache(None)
def radial_fast(mu,k):
 if sum(mu)<k:return {}
 delta=dict(vandermonde(k));out={}
 for aa in monomials(mu,k):
  for bb,s in delta.items():
   cc=tuple(a+b for a,b in zip(aa,bb));val=prod(cc)
   if val:sparseadd(out,tuple(x-1 for x in cc),s*val)
 # divide by monic Vandermonde in lex order
 lead=tuple(range(k-1,-1,-1));q={}
 while out:
  mm=max(out);c=out[mm]
  qq=tuple(a-b for a,b in zip(mm,lead));assert min(qq)>=0,(mu,k,mm,lead)
  sparseadd(q,qq,c)
  for bb,s in delta.items():sparseadd(out,tuple(a+b for a,b in zip(qq,bb)),-c*s)
 ans={}
 for aa,c in q.items():
  la=tuple(sorted((x for x in aa if x),reverse=True))
  if la in ans:assert ans[la]==c
  ans[la]=c
 return ans

@lru_cache(None)
def diagonal_derivative(mu,k):
 # (d/dx1+...+d/dxk)^k m_mu
 if sum(mu)<k:return {}
 out={}
 for aa in monomials(mu,k):
  for bb in product(*[range(a+1) for a in aa]):
   if sum(bb)!=sum(mu)-k:continue
   c=factorial(k)*prod(comb(a,b) for a,b in zip(aa,bb))
   sparseadd(out,bb,c)
 ans={}
 for aa,c in out.items():
  la=tuple(sorted((x for x in aa if x),reverse=True))
  if la in ans:assert ans[la]==c
  ans[la]=c
 return ans
