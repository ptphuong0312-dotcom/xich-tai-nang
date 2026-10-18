import math
import subprocess
import os

def render_section_html(geom, hub_params, out_path):
    p = geom['p']
    z = geom['z']
    B1 = geom['B1']
    d1 = geom['d1']
    dw = hub_params['dw']
    NL = hub_params['hub_NL']
    hubType = hub_params['hubType']
    standard = geom.get('standard', 'KWN_017')
    rawDn = hub_params.get('hub_Dn', dw * 1.55)

    alpha_rad = 2.0 * math.pi / z
    alpha_deg = 360.0 / z
    d0 = p / math.sin(math.pi / z)
    df = d0 - d1
    da = d0 + (0.8 * d1)
    ds = (p / math.tan(alpha_rad / 2.0)) - 50.0 - 10.0

    R0 = d0 / 2.0
    Rf = df / 2.0
    Ra = da / 2.0
    Rs = ds / 2.0

    w2 = B1 / 2.0
    w_tip2 = w2 * 0.72
    rtip = min(6.0, B1 * 0.10)
    w_flat2 = w_tip2 - rtip

    r_bore = dw / 2.0
    max_RH = max(r_bore + 12.0, Rf - 5.0)
    min_RH = r_bore + 10.0
    RH = max(min_RH, min(max_RH, rawDn / 2.0))
    Dn = RH * 2.0

    if hubType == 'Type_A':
        xh_L = -w2
        xh_R = +w2
    elif hubType == 'Type_B':
        xh_L = -w2
        xh_R = -w2 + NL
    else:
        xh_L = -NL / 2.0
        xh_R = +NL / 2.0

    bk = hub_params.get('key_b', 32.0)
    t2 = hub_params.get('key_t2', 10.4)

    S_sec = max(B1 * 2.8, (Ra - r_bore) * 1.25)
    textSz = max(3.5, min(S_sec * 0.035, B1 * 0.28))
    arrowSz = textSz * 0.95

    # Centerlines
    x_axis_min = min(xh_L, -w2) - textSz * 8.0
    x_axis_max = max(xh_R, +w2) + textSz * 8.0

    # Top Body
    if hubType == 'Type_A':
        dTopBody = f"M {-w2:.2f} {-r_bore:.2f} L {-w2:.2f} {-Rf:.2f} L {w2:.2f} {-Rf:.2f} L {w2:.2f} {-r_bore:.2f} L {bk/2:.2f} {-r_bore:.2f} L {bk/2:.2f} {-(r_bore+t2):.2f} L {-bk/2:.2f} {-(r_bore+t2):.2f} L {-bk/2:.2f} {-r_bore:.2f} Z"
        dBotBody = f"M {-w2:.2f} {r_bore:.2f} L {-w2:.2f} {Rf:.2f} L {w2:.2f} {Rf:.2f} L {w2:.2f} {r_bore:.2f} Z"
    elif hubType == 'Type_B':
        dTopBody = f"M {xh_L:.2f} {-r_bore:.2f} L {xh_L:.2f} {-Rf:.2f} L {w2:.2f} {-Rf:.2f} L {w2:.2f} {-RH:.2f} L {xh_R:.2f} {-RH:.2f} L {xh_R:.2f} {-r_bore:.2f} L {bk/2:.2f} {-r_bore:.2f} L {bk/2:.2f} {-(r_bore+t2):.2f} L {-bk/2:.2f} {-(r_bore+t2):.2f} L {-bk/2:.2f} {-r_bore:.2f} Z"
        dBotBody = f"M {xh_L:.2f} {r_bore:.2f} L {xh_L:.2f} {Rf:.2f} L {w2:.2f} {Rf:.2f} L {w2:.2f} {RH:.2f} L {xh_R:.2f} {RH:.2f} L {xh_R:.2f} {r_bore:.2f} Z"
    else:
        dTopBody = f"M {xh_L:.2f} {-r_bore:.2f} L {xh_L:.2f} {-RH:.2f} L {-w2:.2f} {-RH:.2f} L {-w2:.2f} {-Rf:.2f} L {w2:.2f} {-Rf:.2f} L {w2:.2f} {-RH:.2f} L {xh_R:.2f} {-RH:.2f} L {xh_R:.2f} {-r_bore:.2f} L {bk/2:.2f} {-r_bore:.2f} L {bk/2:.2f} {-(r_bore+t2):.2f} L {-bk/2:.2f} {-(r_bore+t2):.2f} L {-bk/2:.2f} {-r_bore:.2f} Z"
        dBotBody = f"M {xh_L:.2f} {r_bore:.2f} L {xh_L:.2f} {RH:.2f} L {-w2:.2f} {RH:.2f} L {-w2:.2f} {Rf:.2f} L {w2:.2f} {Rf:.2f} L {w2:.2f} {RH:.2f} L {xh_R:.2f} {RH:.2f} L {xh_R:.2f} {r_bore:.2f} Z"

    dToothTop = f"M {-w_flat2:.2f} {-Ra:.2f} L {w_flat2:.2f} {-Ra:.2f} A {rtip:.2f} {rtip:.2f} 0 0 1 {w_tip2:.2f} {-(Ra-rtip):.2f} L {w2:.2f} {-R0:.2f} L {w2:.2f} {-Rf:.2f} L {-w2:.2f} {-Rf:.2f} L {-w2:.2f} {-R0:.2f} L {-w_tip2:.2f} {-(Ra-rtip):.2f} A {rtip:.2f} {rtip:.2f} 0 0 1 {-w_flat2:.2f} {-Ra:.2f} Z"
    dToothBot = f"M {-w_flat2:.2f} {Ra:.2f} L {w_flat2:.2f} {Ra:.2f} A {rtip:.2f} {rtip:.2f} 0 0 0 {w_tip2:.2f} {Ra-rtip:.2f} L {w2:.2f} {R0:.2f} L {w2:.2f} {Rf:.2f} L {-w2:.2f} {Rf:.2f} L {-w2:.2f} {R0:.2f} L {-w_tip2:.2f} {Ra-rtip:.2f} A {rtip:.2f} {rtip:.2f} 0 0 0 {-w_flat2:.2f} {Ra:.2f} Z"

    # Dimensions
    # Right side cols: df, d0, da
    x_base_R = max(xh_R, w2) + textSz * 2.5
    colStep = textSz * 4.2
    x_df = x_base_R + colStep * 1
    x_d0 = x_base_R + colStep * 2
    x_da = x_base_R + colStep * 3

    # Left side cols: dw, Dn
    x_base_L = min(xh_L, -w2) - textSz * 2.5
    x_dw = x_base_L - colStep * 1
    x_Dn = x_base_L - colStep * 2

    # SVG ViewBox
    min_X = x_Dn - textSz * 14.0
    max_X = x_da + textSz * 16.0
    min_Y = -Ra - textSz * 8.0
    max_Y = Ra + textSz * 6.0
    vW = max_X - min_X
    vH = max_Y - min_Y

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ background: #0b0f19; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }}
  svg {{ width: 95vw; height: 95vh; }}
  text {{ font-family: 'Segoe UI', Arial, sans-serif; }}
</style>
</head>
<body>
<svg viewBox="{min_X:.2f} {min_Y:.2f} {vW:.2f} {vH:.2f}">
  <defs>
    <pattern id="hatch" patternUnits="userSpaceOnUse" width="8" height="8" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#38bdf8" stroke-width="0.6"/>
    </pattern>
  </defs>

  <!-- Title -->
  <text x="0" y="{-Ra - textSz * 6.2:.2f}" fill="#f8fafc" font-size="{textSz * 1.3:.2f}" font-weight="800" text-anchor="middle">MẶT CẮT DỌC TRỤC A-A (AXIAL SECTION A-A)</text>
  <text x="0" y="{-Ra - textSz * 4.5:.2f}" fill="#10b981" font-size="{textSz:.2f}" font-weight="700" text-anchor="middle">KẾT CẤU: {hubType} | NL = {NL:.1f} mm | ØDn = {Dn:.1f} mm | Ødw = {dw:.1f} mm</text>

  <!-- Shaft Axis (Centerline) -->
  <line x1="{x_axis_min:.2f}" y1="0" x2="{x_axis_max:.2f}" y2="0" stroke="#0284c7" stroke-width="0.7" stroke-dasharray="14, 3, 2, 3"/>
  <line x1="0" y1="{-Ra - textSz * 3.5:.2f}" x2="0" y2="{Ra + textSz * 3.5:.2f}" stroke="#0284c7" stroke-width="0.7" stroke-dasharray="14, 3, 2, 3"/>

  <!-- Metal Body Hatch Top & Bottom -->
  <path d="{dTopBody}" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <path d="{dTopBody}" fill="url(#hatch)" stroke="#38bdf8" stroke-width="1"/>
  <path d="{dBotBody}" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <path d="{dBotBody}" fill="url(#hatch)" stroke="#38bdf8" stroke-width="1"/>

  <!-- Teeth Top & Bottom -->
  <path d="{dToothTop}" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <path d="{dToothBot}" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>

  <!-- df line (dashed) -->
  <line x1="{-w2 - textSz:.2f}" y1="{-Rf:.2f}" x2="{w2 + textSz:.2f}" y2="{-Rf:.2f}" stroke="#ef4444" stroke-width="0.6" stroke-dasharray="5, 2.5"/>
  <line x1="{-w2 - textSz:.2f}" y1="{Rf:.2f}" x2="{w2 + textSz:.2f}" y2="{Rf:.2f}" stroke="#ef4444" stroke-width="0.6" stroke-dasharray="5, 2.5"/>

  <!-- d0 line (dashdot) -->
  <line x1="{-w2 - textSz * 1.5:.2f}" y1="{-R0:.2f}" x2="{w2 + textSz * 1.5:.2f}" y2="{-R0}" stroke="#38bdf8" stroke-width="0.6" stroke-dasharray="8, 2.5, 2, 2.5"/>
  <line x1="{-w2 - textSz * 1.5:.2f}" y1="{R0:.2f}" x2="{w2 + textSz * 1.5:.2f}" y2="{R0:.2f}" stroke="#38bdf8" stroke-width="0.6" stroke-dasharray="8, 2.5, 2, 2.5"/>

  <!-- Keyway ghost line -->
  <line x1="{-bk/2:.2f}" y1="{-r_bore:.2f}" x2="{bk/2:.2f}" y2="{-r_bore:.2f}" stroke="#64748b" stroke-width="0.5" stroke-dasharray="3, 2"/>

  <!-- Horizontal dims: B1 -->
  <line x1="{-w2:.2f}" y1="{-Ra - textSz * 2.2:.2f}" x2="{w2:.2f}" y2="{-Ra - textSz * 2.2:.2f}" stroke="#0284c7" stroke-width="0.5"/>
  <line x1="{-w2:.2f}" y1="{-Ra:.2f}" x2="{-w2:.2f}" y2="{-Ra - textSz * 2.8:.2f}" stroke="#0284c7" stroke-width="0.4"/>
  <line x1="{w2:.2f}" y1="{-Ra:.2f}" x2="{w2:.2f}" y2="{-Ra - textSz * 2.8:.2f}" stroke="#0284c7" stroke-width="0.4"/>
  <text x="0" y="{-Ra - textSz * 2.6:.2f}" fill="#0284c7" font-size="{textSz:.2f}" font-weight="700" text-anchor="middle">B1 = {B1:.1f} mm</text>

  <!-- Horizontal dims: NL -->
  <line x1="{xh_L:.2f}" y1="{RH + textSz * 3.0:.2f}" x2="{xh_R:.2f}" y2="{RH + textSz * 3.0:.2f}" stroke="#10b981" stroke-width="0.5"/>
  <line x1="{xh_L:.2f}" y1="{RH:.2f}" x2="{xh_L:.2f}" y2="{RH + textSz * 3.6:.2f}" stroke="#10b981" stroke-width="0.4"/>
  <line x1="{xh_R:.2f}" y1="{RH:.2f}" x2="{xh_R:.2f}" y2="{RH + textSz * 3.6:.2f}" stroke="#10b981" stroke-width="0.4"/>
  <text x="{(xh_L + xh_R)/2.0:.2f}" y="{RH + textSz * 4.4:.2f}" fill="#10b981" font-size="{textSz:.2f}" font-weight="700" text-anchor="middle">NL = {NL:.1f} mm</text>

  <!-- Vertical Diameters Right: df, d0, da -->
  <!-- df -->
  <line x1="{w2:.2f}" y1="{-Rf:.2f}" x2="{x_df + textSz:.2f}" y2="{-Rf:.2f}" stroke="#ef4444" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{w2:.2f}" y1="{Rf:.2f}" x2="{x_df + textSz:.2f}" y2="{Rf:.2f}" stroke="#ef4444" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{x_df:.2f}" y1="{-Rf:.2f}" x2="{x_df:.2f}" y2="{Rf:.2f}" stroke="#ef4444" stroke-width="0.7"/>
  <text x="{x_df + textSz * 0.5:.2f}" y="{-Rf * 0.4:.2f}" fill="#ef4444" font-size="{textSz * 0.95:.2f}" font-weight="700">Ø df = {df:.2f} (h11)</text>

  <!-- d0 -->
  <line x1="{w2:.2f}" y1="{-R0:.2f}" x2="{x_d0 + textSz:.2f}" y2="{-R0:.2f}" stroke="#38bdf8" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{w2:.2f}" y1="{R0:.2f}" x2="{x_d0 + textSz:.2f}" y2="{R0:.2f}" stroke="#38bdf8" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{x_d0:.2f}" y1="{-R0:.2f}" x2="{x_d0:.2f}" y2="{R0:.2f}" stroke="#38bdf8" stroke-width="0.7"/>
  <text x="{x_d0 + textSz * 0.5:.2f}" y="{0:.2f}" fill="#38bdf8" font-size="{textSz * 0.95:.2f}" font-weight="700">Ø d0 = {d0:.2f}</text>

  <!-- da -->
  <line x1="{w_tip2:.2f}" y1="{-Ra:.2f}" x2="{x_da + textSz:.2f}" y2="{-Ra:.2f}" stroke="#c084fc" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{w_tip2:.2f}" y1="{Ra:.2f}" x2="{x_da + textSz:.2f}" y2="{Ra:.2f}" stroke="#c084fc" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{x_da:.2f}" y1="{-Ra:.2f}" x2="{x_da:.2f}" y2="{Ra:.2f}" stroke="#c084fc" stroke-width="0.7"/>
  <text x="{x_da + textSz * 0.5:.2f}" y="{Rf * 0.4:.2f}" fill="#c084fc" font-size="{textSz * 0.95:.2f}" font-weight="700">Ø da = {da:.2f}</text>

  <!-- Vertical Diameters Left: dw, Dn -->
  <!-- dw -->
  <line x1="{xh_L:.2f}" y1="{-r_bore:.2f}" x2="{x_dw - textSz:.2f}" y2="{-r_bore:.2f}" stroke="#fbbf24" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{xh_L:.2f}" y1="{r_bore:.2f}" x2="{x_dw - textSz:.2f}" y2="{r_bore:.2f}" stroke="#fbbf24" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{x_dw:.2f}" y1="{-r_bore:.2f}" x2="{x_dw:.2f}" y2="{r_bore:.2f}" stroke="#fbbf24" stroke-width="0.7"/>
  <text x="{x_dw - textSz * 0.5:.2f}" y="{-r_bore * 0.4:.2f}" fill="#fbbf24" font-size="{textSz * 0.95:.2f}" font-weight="700" text-anchor="end">Ø dw = {dw:.1f} (H7)</text>

  <!-- Dn -->
  <line x1="{xh_L:.2f}" y1="{-RH:.2f}" x2="{x_Dn - textSz:.2f}" y2="{-RH:.2f}" stroke="#34d399" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{xh_L:.2f}" y1="{RH:.2f}" x2="{x_Dn - textSz:.2f}" y2="{RH:.2f}" stroke="#34d399" stroke-width="0.5" stroke-dasharray="4,2"/>
  <line x1="{x_Dn:.2f}" y1="{-RH:.2f}" x2="{x_Dn:.2f}" y2="{RH:.2f}" stroke="#34d399" stroke-width="0.7"/>
  <text x="{x_Dn - textSz * 0.5:.2f}" y="{RH * 0.4:.2f}" fill="#34d399" font-size="{textSz * 0.95:.2f}" font-weight="700" text-anchor="end">Ø Dn = {Dn:.1f}</text>

  <!-- Keyway note -->
  <line x1="0" y1="{-(r_bore + t2):.2f}" x2="{-textSz * 3.5:.2f}" y2="{-(r_bore + t2 + textSz * 3.0):.2f}" stroke="#fbbf24" stroke-width="0.5"/>
  <line x1="{-textSz * 3.5:.2f}" y1="{-(r_bore + t2 + textSz * 3.0):.2f}" x2="{-textSz * 8.0:.2f}" y2="{-(r_bore + t2 + textSz * 3.0):.2f}" stroke="#fbbf24" stroke-width="0.5"/>
  <text x="{-textSz * 8.2:.2f}" y="{-(r_bore + t2 + textSz * 3.3):.2f}" fill="#fbbf24" font-size="{textSz * 0.85:.2f}" font-weight="700" text-anchor="end">Rãnh then {bk:.0f}x{t2:.1f} (DIN 6885)</text>

</svg>
</body>
</html>
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML written to {out_path}")

if __name__ == '__main__':
    render_section_html(
        {'p': 100, 'z': 12, 'B1': 21.0, 'd1': 35.0},
        {'dw': 155.0, 'hub_NL': 125.0, 'hubType': 'Type_C', 'hub_Dn': 175.0, 'key_b': 32.0, 'key_t2': 10.4},
        'd:/Google Antigravity/Xich tai nang/test_section_fv90.html'
    )
    render_section_html(
        {'p': 50, 'z': 12, 'B1': 52.5, 'd1': 16.0},
        {'dw': 35.0, 'hub_NL': 79.0, 'hubType': 'Type_C', 'hub_Dn': 70.0, 'key_b': 10.0, 'key_t2': 3.3},
        'd:/Google Antigravity/Xich tai nang/test_section_mt20.html'
    )
