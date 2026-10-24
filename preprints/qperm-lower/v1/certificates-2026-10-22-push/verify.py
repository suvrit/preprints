"""Standalone exact verification of finite seeds, the analytic24 step and tails.

Only Python's standard library is used. No numerical optimizer is imported.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
import json, hashlib, argparse
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'checks'))
from sparse_extend import build, verify
from verify_transport_general import certify_seed, parameters, target
from analytic_seed24 import certify as certify24


def finish(gamma):
    transports=[]
    for k in (18,19,20,21):
        cert=certify_seed(k,gamma[k],k+1)
        transports.append({'seed_dimension':k,'gamma':str(gamma[k]),
                           'K':str(parameters(k,gamma[k])[2]),
                           'valid_from':k,'polynomial_cases':len(cert['rows'])})
    analytic=certify24(gamma[21])
    assert analytic==json.loads((ROOT/'analytic24.json').read_text())
    gamma24=Q(analytic['gamma']); K24=Q(analytic['K'])
    cert=certify_seed(24,gamma24,25)
    transports.append({'seed_dimension':24,'gamma':str(gamma24),'K':str(K24),
                       'valid_from':24,'polynomial_cases':len(cert['rows'])})
    rounded=certify_seed(24,target(24,Q(20,3)),25)
    assert Q(analytic['gamma'])>=target(24,Q(20,3))
    K21=parameters(21,gamma[21])[2]
    known=lambda n: gamma[n] if n<=21 else (target(n,K21) if n<24 else target(n,K24))
    simple=lambda n:-Q(3*n,3*n*n+20*n+103)
    finite=[{'n':n,'margin':str(known(n)-simple(n))} for n in range(8,27)]
    assert all(Q(row['margin'])>=0 for row in finite)
    A=Q(20,3); B=Q(103,3)
    simple_coeff=[B*(A+1), A*A+2*A-B]
    assert simple_coeff==[Q(2369,9),Q(211,9)] and min(simple_coeff)>0
    # h_n(A) - (-n/(n²+An+B)) has numerator c0+c1*n.
    # New simple denominator minus prior simple denominator is n-8.
    assert (3*8*8+20*8+103)==(3*8*8+19*8+111)
    smooth_B=-Q(8)/gamma[8]-64-8*K24
    assert smooth_B>0
    smooth=lambda n:-Q(n)/(n*n+K24*n+smooth_B)
    smooth_finite=[{'n':n,'margin':str(known(n)-smooth(n))} for n in range(8,25)]
    assert all(Q(row['margin'])>=0 for row in smooth_finite)
    assert smooth(8)==gamma[8]
    smooth_coeff=[smooth_B*(K24+1),K24*K24+2*K24-smooth_B]
    assert min(smooth_coeff)>0
    old_K=Q(6562108347902,1034110757033)
    old_gamma8=-Q(5274023,100000000)
    # Difference of smooth denominators is positive at8 and increases withn.
    denom_difference_at8=-Q(8)/gamma[8]+Q(8)/old_gamma8
    assert denom_difference_at8>0 and K24>old_K
    return {'transport_certificates':transports,'analytic_seed24':analytic,
            'simple_envelope':{'formula':'-3*n/(3*n*n+20*n+103)',
                               'valid_from':8,'finite_margins':finite,
                               'tail_numerator_coefficients':list(map(str,simple_coeff)),
                               'rounded_K':str(A),'rounded_transport_cases':len(rounded['rows']),
                               'equals_previous_simple_at':8,'strictly_improves_previous_simple_from':9},
            'smooth_envelope':{'A':str(K24),'B':str(smooth_B),'valid_from':8,
                               'finite_margins':smooth_finite,
                               'tail_numerator_coefficients':list(map(str,smooth_coeff)),
                               'strictly_improves_prior_release_smooth_from':8}}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tails-only',action='store_true',help='check transport/envelope arithmetic only; does not verify LP dependencies')
    args=ap.parse_args()
    gamma={2:Q(0),3:Q(0)}; records=[]
    for n in range(4,22):
        name=f'recursive_cert_{n}.json' if n<8 else f'dual_{n}.json'
        cert=json.loads((ROOT/'finite'/name).read_text())
        used={int(k):Q(v) for k,v in cert['gammas'].items()}
        assert set(used)==set(range(2,n))
        assert all(v<=gamma[k]<=0 for k,v in used.items())
        value=Q(cert['objective'] if n<8 else cert['lower'])
        floor=value if n<8 else Q(cert['floor'])
        assert value>=floor>=-Q(1,n)
        if not args.tails_only:
            model=build(n,used)
            assert verify(model,list(map(Q,cert['dual'])))==value
            if n<8:
                x=list(map(Q,cert['primal']))
                assert len(x)==len(model['c']) and min(x)>=0
                assert all(sum(a*x[j] for j,a in row.items())==b for row,b in zip(model['A'],model['b']))
                assert sum(c*v for c,v in zip(model['c'],x))==value
            records.append({'n':n,'floor':str(floor),'exact_dual_value':str(value),
                            'rows':len(model['A']),'variables':len(model['c'])})
            print('VERIFIED',n,str(floor),flush=True)
        gamma[n]=floor
    result=finish(gamma)
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    if args.tails_only:
        result['status']='PASS: tail arithmetic only; LP certificates were not reverified'
        print(json.dumps(result,indent=2))
    else:
        result.update({'all_passed':True,'finite_certificates':records})
        (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
        print('EXACT DEPENDENCY CHAIN, ANALYTIC24 SEED, TRANSPORT, ENVELOPES AND CHECKSUMS VERIFIED',flush=True)


if __name__=='__main__':main()
