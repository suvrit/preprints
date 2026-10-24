"""Exact projection-spectral relaxation for the signed quantum permanent.

No numerical optimizer or external package is needed to build this model.
All coefficients are fractions. Certificate order is deterministic.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import comb
from typing import Iterator

Q = Fraction


def partitions(n: int, maximum: int | None = None) -> Iterator[tuple[int, ...]]:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        yield ()
        return
    if maximum is None:
        maximum = n
    for a in range(min(n, maximum), 0, -1):
        for tail in partitions(n-a, a):
            yield (a,) + tail


def profile(lam: tuple[int, ...], k: int) -> tuple[Q, ...]:
    """[t^(n-j)] m_lam(t 1 + 1_[k])/m_lam(1), 0 <= j <= n.

    Average the exponents occupying the k distinguished slots. This is
    independent of the dynamic-programming implementation used to discover
    the certificates.
    """
    n = sum(lam)
    if not 0 <= k <= n:
        raise ValueError("projection rank is outside 0,...,n")
    padded = lam + (0,) * (n-len(lam))
    subset_sums = [sum(padded[i] for i in I)
                   for I in combinations(range(n), k)]
    denominator = comb(n, k)
    return tuple(Q(sum(comb(s,j) if s >= j else 0 for s in subset_sums),
                   denominator) for j in range(n+1))


@dataclass(frozen=True)
class Vertex:
    ones: int
    fractional_count: int
    fractional_value: Q
    elementary: tuple[Q, ...]


def vertices(n: int, k: int) -> tuple[Vertex, ...]:
    """Finite coefficient-hull generators for 0 <= y <= 1, sum(y)=k."""
    if not 0 < k < n:
        raise ValueError("require 0 < k < n")
    out = [Vertex(k, 0, Q(0),
                  tuple(Q(comb(k,j) if j <= k else 0) for j in range(n+1)))]
    for a in range(k):
        for b in range(k-a+1, n-a+1):
            t = Q(k-a,b)
            e = tuple(sum((Q(comb(a,i)*comb(b,j-i))*t**(j-i)
                           for i in range(max(0,j-b), min(j,a)+1)), Q(0))
                      for j in range(n+1))
            out.append(Vertex(a,b,t,e))
    assert len(out) == 1 + k*(n-k)
    return tuple(out)


@dataclass
class Model:
    n: int
    partitions: tuple[tuple[int, ...], ...]
    vertices: dict[int, tuple[Vertex, ...]]
    groups: list[list[int]]
    matrix: list[list[Q]]
    rhs: list[Q]
    objective: list[Q]
    row_metadata: list[list[object]]


def build(n: int) -> Model:
    if n < 2:
        raise ValueError("this relaxation is stated for n >= 2")
    ps = tuple(partitions(n))
    count = len(ps)
    groups = [list(range(count))]
    vs = {}
    offsets = {}
    for k in range(1,n//2+1):
        vs[k] = vertices(n,k)
        offsets[k] = count
        groups.append(list(range(count,count+len(vs[k]))))
        count += len(vs[k])
    A, b, meta = [], [], []
    for k, group in enumerate(groups):
        row = [Q(0)]*count
        for idx in group:
            row[idx] = Q(1)
        A.append(row)
        b.append(Q(1))
        meta.append(["sum",k])
    for k, vv in vs.items():
        pp = [profile(lam,k) for lam in ps]
        for j in range(2,n+1):
            row = [Q(0)]*count
            for idx in range(len(ps)):
                row[idx] = pp[idx][j]
            for idx, v in enumerate(vv):
                row[offsets[k]+idx] = -v.elementary[j]
            A.append(row)
            b.append(Q(0))
            meta.append(["spectral",k,j])
    c = [Q((-1)**(n-len(lam)),comb(n,len(lam))) for lam in ps]
    c += [Q(0)]*(count-len(c))
    return Model(n,ps,vs,groups,A,b,c,meta)


def build_strengthened(n: int) -> Model:
    """Also retain the established mixed-discriminant floor W_n >= n!/n^n.

    The last nonnegative variable is the slack W_n - n!/n^n.
    """
    from math import factorial
    m = build(n)
    for row in m.matrix:
        row.append(Q(0))
    m.objective.append(Q(0))
    row = [Q(0)]*len(m.objective)
    row[m.partitions.index((1,)*n)] = Q(1)
    row[-1] = Q(-1)
    m.matrix.append(row)
    m.rhs.append(Q(factorial(n),n**n))
    m.row_metadata.append(["floor","W_n"])
    return m
