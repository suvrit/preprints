from verify_input_order import tensor
from collections import defaultdict
import time, json
from fractions import Fraction
from math import factorial

def polynomial():
 N=tensor(0,0);n=9
 tags={k:(v,0,0)for k,v in N.items()}
 for i in range(3):
  for j in range(3):
   for key in [(i,6+j,6+i,j),(6+j,i,j,6+i)]:tags[key]=(4,1,0)
   for key in [(3+i,6+j,3+j,6+i),(6+j,3+i,6+i,3+j)]:tags[key]=(4,0,1)
 rows=[[]for _ in range(n)]
 for(a,b,i,j),(v,x,y)in tags.items(): rows[a].append((1<<b,1<<i,1<<j,b,i,j,v,x,y))
 D={(0,0,0,0,0):1};sizes=[]
 for a in range(n):
  E=defaultdict(int)
  for(B,I,J,x,y),v in D.items():
   for bb,ii,jj,b,i,j,c,xx,yy in rows[a]:
    if(B&bb)or(I&ii)or(J&jj):continue
    parity=((B>>(b+1)).bit_count()+(I>>(i+1)).bit_count()+(J>>(j+1)).bit_count())%2
    E[B|bb,I|ii,J|jj,x+xx,y+yy]+=(-1 if parity else 1)*v*c
  D={k:v for k,v in E.items()if v};sizes.append(len(D))
 full=(1<<n)-1
 return {(x,y):v for (B,I,J,x,y),v in D.items()if(B,I,J)==(full,full,full)},sizes

if __name__=='__main__':
 t=time.time();p,sz=polynomial()
 print('seconds',time.time()-t,'state sizes',sz)
 print('Gamma numerator polynomial:',p)
 norm={str((a,b)):str(Fraction(v,8**9))for(a,b),v in p.items()}
 print('Gamma normalized',norm)
 assert norm == {str((0,0)):'-3/64',str((0,2)):'-27/256',str((0,4)):'-3/256',str((2,0)):'-27/256',str((2,2)):'-3/16',str((2,4)):'-3/256',str((4,0)):'-3/256',str((4,2)):'-3/256'}
 print('Phi at1',Fraction(sum(p.values()),8**9*factorial(9)))
 with open('coherent_polynomial.json','w')as f:
  json.dump({'Gamma_coefficients':norm,'Phi_at_1':str(Fraction(sum(p.values()),8**9*factorial(9))),'integer_coefficients':{str(k):v for k,v in p.items()}},f,indent=2)
