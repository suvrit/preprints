from pinching_checks import contraction
from verify_input_order import tensor,contraction_input
from fractions import Fraction
from math import factorial
from itertools import combinations
from pathlib import Path
import json,time,sys

def compress(c,ins,outs):
    ii={x:i for i,x in enumerate(ins)};oo={x:i for i,x in enumerate(outs)}
    return {(oo[a],oo[b],ii[i],ii[j]):v for (a,b,i,j),v in c.items() if a in oo and b in oo and i in ii and j in ii}

if __name__=='__main__':
    c=tensor(1,1); results={}
    for k in [8,7,6,5,4]:
        t=time.time(); cnt=0; mn=0; pair=None; negs=[]
        subs=list(combinations(range(9),k))
        for ins in subs:
            for outs in subs:
                cc=compress(c,ins,outs)
                gamma=contraction(k,cc)
                if gamma<0:
                    cnt+=1
                    if gamma<mn:mn=gamma;pair=(ins,outs)
                    negs.append((ins,outs,gamma))
        if pair:
            assert contraction_input(k,compress(c,*pair))==mn
        results[str(k)]={'negative_count':cnt,'minimum_raw_gamma':mn,'minimum_Phi':str(Fraction(mn,8**k*factorial(k))),'pair':pair,'seconds':time.time()-t,'negative_compressions':negs}
        print(k,{a:v for a,v in results[str(k)].items() if a!='negative_compressions'},flush=True)
        Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2)+'\n')
