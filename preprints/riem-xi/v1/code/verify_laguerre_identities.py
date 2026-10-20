#!/usr/bin/env python3
"""Exact finite algebra checks for the Laguerre coefficient identities
(Section 4 of "On some positivity properties of the Riemann Xi function").

Requires Python 3 and SymPy. Run:
    python verify_laguerre_identities.py

These checks verify algebra, not the canonical-product convergence argument,
external zero verification, or any claim of complete monotonicity or RH.
"""
from __future__ import annotations
import sympy as sp


def check_zero(name: str, expression: sp.Expr) -> None:
    """Raise on a failed or undecidable exact identity."""
    simplified = sp.simplify(sp.expand(expression))
    if simplified != 0:
        raise AssertionError(f"Identity failed: {name}\nRemainder: {simplified}")
    print(f"PASS: {name}")


def main() -> None:
    x, y, a, b = sp.symbols("x y a b", real=True)
    qpoly = lambda z: (z-a)**2+b**2
    target = ((x-a)**2+b**2)**2 + 2*((x-a)**2-b**2)*y**2+y**4
    check_zero("conjugate-pair quartic and coefficient 2((x-a)^2-b^2)",
               qpoly(x+sp.I*y)*qpoly(x-sp.I*y)-target)
    check_zero("conjugate-pair logarithmic second derivative",
               1/(x-a-sp.I*b)**2 + 1/(x-a+sp.I*b)**2
               -2*((x-a)**2-b**2)/((x-a)**2+b**2)**2)

    for n in range(7):
        derivs = sp.symbols(f"f0:{2*n+1}", real=True)
        positive = sum(derivs[j]*(sp.I*y)**j/sp.factorial(j) for j in range(2*n+1))
        negative = positive.subs(y, -y)
        coefficient = sp.expand(positive*negative).coeff(y, 2*n)
        laguerre = sum((-1)**(j+n)*sp.binomial(2*n,j)*derivs[j]*derivs[2*n-j]
                       for j in range(2*n+1))/sp.factorial(2*n)
        check_zero(f"generalized Laguerre generating coefficient n={n}", coefficient-laguerre)
        tensor = sum((-1)**j*sp.binomial(2*n,j)
                     *((-1)**j*derivs[j])*((-1)**(2*n-j)*derivs[2*n-j])
                     for j in range(2*n+1))
        check_zero(f"tensor-square sign and factorial n={n}",
                   tensor-(-1)**n*sp.factorial(2*n)*laguerre)

    t, q = sp.symbols("t q", positive=True)
    expression = sp.exp(-q*t)/t
    for k in range(9):
        check_zero(f"conjugated derivative identity k={k}",
                   expression-sp.exp(-q*t)*(-1)**k*sp.factorial(k)/t**(k+1))
        expression = sp.diff(expression,t)+q*expression

    B = sp.Function("B")
    s = sp.symbols("s", real=True)
    expected = 2*sp.diff(B(s),s).subs(s,-x*x)-4*x*x*sp.diff(B(s),s,2).subs(s,-x*x)
    check_zero("chain rule for L1[Xi]/Xi^2", -sp.diff(B(-x*x),x,2)-expected)

    for k in range(10):
        gamma_sum = sum(sp.binomial(k,j)*sp.factorial(k-j)*sp.rf(sp.Rational(1,2),j)
                        for j in range(k+1))
        check_zero(f"small-time gamma-convolution moment k={k}",
                   gamma_sum-sp.rf(sp.Rational(3,2),k))

    for n in range(7):
        check_zero(f"Hermite-Laguerre normalization n={n}",
                   sp.hermite(2*n,x)-(-1)**n*2**(2*n)*sp.factorial(n)
                   *sp.assoc_laguerre(n,sp.Rational(-1,2),x*x))

    determinant = sp.Matrix([[1,1],[1,-1]]).det()
    if abs(determinant) != 2:
        raise AssertionError("Incorrect Fourier change-of-variables Jacobian")
    print("PASS: absolute Jacobian for (s,t)=(u+v,u-v) is 2")
    print("All exact finite algebra checks passed.")


if __name__ == "__main__":
    main()
