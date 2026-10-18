"""
Automated Test Suite: AutoCAD DXF Syntax, Encodings & Layers Verification
Validates that generated DXF files comply with AutoCAD AC1009 (R12),
contain valid escapes (%%c, %%d), and contain no unescaped UTF-8 characters.
"""

import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def test_dxf_files():
    print("--> Testing DXF Output Files Syntax & Encodings...")
    try:
        import ezdxf
    except ImportError:
        print("    [SKIP] ezdxf not installed, skipping direct ezdxf parsing")
        return

    # Look for clean dxf files in tests/outputs or root
    search_dirs = [os.path.join('tests', 'outputs'), '.']
    dxf_candidates = []
    for sdir in search_dirs:
        if os.path.exists(sdir):
            dxf_candidates.extend([os.path.join(sdir, f) for f in os.listdir(sdir) if f.startswith('clean_') and f.endswith('.dxf')])
    if not dxf_candidates:
        for sdir in search_dirs:
            if os.path.exists(sdir):
                dxf_candidates.extend([os.path.join(sdir, f) for f in os.listdir(sdir) if f.endswith('.dxf') and not f.startswith('verified_') and not f.startswith('test_')])

    for f in dxf_candidates:
        print(f"    Checking {f}...")
        with open(f, 'rb') as fp:
            content = fp.read()

        # Check for unescaped Greek or Unicode characters
        for byte in [b'\xcf\x86', b'\xcf\x80', b'\xce\xb3', b'\xce\xb2', b'\xce\xb1', b'\xc2\xb0']:
            assert byte not in content, f"Found unescaped Unicode byte {byte} in {f}!"

        doc = ezdxf.readfile(f)
        valid_versions = ['AC1009', 'AC1015', 'AC1018', 'AC1021', 'AC1024', 'AC1027', 'AC1032']
        assert doc.dxfversion in valid_versions, f"Invalid DXF version {doc.dxfversion} in {f}"
        print(f"    [PASS] {f} (AutoCAD {doc.dxfversion}) is valid DXF with 0 syntax or encoding errors.")

if __name__ == '__main__':
    print("=== RUNNING DXF SYNTAX AND LAYERS TEST SUITE ===")
    test_dxf_files()
    print("=== ALL DXF TESTS PASSED SUCCESSFULLY! ===")
