#!/usr/bin/env python3
"""Directed certificate for Lambda in PF_10
(Appendix F.2--F.3 of "On some positivity properties of the Riemann Xi function").

Eleven verified real zeros supply Laplace factors. The residual is used
only through E Y^2 <= 2 b and E cosh(100000 Y)-1 <= 1/2. Every bounded
interval is covered by closed rational boxes; the tail is monotone.
This program does not independently reverify the published height 3e12.
"""
from fractions import Fraction
from itertools import combinations
from math import comb, factorial
from mpmath import iv
from sympy import bernoulli

iv.dps = 70
Q = iv.mpf
ORDER = 10
SCALE = 100
NOISE_RATE = 100000
KAPPA = Q(1)/2
RADIUS = Q('1e-40')
CENTERS = (
    '14.13472514173469379045725198356247027078425711569924318',
    '21.02203963877155499262847959389690277733434052490278175',
    '32.93506158773918969066236896407490348881271560351703901',
    '48.00515088116715972794247274942751604168684400114442512',
    '72.06715767448190758252210796982616839048090662145669709',
    '107.1686111842764075151233519630861912134767078814047653',
    '161.1889641375960275194373441293695543649157903274754666',
    '241.0491577962165864128379214103356705496456828447220938',
    '361.2893616958046503902913112277152281908759416379958332',
    '544.3238901010052629031213087557608362045030422788811585',
    '814.8705396258725677840196869567854134266570546908545228',
)
U = Q('3e12')
B = 16/U**2 + 2*(iv.log(U)+1)/U


def require(name, condition):
    if condition is not True:
        raise AssertionError('Failed or inconclusive certificate: '+name)
    print('PASS: '+name, flush=True)


def xi_enclosure(t):
    """Euler--Maclaurin, N=1000,p=64, explicit remainder disc."""
    s = iv.mpc(Q(1)/2, t)
    N, p = 1000, 64
    z = sum(Q(n)**(-s) for n in range(1, N))
    z += Q(N)**(1-s)/(s-1)+Q(N)**(-s)/2
    rising = [iv.mpc(1)]
    for j in range(2*p):
        rising.append(rising[-1]*(s+j))
    for k in range(1, p+1):
        bern = bernoulli(2*k)
        z += (Q(int(bern.p))/(int(bern.q)*factorial(2*k))
              * rising[2*k-1]*Q(N)**(-s-2*k+1))
    remainder = 4*abs(rising[2*p])/(
        (2*iv.pi)**(2*p)*(Q(1)/2+2*p-1)*Q(N)**(Q(1)/2+2*p-1))
    error = Q([-remainder.b, remainder.b])
    z += iv.mpc(error, error)
    return (s*(s-1)*iv.pi**(-s/2)*iv.gamma(s/2)*z/2).real


def rational(q):
    return Q(q.numerator)/q.denominator


def symmetric(e):
    return Q([-e.b, e.b])


class LaplaceCertificate:
    def __init__(self):
        endpoints = [(Q(c)-RADIUS, Q(c)+RADIUS) for c in CENTERS]
        self.a = [Q([lo.a, hi.b]) for lo, hi in endpoints]
        self.r = [a/SCALE for a in self.a]
        self.c = [iv.fprod(a*a for a in self.a)/(
            2*a*iv.fprod(b*b-a*a for j, b in enumerate(self.a) if j != i))
            for i, a in enumerate(self.a)]
        self.C = [sum(abs(c)*r**j for r, c in zip(self.r, self.c))
                  for j in range(2*ORDER+1)]
        self.M = [1+Q([0, (a*a*KAPPA/NOISE_RATE**2).b]) for a in self.a]
        self.reference, self.error = {}, {}

    def central_box_is_positive(self, lo, hi):
        mid, half = rational((lo+hi)/2), rational((hi-lo)/2)
        left = rational(lo)
        values_mid = [sum(c*(-r)**j*iv.exp(-a*mid)
                          for a, r, c in zip(self.a, self.r, self.c))
                      for j in range(2*ORDER)]
        values = []
        for j in range(2*ORDER-1):
            second_bound = sum(abs(c)*r**(j+2)*iv.exp(-a*left)
                               for a, r, c in zip(self.a, self.r, self.c))
            remainder = half**2*SCALE**2*second_bound/2
            noise = B*SCALE**2*self.C[j+2]
            values.append(values_mid[j]+symmetric(half)*SCALE*values_mid[j+1]
                          + symmetric(remainder+noise))
        A = [[values[i+j] for j in range(ORDER)] for i in range(ORDER)]
        for i in range(ORDER):
            if not (-1)**i*A[i][i] > 0:
                return False
            for j in range(i+1, ORDER):
                multiplier = A[j][i]/A[i][i]
                for k in range(i+1, ORDER):
                    A[j][k] -= multiplier*A[i][k]
        return True

    def prepare_structured_bounds(self):
        for k in range(2, ORDER+1):
            first = tuple(range(k))
            lead = (-1)**(k*(k-1)//2)*iv.fprod(self.c[i] for i in first)
            lead *= iv.fprod((self.r[j]-self.r[i])**2
                             for i, j in combinations(first, 2))
            total = sum(self.a[i] for i in first)
            require(f'order {k}: leading coefficient positive', lead > 0)
            self.reference[k] = []
            later_positive = True
            for indices in combinations(range(len(self.a)), k):
                weight = (-1)**(k*(k-1)//2)*iv.fprod(self.c[i] for i in indices)
                weight *= iv.fprod((self.r[j]-self.r[i])**2
                                   for i, j in combinations(indices, 2))
                exponent = (Q(0) if indices == first else
                            sum(self.a[i] for i in indices)-total)
                if indices != first:
                    later_positive &= exponent > 0
                require_sign = weight > 0 or weight < 0
                if not require_sign:
                    raise AssertionError('Undecided coefficient sign')
                coefficient = weight/lead*iv.fprod(self.M[i] for i in indices)
                self.reference[k].append((coefficient, exponent))
            require(f'order {k}: later reference exponents positive', later_positive)
            # Entrywise Leibniz bounds suffice at this much larger noise
            # rate. The r_max factor accounts for every row/column power.
            common = (factorial(k)*self.C[0]**k
                      * self.r[-1]**(k*(k-1))/lead)
            self.error[k] = []
            positive = True
            for ell in range(1, k+1):
                exponent = ell*NOISE_RATE+(k-ell)*self.a[0]-total
                positive &= exponent > 0
                coefficient = common*comb(k, ell)*self.M[-1]**(k-ell)*(4*KAPPA)**ell
                self.error[k].append((coefficient, exponent, ell))
            require(f'order {k}: every error exponent positive', positive)

    def relative_error_at(self, k, x):
        denominator = 1-iv.exp(-NOISE_RATE*x)
        return sum(coefficient*iv.exp(-exponent*x)/denominator**(2*ell)
                   for coefficient, exponent, ell in self.error[k])

    def reference_box(self, k, lo, hi):
        mid, half = rational((lo+hi)/2), rational((hi-lo)/2)
        left = rational(lo)
        value = sum(c*iv.exp(-e*mid) for c, e in self.reference[k])
        derivative = -sum(c*e*iv.exp(-e*mid) for c, e in self.reference[k])
        second = sum(abs(c)*e**2*iv.exp(-e*left) for c, e in self.reference[k])
        return value+symmetric(half)*derivative+symmetric(half**2*second/2)

    def structured_box_is_positive(self, lo, hi):
        return all(self.reference_box(k, lo, hi) > self.relative_error_at(k, rational(lo))
                   for k in range(2, ORDER+1))

    def cover(self, lo, hi, mode):
        test = (self.central_box_is_positive if mode == 'central'
                else self.structured_box_is_positive)
        pending = [(lo, hi, 0)]
        accepted, maximum_depth = 0, 0
        while pending:
            left, right, depth = pending.pop()
            if test(left, right):
                accepted += 1
                maximum_depth = max(maximum_depth, depth)
                continue
            if depth >= 25:
                raise AssertionError(('Uncertified interval', mode, left, right))
            middle = (left+right)/2
            pending.extend([(left, middle, depth+1), (middle, right, depth+1)])
        print(f'PASS: {mode} interval [{lo}, {hi}]: {accepted} closed dyadic boxes, '
              f'maximum depth {maximum_depth}', flush=True)

    def unbounded_tail(self):
        x = Q(1)/10
        for k in range(2, ORDER+1):
            negative = sum(abs(c)*iv.exp(-e*x) for c, e in self.reference[k][1:] if c < 0)
            margin = 1-negative
            require(f'order {k}: tail reference margin exceeds 0.18', margin > Q('.18'))
            relative = self.relative_error_at(k, x)/margin
            require(f'order {k}: tail error below 1e-1000 of margin', relative < Q('1e-1000'))
            print(f'  reference tail margin: {margin}\n  relative tail error: {relative}', flush=True)


def main():
    for center in CENTERS:
        lo, hi = Q(center)-RADIUS, Q(center)+RADIUS
        left, right = xi_enclosure(lo), xi_enclosure(hi)
        print(f'Xi endpoints at {center} +/- 1e-40: {left}; {right}', flush=True)
        require('real zero in this box', left*right < 0)
    require('moment parameter below half the retained anchor rate',
            NOISE_RATE**2 <= U**2/32)
    require('moment parameter below half the tail rates',
            NOISE_RATE**2+Q(1)/4 <= U**2/2)
    require('residual exponential moment below 1/2', iv.exp(2*NOISE_RATE**2*B)-1 < KAPPA)
    print(f'  residual mean upper bound: {B}', flush=True)
    certificate = LaplaceCertificate()
    require('eleven factors supply the twenty derivatives', len(CENTERS) == ORDER+1)
    require('rate boxes are positive, disjoint, and increasing',
            certificate.a[0] > 0 and all(certificate.a[i] < certificate.a[i+1]
                                        for i in range(len(CENTERS)-1)))
    require('all rates below the noise rate', certificate.a[-1] < NOISE_RATE)
    certificate.cover(Fraction(0), Fraction(1, 250), 'central')
    certificate.prepare_structured_bounds()
    certificate.cover(Fraction(1, 250), Fraction(1, 10), 'structured')
    certificate.unbounded_tail()
    print('ALL LAMBDA PF_10 CERTIFICATES PASSED', flush=True)


if __name__ == '__main__':
    main()
