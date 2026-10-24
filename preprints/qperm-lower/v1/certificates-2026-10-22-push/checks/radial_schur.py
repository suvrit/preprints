"""Exact Schur/Pieri evaluation of radial determinant derivatives.

All proof calculations use integers or rational numbers.  The partition order
is decreasing lexicographic order, compatible with dominance.  H_mu is expanded
in Schur functions by Pieri; Hall duality gives the inverse-transpose transition
from monomials to Schur functions.  The radial determinant is diagonal followed
by removal of one full column.
"""
from functools import lru_cache
from collections import Counter
from math import comb, factorial, prod
from spectral_model import partitions

@lru_cache(None)
def horizontal_strips(mu, degree):
    out = []
    for lam in partitions(sum(mu) + degree):
        if len(lam) < len(mu) or len(lam) > len(mu) + 1:
            continue
        if any(not (lam[i] >= a >= (lam[i+1] if i+1 < len(lam) else 0))
               for i, a in enumerate(mu)):
            continue
        out.append(lam)
    return tuple(out)

@lru_cache(None)
def complete_to_schur(lam):
    f = {(): 1}
    for degree in lam:
        g = {}
        for mu, c in f.items():
            for nu in horizontal_strips(mu, degree):
                g[nu] = g.get(nu, 0) + c
        f = g
    return f

@lru_cache(None)
def transition(degree):
    ps = tuple(partitions(degree))
    idx = {p: i for i, p in enumerate(ps)}
    size = len(ps)
    K = [[complete_to_schur(lam).get(shape, 0) for shape in ps] for lam in ps]
    assert all(K[i][i] == 1 and not any(K[i][j] for j in range(i+1, size))
               for i in range(size))
    inverse = [[int(i == j) for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(i):
            inverse[i][j] = -sum(K[i][h] * inverse[h][j] for h in range(j, i))
    return ps, idx, tuple(map(tuple, K)), tuple(map(tuple, inverse))

@lru_cache(None)
def radial(mu, k):
    degree = sum(mu)
    if len(mu) > k or degree < k:
        return {}
    ps, idx, K, inverse = transition(degree)
    low, li, Kl, _ = transition(degree-k)
    i = idx[mu]
    out = {}
    for j, lam in enumerate(ps):
        if len(lam) != k or not inverse[j][i]:
            continue
        nu = tuple(a-1 for a in lam if a > 1)
        c = inverse[j][i] * prod(lam[a] + k-1-a for a in range(k))
        col = li[nu]
        for a, beta in enumerate(low):
            if len(beta) > k:
                continue
            value = c * Kl[a][col]
            if value:
                out[beta] = out.get(beta, 0) + value
    return {p: v for p, v in out.items() if v}

@lru_cache(None)
def directional(mu, k):
    degree = sum(mu)
    if len(mu) > k or degree < k:
        return {}
    counts = Counter(mu + (0,) * (k-len(mu)))
    keys = tuple(sorted(counts))
    initial = tuple(counts[a] for a in keys)
    out = {}
    for beta in partitions(degree-k):
        if len(beta) > k:
            continue
        padded = beta + (0,) * (k-len(beta))
        @lru_cache(None)
        def rec(state):
            i = k-sum(state)
            if i == k:
                return 1
            value = 0
            for j, a in enumerate(keys):
                if not state[j] or a < padded[i]:
                    continue
                next_state = list(state)
                next_state[j] -= 1
                value += comb(a, padded[i]) * rec(tuple(next_state))
            return value
        value = factorial(k) * rec(initial)
        if value:
            out[beta] = value
    return out
