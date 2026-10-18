import math

def generate_section_svg(params):
    p = params.get('p', 100.0)
    z = params.get('z', 12)
    B1 = params.get('B1', 21.0)
    dw = params.get('dw', 155.0)
    hub_NL = params.get('hub_NL', 125.0)
    hub_Dn = params.get('hub_Dn', 175.0)
    hubType = params.get('hubType', 'Type_C')
    standard = params.get('standard', 'KWN_017')
    key_b = params.get('key_b', 32.0)
    key_t2 = params.get('key_t2', 10.4)

    # Basic tooth geometry
    alpha_rad = 2.0 * math.pi / z
    alpha_deg = 360.0 / z
    d0 = p / math.sin(math.pi / z)
    d1 = params.get('d1', 35.0)
    df = d0 - d1
    da = d0 + (0.8 * d1)
    ds = params.get('ds', (p / math.tan(alpha_rad / 2.0)) - 50.0 - 10.0)

    R0 = d0 / 2.0
    Rf = df / 2.0
    Ra = da / 2.0
    Rs = ds / 2.0

    w2 = B1 / 2.0
    w_tip2 = w2 * 0.72
    rtip = min(6.0, B1 * 0.10)
    w_flat2 = w_tip2 - rtip

    r_bore = dw / 2.0
    RH = min(Rf - 5.0, max(r_bore + 10.0, hub_Dn / 2.0))
    NL = hub_NL

    if hubType == 'Type_A':
        xh_L = -w2
        xh_R = +w2
    elif hubType == 'Type_B':
        xh_L = -w2
        xh_R = -w2 + NL
    else:
        xh_L = -NL / 2.0
        xh_R = +NL / 2.0

    print(f"Geometry: d0={d0:.1f}, df={df:.1f}, da={da:.1f}, ds={ds:.1f}")
    print(f"Hub: dw={dw}, Dn={RH*2:.1f}, NL={NL}, xh_L={xh_L:.1f}, xh_R={xh_R:.1f}")
    return True

if __name__ == '__main__':
    generate_section_svg({'p': 100, 'z': 12, 'B1': 21.0, 'dw': 155.0, 'hub_NL': 125.0, 'hub_Dn': 175.0, 'hubType': 'Type_C'})
    generate_section_svg({'p': 50, 'z': 12, 'B1': 52.5, 'dw': 35.0, 'hub_NL': 79.0, 'hub_Dn': 175.0, 'hubType': 'Type_C'})
