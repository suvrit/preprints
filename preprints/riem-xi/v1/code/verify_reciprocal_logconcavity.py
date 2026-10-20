#!/usr/bin/env python3
"""The two scalar bounds of the exponential-tilt proofs of log-concavity
(Section 3.1 of "On some positivity properties of the Riemann Xi function").

The real-zero enclosure near 21.022 is checked by verify_lambda_pf_higher.py.
This program does not verify Yamazato's theorem or the analytic reductions.
"""
from mpmath import iv

iv.dps = 80
Q = lambda x: iv.mpf(str(x))


def check(name, value, bound, direction):
    ok = value < Q(bound) if direction == '<' else value > Q(bound)
    if not ok:
        raise AssertionError((name, value, bound))
    print(f'PASS: {name}: {value}')


def main():
    check('one-sided shifted-tail relative bound', 100**4*iv.exp(-100), 1, '<')
    check('bilateral tilted-tail relative bound', 100**4*iv.exp(-78*iv.pi), 1, '<')
    print('BOTH LOG-CONCAVITY SCALAR CHECKS PASSED')


if __name__ == '__main__':
    main()
