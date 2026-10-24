from collections import defaultdict
from fractions import Fraction
from math import factorial
import sys,time,json
from pathlib import Path
from verify_input_order import tensor

def contraction(n,c):
    rows=[[] for _ in range(n)]
    for (a,b,i,j),v in c.items(): rows[a].append((1<<b,1<<i,1<<j,b+1,i+1,j+1,v))
    d={(0,0,0):1}
    for stage in rows:
        e=defaultdict(int)
        for (B,I,J),v in d.items():
            for bb,ii,jj,b,i,j,w in stage:
                if (B&bb) or (I&ii) or (J&jj):continue
                sign=-1 if ((B>>b).bit_count()+(I>>i).bit_count()+(J>>j).bit_count())%2 else 1
                e[(B|bb,I|ii,J|jj)]+=sign*v*w
        d={k:v for k,v in e.items() if v}
    f=(1<<n)-1
    return d.get((f,f,f),0)

if __name__=='__main__':
    base=tensor(1,1);out={}
    for axis,cut in [('in',0),('in',3),('in',6),('out',0),('out',3),('out',6)]:
        ix=(2,3) if axis=='in' else (0,1)
        data={k:v for k,v in base.items() if ((k[ix[0]]==cut)==(k[ix[1]]==cut))}
        start=time.time()
        val=Fraction(contraction(9,data),8**9*factorial(9))
        b=Fraction(-1,737280)-val
        out[str((axis,cut))]={'pinched_phi':str(val),'curvature_beta':str(b),'seconds':time.time()-start}
        print(axis,cut,out[str((axis,cut))],flush=True)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
