"""Exact recursive low-dimensional constraints. Standard library only.

The raw inequality rows are monomial coefficients of
(D_k - gamma_k (d_1+...+d_k)^k) f. D_k is the radial determinant
operator. See PROOF.md for their applicability to ordinary positive maps.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import factorial, gcd, lcm, prod
from spectral_model import build_strengthened
from radial_exact import radial_fast, diagonal_derivative


def monomial_dimension(lam: tuple[int, ...], n: int) -> int:
    denominator = factorial(n-len(lam)) * prod(
        factorial(c) for c in Counter(lam).values())
    return factorial(n)//denominator


@lru_cache(None)
def splits(lam: tuple[int, ...], k: int, n: int):
    counts = Counter(lam)
    keys = sorted(counts, reverse=True)
    result = []
    for selected in product(*(range(counts[a]+1) for a in keys)):
        left = tuple(a for a,c in zip(keys,selected) for _ in range(c))
        right = tuple(a for a,c in zip(keys,selected)
                      for _ in range(counts[a]-c))
        if len(left)<=k and len(right)<=n-k:
            result.append((left,right))
    return tuple(result)


def mixed_rows(n, partitions, gammas):
    rows = {}
    for j, lam in enumerate(partitions):
        dimension = monomial_dimension(lam,n)
        for k, gamma in gammas.items():
            if k>=n:
                raise ValueError('Only previously certified dimensions k<n may be used')
            gamma = Q(gamma)
            if gamma>0:
                raise ValueError('The determinant-at-identity transfer requires gamma<=0')
            for mu,nu in splits(lam,k,n):
                values = radial_fast(mu,k).copy()
                if gamma:
                    for alpha,c in diagonal_derivative(mu,k).items():
                        values[alpha]=values.get(alpha,0)-gamma*c
                for alpha,c in values.items():
                    if not c:
                        continue
                    key = (k,alpha,nu)
                    if key not in rows:
                        rows[key]=[Q(0)]*len(partitions)
                    rows[key][j] += Q(c,dimension)
    return rows


def build(n, gammas):
    model = build_strengthened(n)
    for key, row in mixed_rows(n,model.partitions,gammas).items():
        if min(row)>=0:
            continue  # follows from the existing w>=0 constraints
        multiplier = lcm(*(v.denominator for v in row))
        integers = [int(v*multiplier) for v in row]
        scale = max(abs(v) for v in integers)
        row = [Q(v,scale) for v in integers]
        for existing in model.matrix:
            existing.append(Q(0))
        model.objective.append(Q(0))
        row += [Q(0)]*(len(model.objective)-len(row))
        row[-1] = Q(-1)  # nonnegative slack for row*w>=0
        model.matrix.append(row)
        model.rhs.append(Q(0))
        model.row_metadata.append(['mixed_small_rank',key])
    return model


def build_recursive(n, gammas):
    """Compatibility adapter for the original archived discovery/checker API."""
    model=build(n,gammas)
    return {"A":model.matrix,"b":model.rhs,"c":model.objective,"parts":model.partitions}
