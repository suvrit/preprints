"""Exact family checks using unchanged source programs and coefficient tables.

Run from any working directory with Python >= 3.10, without -O. This writes
logs and result JSON files in the package: run a copy to retain the snapshot.
The analytic positivity proofs and scope are documented in README.md.
"""
from fractions import Fraction
from math import factorial
from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
RELEASE = HERE.parent
VERIFICATION = RELEASE / 'verification'

COMMANDS = [
    ('nine-full-polynomial', 'coherent9', 'verify_polynomial.py', 'coherent_polynomial.json'),
    ('nine-input-order', 'coherent9', 'verify_input_order.py', 'verify_input_order.json'),
    ('eight-full-polynomial', 'coherence_descent/checks', 'rank8_family.py', 'rank8_family.json'),
    ('eight-input-output-descent', 'coherence_descent/checks', 'verify_descent.py', 'verify_descent.json'),
    ('eight-endpoint', 'coherence_descent/checks', 'rank8_certificate.py', 'rank8_certificate.json'),
]


def run_one(name, relative, script, result):
    cwd = HERE / relative
    log = VERIFICATION / f'family-{name}.log'
    start = time.perf_counter()
    with log.open('wb') as stream:
        process = subprocess.Popen([sys.executable, '-B', script], cwd=cwd,
                                   stdout=stream, stderr=subprocess.STDOUT)
        if hasattr(os, 'wait4'):
            _, status, usage = os.wait4(process.pid, 0)
            process.returncode = os.waitstatus_to_exitcode(status)
            peak = usage.ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
        else:
            process.wait()
            peak = None
    record = {'name': name, 'working_directory_relative_to_release': 'families/' + relative,
              'command': ['python3', '-B', script], 'exit_status': process.returncode,
              'elapsed_seconds': round(time.perf_counter() - start, 6),
              'peak_resident_memory_bytes': peak,
              'log': log.relative_to(RELEASE).as_posix(),
              'generated_result': (cwd / result).relative_to(RELEASE).as_posix()}
    print(name, record['exit_status'], record['elapsed_seconds'], flush=True)
    assert process.returncode == 0, record
    return record


def coefficient_checks():
    nine = json.loads((HERE / 'coherent9/coherent_polynomial.json').read_text())
    expected_nine = {'(0, 0)': '-3/64', '(0, 2)': '-27/256', '(0, 4)': '-3/256',
                     '(2, 0)': '-27/256', '(2, 2)': '-3/16', '(2, 4)': '-3/256',
                     '(4, 0)': '-3/256', '(4, 2)': '-3/256'}
    assert nine['Gamma_coefficients'] == expected_nine
    assert nine['Phi_at_1'] == '-1/737280'
    eight = json.loads((HERE / 'coherence_descent/checks/rank8_family.json').read_text())
    expected_eight = {'(0, 0)': '-5/512', '(2, 0)': '-9/1024', '(0, 2)': '-21/1024',
                      '(4, 0)': '1/128', '(2, 2)': '-17/512'}
    assert eight == expected_eight, eight
    gamma9_start = Fraction(expected_nine['(0, 0)'])
    gamma9_end = sum(map(Fraction, expected_nine.values()))
    gamma8_start = Fraction(expected_eight['(0, 0)'])
    gamma8_end = sum(map(Fraction, expected_eight.values()))
    assert gamma9_end / gamma9_start == Fraction(21, 2)
    assert gamma8_end / gamma8_start == Fraction(33, 5)
    assert gamma9_start / factorial(9) == Fraction(-1, 7741440)
    assert gamma8_start / factorial(8) == Fraction(-1, 4128768)
    return {'nine_Gamma_coefficients': expected_nine, 'eight_Gamma_coefficients': expected_eight,
            'nine_negative_magnitude_improvement': '21/2',
            'eight_negative_magnitude_improvement': '33/5',
            'nine_family_minimum_Phi': '-1/737280',
            'eight_family_minimum_Phi': '-11/6881280'}


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Do not disable assertions with -O.')
    started = time.perf_counter()
    records = [run_one(*command) for command in COMMANDS]
    coefficients = coefficient_checks()
    inventory = json.loads((VERIFICATION / 'family-copied-inputs.json').read_text())
    assert all(hashlib.sha256((RELEASE / item['release_path']).read_bytes()).hexdigest()
               == item['sha256'] for item in inventory)
    report = {'status': 'all fresh family checks passed', 'python': sys.version,
              'platform': platform.platform(), 'commands': records,
              'total_elapsed_seconds': round(time.perf_counter() - started, 6),
              'peak_resident_memory_bytes': max((r['peak_resident_memory_bytes'] or 0) for r in records),
              'coefficient_checks': coefficients, 'copied_sources_unchanged': True,
              'scope': 'Full polynomial coefficient identities; independent input/output contraction checks at exact parameters; exact marginals, norm profiles and family gap identity. Positivity, exact parameter feasibility, and minimization on the full feasible square use the analytic manuscript proofs. The attained family minima are upper bounds on unrestricted mu_8 and mu_9, not global minima of the full positive bistochastic classes.'}
    (VERIFICATION / 'family-run-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
