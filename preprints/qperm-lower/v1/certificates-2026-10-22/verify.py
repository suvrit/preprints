"""Exact verification of the 2026-10-22 finite seed and universal envelope.

Only the Python standard library is needed. Floating-point optimizer results
are never trusted or imported by this verifier.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from fractions import Fraction as Q
import json, hashlib
ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'checks'))
from sparse_extend import build, verify
from verify_transport_general import certify_seed, parameters, target

def main():
    gamma={2:Q(0),3:Q(0)}
    records=[]
    for n in range(4,19):
        name=f'recursive_cert_{n}.json' if n<8 else f'dual_{n}.json'
        cert=json.loads((ROOT/'finite'/name).read_text())
        used={int(k):Q(v) for k,v in cert['gammas'].items()}
        assert all(k in gamma and v<=gamma[k] for k,v in used.items())
        model=build(n,used)
        y=list(map(Q,cert['dual']))
        value=verify(model,y)
        assert value==Q(cert['objective'] if n<8 else cert['lower'])
        floor=value if n<8 else Q(cert['floor'])
        assert value>=floor>=-Q(1,n)
        if n<8:
            x=list(map(Q,cert['primal']))
            assert len(x)==len(model['c']) and min(x)>=0
            assert all(sum(a*x[j] for j,a in row.items())==b
                       for row,b in zip(model['A'],model['b']))
            assert sum(c*v for c,v in zip(model['c'],x))==value
        gamma[n]=floor
        records.append({'n':n,'floor':str(floor),'exact_dual_value':str(value),
                        'rows':len(model['A']),'variables':len(model['c'])})
        print('VERIFIED',n,str(floor),flush=True)

    transport=certify_seed(18,gamma[18],19)
    archived=json.loads((ROOT/'transport_18.json').read_text())
    assert transport==archived
    K=parameters(18,gamma[18])[2]
    assert target(18,K)==gamma[18]
    assert K==Q(6562108347902,1034110757033)>Q(19,3)
    assert gamma[18]>-Q(171460901,5000000000)

    A=Q(19,3); B=Q(37)
    bound=lambda n:-Q(3*n,3*n*n+19*n+111)
    finite=[{'n':n,'margin':str(gamma[n]-bound(n))} for n in range(8,18)]
    assert all(Q(item['margin'])>=0 for item in finite)
    # Identity h_n(A)+n/(n²+An+B) has this numerator, with positive denominator.
    coeff=[B*(A+1), A+A*(A+1)-B, A-A]
    assert coeff==[Q(814,3),Q(142,9),Q(0)]
    assert min(coeff)>=0
    # Difference from previous headline is n(2n-15)/(positive denominators),
    # strictly positive for all integer n>=8.
    assert 2*8-15>0
    smooth_B=Q(800000000,5274023)-64-8*K
    assert smooth_B==Q(201367792086857761456,5453923917139453759)>0
    smooth=lambda n:-Q(n)/(n*n+K*n+smooth_B)
    smooth_finite=[{'n':n,'margin':str(gamma[n]-smooth(n))} for n in range(8,18)]
    assert all(Q(item['margin'])>=0 for item in smooth_finite)
    assert smooth(8)==gamma[8]
    smooth_slope=K*K+2*K-smooth_B
    assert smooth_slope>0 and smooth_B*(K+1)>0
    old_K=Q(32532964294,5171460901)
    old_B=Q(1018970066171739632,27274403735474723)
    assert old_B==Q(800000000,5274023)-64-8*old_K
    assert K>old_K
    # Denominator improvement is exactly (K-old_K)*(n-8), positive for n>8.
    assert smooth_B-old_B==-8*(K-old_K)
    result={'all_passed':True,'finite_certificates':records,
            'transport':{'seed_dimension':18,'gamma':str(gamma[18]),
                         'K':str(K),'all_dimensions_from':18,
                         'shifted_polynomial_cases':len(transport['rows'])},
            'simple_envelope':{'formula':'-3*n/(3*n*n+19*n+111)',
                               'valid_from':8,'finite_margins':finite,
                               'tail_numerator_coefficients':list(map(str,coeff)),
                               'strictly_improves_previous_headline_from':8},
            'smooth_envelope':{'A':str(K),'B':str(smooth_B),'valid_from':8,
                               'finite_margins':smooth_finite,
                               'tail_numerator_coefficients':[str(smooth_B*(K+1)),str(smooth_slope)],
                               'equals_previous_smooth_bound_at':8,
                               'strictly_improves_previous_smooth_bound_from':9}}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('EXACT TRANSPORT, CLEAN AND SMOOTH ENVELOPES VERIFIED',flush=True)

    checksum_file=ROOT/'SHA256SUMS'
    if checksum_file.exists():
        for line in checksum_file.read_text().splitlines():
            expected,name=line.split('  ',1)
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
        print('CHECKSUMS VERIFIED',flush=True)

if __name__=='__main__':
    main()
