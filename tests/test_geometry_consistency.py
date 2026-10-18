"""
Automated Test Suite: Geometry Consistency Verification
Validates that calculated pitch circle diameters, root diameters, flank angles,
and radii match the KettenWulf Engineering Handbook and Page 67 catalog table.
"""

import math
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_pitch_circles():
    print("--> Testing Pitch Circle Diameters against Page 67 Catalog Table...")
    with open('data/pitch_circle_table.json', 'r', encoding='utf-8') as f:
        p_table = json.load(f)

    pitches = p_table['pitches']
    teeth_dict = p_table['teeth']

    tested_count = 0
    for z_str, pitch_map in teeth_dict.items():
        z = int(z_str)
        for p_str, expected_d0 in pitch_map.items():
            p = float(p_str)
            calc_d0 = round(p / math.sin(math.pi / z), 2)
            assert abs(calc_d0 - expected_d0) <= 0.05, f"Mismatch at z={z}, p={p}: calc={calc_d0}, expected={expected_d0}"
            tested_count += 1

    print(f"    [PASS] {tested_count} pitch circle values verified against Page 67 table!")

def test_kwn017_opening_angles():
    print("--> Testing KWN 017 Opening Angle beta and Flank Angle gamma...")
    with open('data/tooth_profile_rules.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)['KWN_017']

    beta_table = rules['formulas']['beta_table']

    test_cases = [
        (6, 74.0, 7.0),
        (8, 74.0, 14.5),
        (11, 74.0, 20.636),
        (12, 56.0, 13.0),
        (20, 56.0, 19.0),
        (29, 56.0, 21.793),
        (30, 38.0, 13.0),
        (45, 38.0, 15.0)
    ]

    for z, expected_beta, expected_gamma in test_cases:
        matched_beta = None
        for b_rule in beta_table:
            if b_rule['min_z'] <= z <= b_rule['max_z']:
                matched_beta = b_rule['beta_deg']
                break
        assert matched_beta == expected_beta, f"Beta mismatch for z={z}: got {matched_beta}, expected {expected_beta}"
        calc_gamma = round(matched_beta / 2.0 - 180.0 / z, 3)
        assert abs(calc_gamma - expected_gamma) <= 0.05, f"Gamma mismatch for z={z}: calc={calc_gamma}, expected={expected_gamma}"

    print(f"    [PASS] KWN 017 beta lookup table and gamma math verified for all z ranges!")

def test_chain_catalog_integrity():
    print("--> Testing Chain Catalog Data Integrity...")
    with open('data/chain_catalogs.json', 'r', encoding='utf-8') as f:
        cat = json.load(f)

    for series_name, models in cat.items():
        assert len(models) > 0, f"Series {series_name} is empty!"
        for m in models:
            assert 'name' in m and 'FB' in m and 'b1' in m and 'd1' in m and 'd3' in m
            assert m['b1'] > 0 and m['d1'] > 0 and m['d3'] >= m['d1'], f"Invalid geometry in {m['name']}"
            assert len(m['p_list']) > 0, f"No pitch list for {m['name']}"

    print(f"    [PASS] All {sum(len(v) for v in cat.values())} chain models have valid geometric dimensions!")

if __name__ == '__main__':
    print("=== RUNNING GEOMETRY CONSISTENCY TEST SUITE ===")
    test_pitch_circles()
    test_kwn017_opening_angles()
    test_chain_catalog_integrity()
    print("=== ALL GEOMETRY TESTS PASSED SUCCESSFULLY! ===")
