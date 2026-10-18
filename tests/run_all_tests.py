"""
Master QA Test Runner
Executes all regression and validation test suites for the KettenWulf Sprocket Studio.
"""

import subprocess
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("==================================================================")
    print("        KETTENWULF SPROCKET CAD STUDIO - MASTER QA RUNNER        ")
    print("==================================================================")

    test_scripts = [
        os.path.join('tests', 'test_geometry_consistency.py'),
        os.path.join('tests', 'test_chain_roller_clearance.py'),
        os.path.join('tests', 'test_dxf_syntax_and_layers.py'),
        os.path.join('tests', 'audit_and_crosscheck_all_data.py'),
        os.path.join('tests', 'test_chrome_catalogs.py'),
        os.path.join('tests', 'verify_all_standards_gap.py')
    ]

    all_passed = True
    for script in test_scripts:
        print(f"\n--- Running: {script} ---")
        res = subprocess.run([sys.executable, script], capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(res.stdout)
        if res.returncode != 0:
            print(res.stderr)
            print(f"FAILED: {script}")
            all_passed = False
        else:
            print(f"SUCCESS: {script} PASSED.")

    print("\n==================================================================")
    if all_passed:
        print("          ALL TEST SUITES COMPLETED: 100% PASS!                  ")
        print("    System geometry, kinematics, and CAD files are VERIFIED.      ")
    else:
        print("          SOME TESTS FAILED! PLEASE REVIEW LOGS ABOVE.           ")
    print("==================================================================")
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()
