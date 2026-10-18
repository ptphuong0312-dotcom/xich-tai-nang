# BẢN ĐẶC TẢ CHI TIẾT CÁC TIÊU CHUẨN BIÊN DẠNG RĂNG KETTENWULF
*(KettenWulf Tooth Profile Standards Specification: KWN 017, KWN 015, KWN 001, KWN 016)*

> **Nguồn trích xuất**: Trang 46, 47, 48, 49 Catalog KettenWulf `kettenwulf-conveyor-chains-and-sprockets.pdf`.

---

## 1. BẢNG SO SÁNH TỔNG QUAN GIỮA CÁC TIÊU CHUẨN

| Tiêu chuẩn | Mục đích áp dụng | Dòng xích tương thích | Điểm nhận dạng hình học | Cơ chế góc mở $\beta$ & góc sườn $\gamma$ |
| :--- | :--- | :--- | :--- | :--- |
| **KWN 017** | Xích tải cào tiêu chuẩn công nghiệp | MT, FVT, M, FV, MC | Hốc răng phẳng có đoạn vát $h_3$, hở đáy $u$ | $\beta$ tra cứu tự động theo $z$ ($74^\circ, 56^\circ, 38^\circ$); $\gamma = \frac{\beta - \alpha}{2}$ |
| **KWN 015** | Xích tải nặng / hạt liệu dễ chèn kẹt hốc răng | MT, FVT, M, FV, MC | Hốc răng rất sâu, vát thoát liệu mạnh | $\gamma$ tùy biến theo kỹ sư; $\beta = \alpha + 2\gamma$ |
| **KWN 001** | Xích con lăn truyền động cơ khí | DIN 8187 (06B đến 32B), ANSI | Đáy tròn ôm sát con lăn $X^\circ$, sườn cong lồi $r_2$ | Không có góc $\beta$ phẳng; ôm con lăn với góc $X$ ($115^\circ, 120^\circ, 125^\circ$) |
| **KWN 016** | Đĩa chốt lồng đèn (Lantern Pinion) | Xích thanh chốt đặc biệt | Răng dạng chấu ôm con lăn, chia theo modun | Ăn khớp modun $m = p/\pi$, biên dạng chốt |

---

## 2. TIÊU CHUẨN KWN 017 – TIÊU CHUẨN XÍCH TẢI CÀO CÔNG NGHIỆP
*(Standard Toothing for Bush Conveyor Chains – Trang 48)*

### 2.1. Bản chất hình học và cơ chế tiếp xúc
KWN 017 là tiêu chuẩn xương sống của KettenWulf cho các dây chuyền gầu nâng, xích cào than, xích cào clinker xi măng.
Biên dạng hốc răng được ghép từ 3 phần tử hình học chính:
1. **Đáy hốc răng tròn (Roller Bed)**: Cung tròn bán kính $r_1 = 0.51 \cdot d_1$, tâm đặt trên đường tròn chia $d_0$.
2. **Khe hở song song đáy hốc (Tooth Gap Clearance $u$)**: Đoạn thẳng dịch chuyển ngang đáy $u = 0.02 \cdot p$ để chống kẹt bụi và bù giãn nở nhiệt.
3. **Đoạn sườn răng phẳng tiếp xúc (Flank Flat Segment $h_3$)**: Chiều dài $h_3 = 0.3 \cdot d_1$, nghiêng một góc $\beta/2$ so với trục hốc răng. Đoạn này là mặt chịu lực chính khi xích kéo đĩa.
4. **Cung lượn đỉnh răng (Flank Blend Arc $r_2$)**: Cung tròn bán kính $r_2 = 0.8 \cdot p$ vuốt tiếp tuyến từ mút của $h_3$ lên đến đường tròn đỉnh $d_a$.

### 2.2. Bảng phân vùng góc mở hốc răng $\beta$
KettenWulf chuẩn hóa góc mở $\beta$ thành 3 khoảng phân vùng theo số răng đĩa xích $z$:
- **$z = 6 \div 11$ răng**: $\beta = \mathbf{74.0^\circ}$
  - Ví dụ $z = 8 \implies \alpha = 45^\circ \implies \gamma = \frac{74^\circ - 45^\circ}{2} = \mathbf{14.50^\circ}$.
- **$z = 12 \div 29$ răng**: $\beta = \mathbf{56.0^\circ}$
  - Ví dụ $z = 12 \implies \alpha = 30^\circ \implies \gamma = \frac{56^\circ - 30^\circ}{2} = \mathbf{13.00^\circ}$.
- **$z \ge 30$ răng**: $\beta = \mathbf{38.0^\circ}$
  - Ví dụ $z = 36 \implies \alpha = 10^\circ \implies \gamma = \frac{38^\circ - 10^\circ}{2} = \mathbf{14.00^\circ}$.

### 2.3. Đường dóng kích thước kỹ thuật chuẩn của $\gamma$
Đường dóng góc sườn $\gamma$ được đo giữa:
- **Đường nét đứt kéo dài của sườn răng $h_3$** (chính là đường định vị góc $\beta$).
- **Đường tâm giữa thân răng** (trục đối xứng hướng tâm của răng đĩa xích).
- Hai đường này giao nhau tại điểm đỉnh Apex ($I_{apex}$). Cung đo góc và giá trị góc $\gamma$ được neo trực tiếp tại Apex này, không dùng đường dóng hướng tâm phụ làm rối mắt.

---

## 3. TIÊU CHUẨN KWN 015 – HỐC RĂNG SÂU TỐI ƯU LỰC
*(Deep Tooth Gap Toothing for Conveyor Chains – Trang 47)*

### 3.1. Sự khác biệt với KWN 017
- Trong KWN 017, góc mở $\beta$ bị ghim cứng theo bảng 3 nấc ($74^\circ, 56^\circ, 38^\circ$), do đó góc $\gamma$ phụ thuộc vào số răng $z$.
- Trong KWN 015, người kỹ sư có toàn quyền điều chỉnh **Góc sườn $\gamma$** (từ $10^\circ$ đến $25^\circ$) để:
  - Tăng độ nghiêng sườn nhằm nhả xích nhanh, tránh dính bết than bùn/quặng ẩm.
  - Phân bổ vector áp lực vuông góc với sườn răng để triệt tiêu tải trọng uốn má xích.
- Công thức tính góc mở $\beta$:
$$\beta = \left(\frac{\alpha}{2} + \gamma\right) \cdot 2 = \alpha + 2\gamma$$

---

## 4. TIÊU CHUẨN KWN 001 – ĐĨA XÍCH CON LĂN TRUYỀN ĐỘNG
*(Sprockets for Roller Chains DIN 8187 / ISO 606 – Trang 46)*

### 4.1. Đặc trưng hình học
- Không có đoạn sườn phẳng $h_3$ hay khe hở đáy $u$.
- Đáy hốc ôm sát con lăn theo cung tròn bán kính $r_1$:
$$r_1 = 0.505 \cdot d_1 + 0.069 \cdot \sqrt[3]{d_1}$$
- Cung sườn răng $r_2$ nối tiếp từ góc ôm đáy $X^\circ$:
$$r_2 = 0.008 \cdot d_1 \cdot (z_1^2 + 180)$$
Trong đó hệ số răng $z_1$ và góc ôm đáy $X$:
- $z \le 6$: $z_1 = 6, X = 115^\circ$
- $z = 7 \div 12$: $z_1 = 8, X = 120^\circ$
- $z \ge 13$: $z_1 = 12, X = 125^\circ$

### 4.2. Giải pháp chống va chạm con lăn ở số răng nhỏ ($z \le 8$)
Khi $z$ nhỏ ($z \le 8$), góc ngoặt giữa 2 bước xích là $\alpha \ge 45^\circ$. Nếu tâm $C_2$ không đặt đúng hướng vào thân răng hoặc đường kính đỉnh $d_a$ quá cao, mép đỉnh răng sẽ đâm thủng con lăn khi con lăn hạ cánh vào hốc.
- Hiệu chỉnh đỉnh răng chuẩn KettenWulf: $d_a = d_0 + 0.50 \cdot d_1$ (cho $z \le 8$).
- Cung sườn cong lồi vào thân răng đảm bảo tiếp tuyến êm dịu, khe hở động học khi vào khớp luôn dương $> 0.3\text{ mm}$.
