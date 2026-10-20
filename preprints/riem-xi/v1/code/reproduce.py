#!/usr/bin/env python3
"""Run the four certificate programs in a fresh, isolated output directory."""
import argparse
import importlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

SCRIPTS = ["verify_reciprocal_xi.py", "verify_laguerre_identities.py",
           "verify_reciprocal_logconcavity.py", "verify_lambda_pf_higher.py"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="New directory for the source snapshot, logs, and results")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    versions = {package: importlib.import_module(package).__version__ for package in ("mpmath", "sympy")}
    if versions != {"mpmath": "1.3.0", "sympy": "1.14.0"}:
        parser.error("Install the pinned versions in requirements-verification.txt")
    output = args.output_dir.expanduser().resolve()
    if output == source or source in output.parents:
        parser.error("Choose an output directory outside the code folder.")
    output.mkdir(parents=True, exist_ok=False)
    snapshot = output / "code"
    shutil.copytree(source, snapshot, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    report = {"python": sys.version, "platform": platform.platform(), "packages": versions, "runs": [],
              "scope": "Scalar, finite algebraic, and interval checks; not independent verification of the analytic proofs or of external zero computations."}
    for script in SCRIPTS:
        name = Path(script).stem
        print(f"Running {name}", flush=True)
        log = output / (name + ".log")
        with log.open("w") as stream:
            result = subprocess.run([sys.executable, str(snapshot / script)], cwd=output,
                                    stdout=stream, stderr=subprocess.STDOUT)
        report["runs"].append({"name": name, "returncode": result.returncode, "log": log.name})
        report["passed"] = all(run["returncode"] == 0 for run in report["runs"])
        (output / "run-summary.json").write_text(json.dumps(report, indent=2) + "\n")
        if result.returncode:
            print(f"FAILED: see {log}", flush=True)
            return result.returncode
    print(f"All {len(SCRIPTS)} programs passed. Results: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
