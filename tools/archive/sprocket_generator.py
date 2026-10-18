"""
KettenWulf Sprocket 2D Geometric Calculator & DXF/SVG Generator
Tuân thủ tiêu chuẩn nhà máy KWN 017 và KWN 015 của KettenWulf
"""

import math
import argparse
import sys
import os
import ezdxf
from ezdxf import units

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class KettenWulfSprocket:
    def __init__(self, p=400.0, z=8, d1=68.0, b1=66.0, g=90.0, r4=5.0, 
                 chain_type='without_roller', standard='KWN_017', 
                 bore_dia=100.0, key_width=28.0, key_depth=10.0, gamma_override=None):
        """
        Khởi tạo thông số đĩa xích theo chuẩn KettenWulf:
        :param p: Bước xích [mm]
        :param z: Số răng đĩa xích (nguyên >= 5)
        :param d1: Đường kính ống lót / con lăn [mm]
        :param b1: Chiều rộng trong mắt xích [mm]
        :param g: Chiều cao má xích [mm]
        :param r4: Bán kính góc lượn vành đĩa xích [mm]
        :param chain_type: 'without_roller' (da = d0 + 0.8*d1), 
                           'with_roller' (da = d0 + 0.4*d1), 
                           'with_protection_roller' (da = d0 + 0.6*d1)
        :param standard: 'KWN_017' hoặc 'KWN_015'
        :param bore_dia: Đường kính lỗ trục dw [mm]
        :param key_width: Bề rộng then DIN 6885 [mm]
        :param key_depth: Chiều sâu rãnh then trên may-ơ t2 [mm]
        :param gamma_override: Góc sườn răng gamma [độ] (dùng cho KWN 015)
        """
        self.p = float(p)
        self.z = int(z)
        self.d1 = float(d1)
        self.b1 = float(b1)
        self.g = float(g)
        self.r4 = float(r4)
        self.chain_type = chain_type
        self.standard = standard
        self.bore_dia = float(bore_dia)
        self.key_width = float(key_width)
        self.key_depth = float(key_depth)
        self.gamma_override = gamma_override

        self.calculate_parameters()

    def calculate_parameters(self):
        # 1. Góc bước răng alpha
        self.alpha_deg = 360.0 / self.z
        self.alpha_rad = math.radians(self.alpha_deg)

        # 2. Đường kính vòng chia d0
        self.d0 = self.p / math.sin(math.radians(180.0 / self.z))
        self.R0 = self.d0 / 2.0

        # 3. Đường kính vòng chân răng df (miền dung sai h11)
        self.df = self.d0 - self.d1
        self.Rf = self.df / 2.0

        # 4. Đường kính vòng đỉnh răng da
        if self.chain_type == 'with_roller':
            self.da = self.d0 + 0.4 * self.d1
        elif self.chain_type == 'with_protection_roller':
            self.da = self.d0 + 0.6 * self.d1
        else: # without_roller
            self.da = self.d0 + 0.8 * self.d1
        self.Ra = self.da / 2.0

        # 5. Đường kính bậc lõm vành đĩa xích ds
        self.ds = (self.p / math.tan(math.radians(self.alpha_deg / 2.0))) - self.g - (2.0 * self.r4)
        self.Rs = self.ds / 2.0

        # 6. Góc mở rãnh răng beta & Góc sườn răng gamma
        if self.standard == 'KWN_017':
            if 6 <= self.z <= 11:
                self.beta_deg = 74.0
            elif 12 <= self.z <= 29:
                self.beta_deg = 56.0
            else:
                self.beta_deg = 38.0
            self.gamma_deg = (self.beta_deg / 2.0) - (180.0 / self.z)
        else: # KWN_015
            if self.gamma_override is not None:
                self.gamma_deg = float(self.gamma_override)
            else:
                # Giá trị mẫu tính toán tối ưu theo tải trọng
                self.gamma_deg = 14.5
            self.beta_deg = (self.alpha_deg / 2.0 + self.gamma_deg) * 2.0

        self.beta_rad = math.radians(self.beta_deg)
        self.half_beta = self.beta_rad / 2.0

        # 7. Các kích thước biên dạng hốc răng
        self.r1 = 0.51 * self.d1           # Bán kính đáy rãnh
        self.u = 0.02 * self.p             # Khe hở đáy rãnh
        self.h3 = 0.3 * self.d1            # Chiều dài đoạn thẳng sườn răng
        self.r2 = 0.8 * self.p             # Bán kính cong sườn răng
        self.B1 = 0.9 * self.b1            # Chiều rộng răng đĩa xích

    def compute_single_gap_half(self, num_arc_pts=20):
        """
        Tính tọa độ nửa phải của một rãnh răng (trục đối xứng là trục +Y)
        Gồm:
        - Đáy phẳng từ x = 0 đến x = u/2 tại y = Rf
        - Cung r1 từ (u/2, Rf) đến P1
        - Đoạn thẳng h3 từ P1 đến P2
        - Cung r2 từ P2 đến P3 (cắt vòng đỉnh Ra)
        """
        pts = [(0.0, self.Rf), (self.u / 2.0, self.Rf)]

        # Tâm cung r1
        C1 = (self.u / 2.0, self.Rf + self.r1)
        theta_end = math.pi / 2.0 - self.half_beta

        for i in range(1, num_arc_pts + 1):
            theta = theta_end * (i / num_arc_pts)
            x = C1[0] + self.r1 * math.sin(theta)
            y = C1[1] - self.r1 * math.cos(theta)
            pts.append((x, y))

        P1 = pts[-1]
        T = (math.sin(self.half_beta), math.cos(self.half_beta))
        P2 = (P1[0] + self.h3 * T[0], P1[1] + self.h3 * T[1])
        pts.append(P2)

        # Cung r2: Tâm C2 nằm về phía thân răng
        N_right = (math.cos(self.half_beta), -math.sin(self.half_beta))
        C2 = (P2[0] + self.r2 * N_right[0], P2[1] + self.r2 * N_right[1])

        # Giao điểm của đường tròn (C2, r2) và (O, Ra)
        d = math.hypot(C2[0], C2[1])
        a_len = (self.Ra**2 - self.r2**2 + d**2) / (2.0 * d)
        h_len = math.sqrt(max(0.0, self.Ra**2 - a_len**2))
        x_base = a_len * C2[0] / d
        y_base = a_len * C2[1] / d
        int1 = (x_base + h_len * (-C2[1]) / d, y_base + h_len * C2[0] / d)
        int2 = (x_base - h_len * (-C2[1]) / d, y_base - h_len * C2[0] / d)

        # Chọn giao điểm gần P2 hơn
        d1_sq = (int1[0] - P2[0])**2 + (int1[1] - P2[1])**2
        d2_sq = (int2[0] - P2[0])**2 + (int2[1] - P2[1])**2
        P3 = int1 if d1_sq < d2_sq else int2

        th_start = math.atan2(P2[1] - C2[1], P2[0] - C2[0])
        th_end = math.atan2(P3[1] - C2[1], P3[0] - C2[0])

        for i in range(1, num_arc_pts + 1):
            ang = th_start + (th_end - th_start) * (i / num_arc_pts)
            pts.append((C2[0] + self.r2 * math.cos(ang), C2[1] + self.r2 * math.sin(ang)))

        # Góc của P3 tính từ trục +Y (theo chiều kim đồng hồ)
        tip_angle = math.atan2(P3[0], P3[1])

        P0_info = (P1, P2, P3, C1, C2)
        return pts, P0_info, tip_angle

    def generate_full_contour(self, num_arc_pts=15):
        """
        Dựng toàn bộ đường bao khép kín 360 độ của đĩa xích z răng
        """
        right_half, _, tip_ang_right = self.compute_single_gap_half(num_arc_pts)

        # Lấy nửa trái bằng cách lấy đối xứng qua trục Y (x -> -x) và đảo ngược thứ tự
        left_half = [(-x, y) for (x, y) in reversed(right_half[1:])]
        single_gap = left_half + right_half

        # Góc nửa bước răng
        half_pitch = self.alpha_rad / 2.0

        full_profile = []

        for k in range(self.z):
            gap_center_angle = k * self.alpha_rad

            # Xoay các điểm của rãnh răng thứ k
            cos_g = math.cos(gap_center_angle)
            sin_g = math.sin(gap_center_angle)

            # Rãnh răng k
            for (gx, gy) in single_gap:
                rx = gx * cos_g + gy * sin_g
                ry = -gx * sin_g + gy * cos_g
                full_profile.append((rx, ry))

            # Đoạn cung đỉnh răng nối từ rãnh k sang rãnh k+1
            # Góc bắt đầu tại đỉnh răng: gap_center_angle + tip_ang_right
            # Góc kết thúc: gap_center_angle + alpha_rad - tip_ang_right
            ang_start = gap_center_angle + tip_ang_right
            ang_end = gap_center_angle + self.alpha_rad - tip_ang_right

            tip_steps = max(3, int(num_arc_pts / 2))
            for i in range(1, tip_steps):
                cur_ang = ang_start + (ang_end - ang_start) * (i / tip_steps)
                # Điểm trên vòng tròn đỉnh Ra (tính từ trục +Y)
                tx = self.Ra * math.sin(cur_ang)
                ty = self.Ra * math.cos(cur_ang)
                full_profile.append((tx, ty))

        return full_profile

    def export_dxf(self, filename="sprocket_profile.dxf"):
        """
        Xuất file DXF chuyên nghiệp chuẩn AutoCAD / SolidWorks
        """
        doc = ezdxf.new('R2010')
        doc.units = units.MM
        msp = doc.modelspace()

        # Tạo các Layer kỹ thuật theo tiêu chuẩn CAD
        doc.layers.add('SPROCKET_CONTOUR', color=ezdxf.colors.GREEN) # Đường bao răng
        doc.layers.add('PITCH_CIRCLE', color=ezdxf.colors.CYAN, linetype='CENTER') # Vòng chia
        doc.layers.add('ROOT_CIRCLE', color=ezdxf.colors.RED, linetype='DASHED') # Vòng chân răng
        doc.layers.add('TIP_CIRCLE', color=ezdxf.colors.MAGENTA, linetype='PHANTOM') # Vòng đỉnh răng
        doc.layers.add('RECESS_CIRCLE', color=ezdxf.colors.YELLOW, linetype='DASHDOT') # Bậc lõm vành
        doc.layers.add('CENTER_BORE', color=ezdxf.colors.WHITE) # Lỗ trục & rãnh then
        doc.layers.add('CENTER_LINES', color=ezdxf.colors.CYAN, linetype='CENTER') # Trục tâm

        # 1. Vẽ đường bao răng khép kín (LWPOLYLINE)
        contour_pts = self.generate_full_contour(num_arc_pts=16)
        poly = msp.add_lwpolyline(contour_pts, close=True, dxfattribs={'layer': 'SPROCKET_CONTOUR', 'color': 3})

        # 2. Vẽ các đường tròn cơ sở
        msp.add_circle((0, 0), self.R0, dxfattribs={'layer': 'PITCH_CIRCLE', 'color': 4})
        msp.add_circle((0, 0), self.Rf, dxfattribs={'layer': 'ROOT_CIRCLE', 'color': 1})
        msp.add_circle((0, 0), self.Ra, dxfattribs={'layer': 'TIP_CIRCLE', 'color': 6})
        if self.Rs > 0:
            msp.add_circle((0, 0), self.Rs, dxfattribs={'layer': 'RECESS_CIRCLE', 'color': 2})

        # 3. Vẽ lỗ trục & rãnh then DIN 6885
        r_bore = self.bore_dia / 2.0
        if r_bore > 0:
            if self.key_width > 0 and self.key_depth > 0:
                # Dựng biên dạng lỗ trục có rãnh then
                kw2 = self.key_width / 2.0
                y_key = r_bore + self.key_depth
                # Giao điểm của x = +/- kw2 với đường tròn r_bore
                if r_bore > kw2:
                    y_circ = math.sqrt(r_bore**2 - kw2**2)
                    key_pts = [
                        (-kw2, y_circ),
                        (-kw2, y_key),
                        (kw2, y_key),
                        (kw2, y_circ)
                    ]
                    # Vẽ cung tròn lỗ từ angle(kw2, y_circ) vòng xuống dưới tới angle(-kw2, y_circ)
                    ang_end_deg = math.degrees(math.atan2(y_circ, kw2))
                    ang_start_deg = math.degrees(math.atan2(y_circ, -kw2))
                    # Arc đi ngược chiều kim đồng hồ
                    msp.add_arc((0, 0), r_bore, start_angle=ang_end_deg, end_angle=ang_start_deg,
                                dxfattribs={'layer': 'CENTER_BORE', 'color': 7})
                    msp.add_lwpolyline(key_pts, close=False, dxfattribs={'layer': 'CENTER_BORE', 'color': 7})
                else:
                    msp.add_circle((0, 0), r_bore, dxfattribs={'layer': 'CENTER_BORE', 'color': 7})
            else:
                msp.add_circle((0, 0), r_bore, dxfattribs={'layer': 'CENTER_BORE', 'color': 7})

        # 4. Trục đối xứng chữ thập
        L_axis = self.Ra * 1.15
        msp.add_line((-L_axis, 0), (L_axis, 0), dxfattribs={'layer': 'CENTER_LINES', 'color': 4})
        msp.add_line((0, -L_axis), (0, L_axis), dxfattribs={'layer': 'CENTER_LINES', 'color': 4})

        doc.saveas(filename)
        print(f"[OK] Đã xuất file CAD DXF: {filename}")
        return filename

    def export_svg(self, filename="sprocket_profile.svg"):
        """
        Xuất file SVG chuẩn vector hiển thị trực tiếp trên trình duyệt
        """
        contour_pts = self.generate_full_contour(num_arc_pts=16)
        
        # Viewbox padding
        pad = self.Ra * 0.15
        size = (self.Ra + pad) * 2.0
        v_min = -(self.Ra + pad)
        
        svg = []
        svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{v_min} {v_min} {size} {size}" width="100%" height="100%">')
        svg.append('  <defs>')
        svg.append('    <style>')
        svg.append('      .sprocket-body { fill: #1e293b; stroke: #38bdf8; stroke-width: 2.5; stroke-linejoin: round; }')
        svg.append('      .circle-ref { fill: none; stroke-width: 1.2; }')
        svg.append('      .d0 { stroke: #0284c7; stroke-dasharray: 8,4; }')
        svg.append('      .df { stroke: #ef4444; stroke-dasharray: 4,4; }')
        svg.append('      .da { stroke: #a855f7; stroke-dasharray: 6,4; }')
        svg.append('      .ds { stroke: #eab308; stroke-dasharray: 4,2; }')
        svg.append('      .axis { stroke: #64748b; stroke-width: 1; stroke-dasharray: 10,5; }')
        svg.append('      .bore { fill: #0f172a; stroke: #f8fafc; stroke-width: 2; }')
        svg.append('    </style>')
        svg.append('  </defs>')

        # Vẽ các trục tâm
        L = self.Ra * 1.1
        svg.append(f'  <line x1="{-L}" y1="0" x2="{L}" y2="0" class="axis" />')
        svg.append(f'  <line x1="0" y1="{-L}" x2="0" y2="{L}" class="axis" />')

        # Vẽ các đường tròn tham chiếu
        svg.append(f'  <circle cx="0" cy="0" r="{self.Rf}" class="circle-ref df" />')
        svg.append(f'  <circle cx="0" cy="0" r="{self.R0}" class="circle-ref d0" />')
        svg.append(f'  <circle cx="0" cy="0" r="{self.Ra}" class="circle-ref da" />')
        if self.Rs > 0:
            svg.append(f'  <circle cx="0" cy="0" r="{self.Rs}" class="circle-ref ds" />')

        # Path đường bao đĩa xích
        d_path = ["M " + f"{contour_pts[0][0]:.3f} {-contour_pts[0][1]:.3f}"]
        for pt in contour_pts[1:]:
            d_path.append(f"L {pt[0]:.3f} {-pt[1]:.3f}")
        d_path.append("Z")
        svg.append(f'  <path d="{" ".join(d_path)}" class="sprocket-body" />')

        # Lỗ trục
        r_bore = self.bore_dia / 2.0
        if r_bore > 0:
            svg.append(f'  <circle cx="0" cy="0" r="{r_bore}" class="bore" />')

        svg.append('</svg>')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(svg))
        print(f"[OK] Đã xuất file SVG: {filename}")
        return filename

    def print_report(self):
        print("="*70)
        print(" BẢNG THÔNG SỐ HÌNH HỌC ĐĨA XÍCH KETTENWULF (KWN 017 / KWN 015)")
        print("="*70)
        print(f"  Tiêu chuẩn thiết kế:               {self.standard}")
        print(f"  Bước xích (p):                     {self.p:.2f} mm")
        print(f"  Số răng (z):                       {self.z} răng")
        print(f"  Đường kính con lăn / bạc (d1):     {self.d1:.2f} mm")
        print(f"  Bề rộng trong mắt xích (b1):       {self.b1:.2f} mm")
        print(f"  Chiều cao má xích (g):             {self.g:.2f} mm")
        print(f"  Cấu hình xích:                     {self.chain_type}")
        print("-"*70)
        print(f"  Góc bước răng (alpha):             {self.alpha_deg:.2f}°")
        print(f"  Góc mở rãnh răng (beta):           {self.beta_deg:.2f}°")
        print(f"  Góc sườn răng (gamma):             {self.gamma_deg:.2f}°")
        print(f"  Đường kính vòng chia (d0):         {self.d0:.2f} mm (R0 = {self.R0:.2f} mm)")
        print(f"  Đường kính vòng chân răng (df):    {self.df:.2f} mm (Rf = {self.Rf:.2f} mm) [dung sai h11]")
        print(f"  Đường kính vòng đỉnh răng (da):    {self.da:.2f} mm (Ra = {self.Ra:.2f} mm)")
        print(f"  Đường kính bậc lõm vành (ds):      {self.ds:.2f} mm (Rs = {self.Rs:.2f} mm)")
        print(f"  Bề rộng răng làm việc (B1):        {self.B1:.2f} mm")
        print(f"  Bán kính đáy rãnh (r1):            {self.r1:.2f} mm")
        print(f"  Khe hở rãnh răng (u):              {self.u:.2f} mm")
        print(f"  Chiều dài đoạn thẳng sườn (h3):    {self.h3:.2f} mm")
        print(f"  Bán kính sườn răng trên (r2):      {self.r2:.2f} mm")
        print(f"  Bán kính lượn chân vành (r4):      {self.r4:.2f} mm")
        print(f"  Đường kính trục (dw):              {self.bore_dia:.2f} mm")
        print("="*70)


if __name__ == '__main__':
    # Chạy kiểm chứng Test Case MT 630 / MT 900 (p=400, z=8, d1=68, b1=66, g=90)
    sprocket = KettenWulfSprocket(
        p=400.0,
        z=8,
        d1=68.0,
        b1=66.0,
        g=90.0,
        r4=5.0,
        chain_type='without_roller',
        standard='KWN_017',
        bore_dia=120.0,
        key_width=32.0,
        key_depth=11.0
    )
    sprocket.print_report()
    sprocket.export_dxf("dia_xich_KWN017_p400_z8.dxf")
    sprocket.export_svg("dia_xich_KWN017_p400_z8.svg")
