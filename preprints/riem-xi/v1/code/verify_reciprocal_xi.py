#!/usr/bin/env python3
"""Directed interval checks for the counting and approximation inputs
(Appendix F.1 of "On some positivity properties of the Riemann Xi function").

Run with Python 3 and mpmath installed:
    python verify_reciprocal_xi.py

The checks are: the counting bound |N(Y)-M(Y)| <= log(Y+2)/8 + 4 derived
from Bellotti--Wong, the two height-100 estimates used in the
log-concavity proofs, the high-anchor counting margin at U = 1000, and
the total-variation bound 225 b_U < 4.5e-9 at U = 3e12. The program does
NOT verify zeta zeros or certify the analytic arguments of the paper.
All nonintegral inputs are decimal strings, not binary floating-point values.
"""
from mpmath import iv

iv.dps = 60


def check(name, proposition):
    if proposition is not True:
        raise AssertionError(f"Interval check failed or was undecidable: {name}")
    print(f"PASS: {name}")


def show(name, value):
    print(f"{name} = {value}")


def main():
    T = iv.mpf(3_000_000_000_000)

    # Bellotti--Wong Theorem 1.1 -> the counting bound of Section 2.1.
    u = iv.mpf('0.12567')/iv.mpf('0.013')
    excess = iv.mpf('0.12567')*iv.ln(u) - iv.mpf('0.013')*u
    constant = iv.mpf('3.77417')
    check('total counting slack < 3.934', excess + constant < iv.mpf('3.934'))
    M_e = -iv.e*iv.ln(2*iv.pi)/(2*iv.pi)
    check('count at e < 4', M_e + iv.mpf('0.11200') + constant < 4)
    check('main counting term at e > -1', M_e > -1)

    # Height-100 inputs of the log-concavity proofs.
    eps = iv.mpf(100)**4*iv.exp(-100)
    check('retained-zero epsilon_100 < 1', eps < 1)
    check('reciprocal-square tail bound at 100 < 1',
          2*(iv.ln(100)+1)/100 < 1)

    # A high retained zero gives PF-infinity approximants of the original laws.
    U = iv.mpf(1000)
    count_margin = U/32 - iv.ln(U+2)/4 - 8
    check('high-anchor count margin at 1000 > 21', count_margin > 21)
    check('log(1000/(8*pi)) > 3', iv.ln(U/(8*iv.pi)) > 3)
    pf_error = 225*(16/T**2 + 2*(iv.ln(T)+1)/T)
    show('PF approximation total variation upper bound', pf_error)
    check('PF approximation error < 4.5e-9', pf_error < iv.mpf('4.5e-9'))
    print('\nAll scalar checks passed. Analytic proofs and external zero verification remain separate inputs.')


if __name__ == '__main__':
    main()
