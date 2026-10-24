"""Exact coefficientwise dual certificate for the bounded-row step 21 -> 24.

The finite rank12 spectral hull determines a rational separator. Every hull
vertex and orbital partition is checked using Fraction arithmetic. No
asymptotic separator theorem or residual interpolation is needed.
"""
from fractions import Fraction as Q
from math import comb
from spectral_model import partitions, vertices
from verify_transport_general import parameters, target, mixed_row, rank_two_row


def orbital_probabilities(lam,n,a):
    dp={(0,0):1}
    for x in lam+(0,)*(n-len(lam)):
        new=dp.copy()
        for (r,s),value in dp.items():
            if r<a:new[r+1,s+x]=new.get((r+1,s+x),0)+value
        dp=new
    dist={s:Q(value,comb(n,a)) for (r,s),value in dp.items() if r==a}
    assert sum(dist.values())==1
    return (sum(value for s,value in dist.items() if s==a),
            sum(value for s,value in dist.items() if abs(s-a)==1),
            sum(value for s,value in dist.items() if abs(s-a)>=2))


def certify(gamma21):
    n,k,a=24,21,12
    N=n*(n-1);K=parameters(k,gamma21)[2];h=target(n,K)
    t=Q(n*n-1,(1-gamma21)*(N+K));eta=Q(1,n)+h
    assert t>0 and eta>0
    v=Q(a*(n-a),N);Delta=Q(a*(n-a),N+K)-Q(1,4)
    a0=Q(4*n,n+1)*v
    assert Delta>0
    # psi(center)=1, psi(center+-1)=-1, psi(other)=C.
    # Minimize C subject to all rank12 hull-generator expectations >=0.
    spectral=[];C=Q(0);active=[]
    for vtx in vertices(n,a):
        u,b,p=vtx.ones,vtx.fractional_count,vtx.fractional_value
        if b==0:triple=(Q(1),Q(0),Q(0))
        else:
            probs={s:comb(b,s)*p**s*(1-p)**(b-s) for s in range(b+1)}
            triple=(sum(value for s,value in probs.items() if u+s==a),
                    sum(value for s,value in probs.items() if abs(u+s-a)==1),
                    sum(value for s,value in probs.items() if abs(u+s-a)>=2))
        center,near,tail=triple
        if tail:C=max(C,(near-center)/tail)
        else:assert center>=near
        spectral.append((u,b,p,triple))
    assert C==Q(49038552465408,22017942472189)
    for u,b,p,(center,near,tail) in spectral:
        value=center-near+C*tail
        assert value>=0
        if value==0:active.append([u,b,str(p)])
    leading={(1,)*n,(2,)+(1,)*(n-2)}
    data={}
    for lam in partitions(n):
        r=Q((-1)**(n-len(lam)),comb(n,len(lam)))
        J=mixed_row(n,k,gamma21,lam);R=rank_two_row(n,lam)
        c=r-h-t*J-eta*R
        if lam in leading or lam==(n,):assert c==0
        else:assert c>0
        ce,ne,ta=orbital_probabilities(lam,n,a)
        b=ce-ne+C*ta
        q=b-1+a0*(1-r)
        if lam in leading:assert q==0
        data[lam]=(r,J,R,c,b,q)
    qstar=data[(n,)][5]
    assert qstar>0
    ratios=[((q+qstar*R)/c,lam) for lam,(r,J,R,c,b,q) in data.items() if c]
    M,shape=max(ratios)
    assert M>0 and shape==(6,)+(1,)*18
    assert M==Q(35977984552366996045762853848991272,327848126478907158293371233405225)
    epsilon=4*Delta/(a0+M);exact_gamma=h+epsilon
    assert exact_gamma==Q(-9167110563519855245922921656813,315707850865223035909120949619832)
    Kstar=parameters(n,exact_gamma)[2]
    rounded_K=Q(271,40);gamma=target(n,rounded_K)
    assert gamma==Q(-649,22351)<=exact_gamma<0
    assert Kstar==Q(19139439468149302001394165971264,2824999664597764270913424967623)>rounded_K
    for lam,(r,J,R,c,b,q) in data.items():
        slack=M*c-q-qstar*R
        assert slack>=0,(lam,slack)
        # Explicit exact dual identity. B,J,R are valid nonnegative rows.
        assert (a0+M)*(r-exact_gamma)==b+M*t*J+(M*eta+qstar)*R+slack
    assert M*t>0 and M*eta+qstar>0
    return {'n':n,'source_dimension':k,'source_gamma':str(gamma21),
            'source_K':str(K),'separator_C':str(C),'projection_rank':a,
            'spectral_vertex_checks':len(spectral),'separator_active_vertices':active,
            'orbital_coefficient_checks':len(data),'maximum_ratio':str(M),
            'maximum_ratio_shape':list(shape),'a0':str(a0),'qstar':str(qstar),
            'epsilon':str(epsilon),'exact_gamma':str(exact_gamma),'exact_K':str(Kstar),
            'gamma':str(gamma),'K':str(rounded_K),
            'rounding_margin':str(exact_gamma-gamma),
            'row_multipliers':{'bounded_spectral':str(1/(a0+M)),
                               'selected_mixed':str(M*t/(a0+M)),
                               'rank_two':str((M*eta+qstar)/(a0+M))}}
