# ĐẶC TẢ KỸ THUẬT XUẤT BẢN VẼ AUTOCAD DXF
*(AutoCAD DXF R12 Technical Specification & Standards)*

> **Phiên bản DXF**: AutoCAD Release 12 (AC1009) – Định dạng tương thích 100% với mọi phần mềm CAD (AutoCAD, SolidWorks, Inventor, BricsCAD, DraftSight, LibreCAD, máy cắt CNC Plasma/Laser/Waterjet).

---

## 1. NGUYÊN TẮC MÃ HÓA KÝ TỰ & FONT CHỮ (CHARACTER ENCODING)

AutoCAD AC1009 sử dụng bảng mã ANSI (Code Page 1252), không hỗ trợ các ký tự Unicode nhiều byte (như $\varnothing$, $^\circ$, $\gamma$, $\beta$, $\alpha$). Nếu xuất trực tiếp chuỗi Unicode, AutoCAD sẽ hiển thị dấu hỏi chấm `?` hoặc lỗi font.

### Bảng chuyển đổi ký tự chuẩn:
| Ý nghĩa | Ký tự Unicode hiển thị Web | Mã lệnh thoát AutoCAD chuẩn | Kết quả hiển thị trong CAD |
| :--- | :---: | :---: | :---: |
| Ký hiệu Đường kính | $\varnothing$ | `%%c` | Biểu tượng $\varnothing$ chuẩn kỹ thuật |
| Ký hiệu Độ | $^\circ$ | `%%d` | Biểu tượng độ $^\circ$ chuẩn |
| Ký hiệu Dung sai cộng/trừ | $\pm$ | `%%p` | Biểu tượng $\pm$ chuẩn |
| Góc sườn | $\gamma$ | `gamma` | Chữ cái La-tinh rõ nghĩa |
| Góc mở hốc răng | $\beta$ | `beta` | Chữ cái La-tinh rõ nghĩa |
| Góc phân chia răng | $\alpha$ | `alpha` | Chữ cái La-tinh rõ nghĩa |

---

## 2. QUY CHUẨN CẤU TRÚC LỚP (LAYERS) VÀ MÀU SẮC (ACI COLORS)

| Tên Layer | Màu ACI | Mã màu | Ý nghĩa đối tượng | Loại nét |
| :--- | :---: | :---: | :--- | :--- |
| `SPROCKET_OUTLINE` | 7 | White/Black | Biên dạng vành răng đĩa xích khép kín (CNC Polyline) | Continuous (0.35mm) |
| `SPROCKET_HOLE_KEY` | 3 | Green | Lỗ trục và rãnh then chuẩn DIN 6885 | Continuous (0.35mm) |
| `SPROCKET_CENTERLINE`| 1 | Red | Trục tâm đĩa xích và trục đối xứng hốc răng | CENTER / Dashed (0.18mm) |
| `SPROCKET_REF_CIRCLES`| 8 | Dark Gray | Các vòng tròn cơ sở kỹ thuật ($d_0, d_f, d_a, d_s$) | DASHED / Continuous (0.18mm) |
| `SPROCKET_DIMS` | 4 | Cyan | Kích thước CAD, mũi tên dóng, trị số đường kính | Continuous (0.18mm) |
| `CHAIN_LINKS_OUTER` | 5 | Blue | Má xích ngoài (Outer link plates) | Continuous (0.25mm) |
| `CHAIN_LINKS_INNER` | 2 | Yellow | Má xích trong (Inner link plates) | Continuous (0.25mm) |
| `CHAIN_PINS_ROLLERS` | 4 | Cyan | Chốt xích, ống lót và con lăn | Continuous (0.25mm) |
| `TITLE_BLOCK` | 7 | White | Khung bản vẽ và khung tên kỹ thuật theo TCVN / ISO | Continuous (0.50mm & 0.25mm) |

---

## 3. CÁC CHẾ ĐỘ XUẤT BẢN VẼ DXF (5 EXPORT MODES)

### 3.1. Chế độ 1: Bản vẽ riêng đĩa xích (`sprocket_only`)
- Chỉ xuất duy nhất đĩa xích cơ khí (không có dải xích/má xích đi kèm).
- Dành cho bộ phận gia công phay/cắt dây CNC: Biên dạng răng khép kín (closed contour), lỗ trục then, 4 vòng cơ sở $d_0, d_f, d_a, d_s$, trục tâm dấu cộng.
- Kích thước đo đạc kỹ thuật: $\varnothing d_0, \varnothing d_f\text{ (h11)}, \varnothing d_a, \varnothing d_s, \varnothing d_w, \text{rãnh then } b \times t_2$.

### 3.2. Chế độ 2: Bản vẽ lắp đĩa xích & xích ăn khớp (`chain_assembly`)
- Thể hiện nguyên vẹn trạng thái động học đĩa xích đang ăn khớp với dải xích tải cào (2 nhánh xích trên và dưới nằm ngang, 4 bước xích ôm trọn vành răng đĩa).
- Phân biệt rõ ràng má xích ngoài, má xích trong, chốt xích và con lăn bằng các layer riêng biệt.

### 3.3. Chế độ 3: Chi tiết hốc răng (Trích phóng to Macro) (`gap_macro`)
- Trích phóng to 1 hốc răng đĩa xích kèm theo **phần thân vành đĩa xích** (sector body đặc trưng).
- Thể hiện chi tiết các yếu tố hình học hốc răng:
  - Bán kính đáy hốc $r_1$
  - Bán kính đỉnh sườn $r_2$
  - Đoạn sườn phẳng tiếp xúc $h_3$
  - Độ hở đáy $u$
  - Góc mở rãnh răng $\beta$
  - **Góc sườn $\gamma$**: Dóng trực tiếp giữa đường sườn nét đứt (định vị $\beta$) và đường tâm giữa thân răng tại điểm đỉnh giao nhau ($I_{apex}$).

### 3.4. Chế độ 4: Mặt cắt ngang thân răng (`section_profile`)
- Thể hiện mặt cắt dọc trục qua thân răng đĩa xích:
  - Bề rộng vành răng $B_1$
  - Chiều cao đỉnh răng
  - Góc vát đỉnh răng $b_a$ và bán kính vê góc $r_x$
  - Mặt cắt lỗ trục $d_w$, then $t_2$ và chiều dài may-ơ $NL$.

### 3.5. Chế độ 5: Xuất TỔNG HỢP toàn bộ trong 1 bản vẽ + Khung tên (`combined_sheet`)
- Kết hợp toàn bộ 3 khung nhìn trên cùng 1 trang vẽ kỹ thuật:
  - **Hình 1**: Bản vẽ lắp đĩa xích và dải xích tải tại tọa độ gốc $(0, 0)$.
  - **Hình 2**: Trích phóng to chi tiết hốc răng, đặt tại tọa độ an toàn bên phải:  
    $$X_{gap} > R_0 + 5.5 \cdot p + 1.3 \cdot R_a, \quad Y_{gap} = 1.1 \cdot R_a$$
  - **Hình 3**: Mặt cắt ngang thân răng và may-ơ, đặt tại:  
    $$X_{sec} > R_0 + 5.5 \cdot p + 1.3 \cdot R_a, \quad Y_{sec} = -1.1 \cdot R_a$$
  - **Khung bản vẽ & Khung tên kỹ thuật chuẩn**: Đóng khung bao quanh toàn bộ các hình biểu diễn, ghi rõ Tên chi tiết, Tiêu chuẩn (KWN 017 / 015 / 001), Mã xích, Bước xích $p$, Số răng $z$, Vật liệu, Tỷ lệ và Ngày xuất.
