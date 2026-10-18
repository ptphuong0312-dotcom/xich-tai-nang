# SỔ TAY KỸ THUẬT XÍCH TẢI VÀ ĐĨA XÍCH KETTENWULF
*(KettenWulf Conveyor Chains & Sprockets Engineering Master Handbook)*

> **Tài liệu nguồn gốc**: `kettenwulf-conveyor-chains-and-sprockets.pdf` (Catalog chính hãng KettenWulf 92 trang).  
> **Mục đích**: Là nguồn dữ liệu chuẩn mực duy nhất (Single Source of Truth - SSOT) cho toàn bộ hệ thống tính toán, mô phỏng động học và xuất bản vẽ CAD/DXF của dự án. Không cần mở lại file PDF gốc.

---

## MỤC LỤC
1. [Tổng Quan Về Xích Tải & Đĩa Xích KettenWulf](#1-tổng-quan-về-xích-tải--đĩa-xích-kettenwulf)
2. [Động Học & Hiệu Ứng Đa Giác (Polygon Effect)](#2-động-học--hiệu-ứng-đa-giác-polygon-effect)
3. [Động Lực Học & Tính Toán Lực Kéo Xích](#3-động-lực-học--tính-toán-lực-kéo-xích)
4. [Các Tiêu Chuẩn Biên Dạng Hốc Răng Đĩa Xích (Toothing Standards)](#4-các-tiêu-chuẩn-biên-dạng-hốc-răng-đĩa-xích-toothing-standards)
   - 4.1. [KWN 017 – Tiêu chuẩn xích tải cào (ISO 1977 & DIN 8167 / DIN 8165)](#41-kwn-017--tiêu-chuẩn-xích-tải-cào)
   - 4.2. [KWN 015 – Tiêu chuẩn hốc răng sâu tối ưu lực phân bố](#42-kwn-015--tiêu-chuẩn-hốc-răng-sâu-tối-ưu-lực)
   - 4.3. [KWN 001 – Tiêu chuẩn đĩa xích con lăn truyền động (DIN 8187 / ISO 606)](#43-kwn-001--tiêu-chuẩn-đĩa-xích-con-lăn-truyền-động)
   - 4.4. [KWN 016 – Tiêu chuẩn đĩa chốt lồng đèn (Lantern Pinion)](#44-kwn-016--tiêu-chuẩn-đĩa-chốt-lồng-đèn)
5. [Tính Toán Trục, May-ơ & Then DIN 6885](#5-tính-toán-trục-may-ơ--then-din-6885)
6. [Các Dạng Kết Cấu Đĩa Xích](#6-các-dạng-kết-cấu-đĩa-xích)
7. [Bảng Kích Thước Hình Học Chuẩn Của Các Dòng Xích](#7-bảng-kích-thước-hình-học-chuẩn-của-các-dòng-xích)
8. [Quy Chuẩn Dung Sai & Chế Tạo](#8-quy-chuẩn-dung-sai--chế-tạo)

---

## 1. TỔNG QUAN VỀ XÍCH TẢI & ĐĨA XÍCH KETTENWULF

KettenWulf là nhà sản xuất hàng đầu thế giới về xích tải nặng công nghiệp (conveyor chains) và đĩa xích (sprockets). Các dòng xích tải công nghiệp chủ yếu bao gồm:
- **Xích cào má sâu (Deep-link scraper chains)**: Dòng **MT** (tiêu chuẩn ISO 1977 / DIN 8167) và dòng **FVT** (tiêu chuẩn DIN 8165). Má xích nhô cao để trực tiếp cào vật liệu hạt rời, than đá, xi măng, khoáng sản.
- **Xích tải má phẳng tiêu chuẩn (Standard conveyor chains)**: Dòng **M** (ISO 1977 / DIN 8167) và dòng **FV** (DIN 8165).
- **Xích chốt rỗng (Hollow pin conveyor chains)**: Dòng **MC** (DIN 8168), cho phép luồn các thanh xà ngang liên kết giữa 2 dải xích song song.
- **Xích con lăn truyền động (Drive roller chains)**: Dòng **DIN 8187 / ISO 606** (hệ châu Âu, ký hiệu B) và **ANSI / DIN 8188** (hệ Mỹ, ký hiệu A).

---

## 2. ĐỘNG HỌC & HIỆU ỨNG ĐA GIÁC (POLYGON EFFECT)
*(Tham chiếu Catalog Trang 6 - 8)*

Khi xích ăn khớp với đĩa xích, các chốt xích nằm trên vòng tròn chia đường kính $d_0$, nhưng các má xích là các đoạn thẳng cứng có bước $p$. Do đó, xích quấn quanh đĩa xích tạo thành một hình đa giác đều $z$ cạnh.

### 2.1. Góc phân chia răng $\alpha$ (Pitch Angle)
$$\alpha = \frac{360^\circ}{z} \quad (\text{radian: } \omega = \frac{2\pi}{z})$$

### 2.2. Đường kính vòng chia $d_0$ (Pitch Circle Diameter)
$$d_0 = \frac{p}{\sin\left(\frac{180^\circ}{z}\right)}$$
Bán kính vòng chia: $R_0 = \frac{d_0}{2} = \frac{p}{2 \cdot \sin(\alpha / 2)}$.

### 2.3. Bán kính hiệu dụng cực tiểu $R_{\min}$
Khi đĩa xích quay một góc $\alpha / 2$, tiếp điểm giữa dải xích căng và đĩa xích hạ xuống vị trí thấp nhất:
$$R_{\min} = R_0 \cdot \cos\left(\frac{\alpha}{2}\right) = \frac{p}{2 \cdot \tan(\alpha / 2)}$$

### 2.4. Độ dao động vận tốc xích do hiệu ứng đa giác ($\Delta v$)
Vận tốc tức thời của xích biến thiên liên tục tuần hoàn:
- Vận tốc lớn nhất: $v_{\max} = R_0 \cdot \omega$
- Vận tốc nhỏ nhất: $v_{\min} = R_{\min} \cdot \omega = R_0 \cdot \cos(\alpha / 2) \cdot \omega$
- Tỉ số biến thiên vận tốc:
$$\frac{\Delta v}{v_{\max}} = 1 - \cos\left(\frac{180^\circ}{z}\right)$$
> [!NOTE]
> Khi số răng $z$ càng nhỏ, hiệu ứng đa giác càng lớn, gây ra va đập, gia tốc giật và rung lắc dải xích. KettenWulf khuyến cáo:
> - $z \ge 8$ đối với xích cào tải nặng tốc độ thấp.
> - $z \ge 17$ đối với truyền động xích con lăn tốc độ trung bình và cao.

---

## 3. ĐỘNG LỰC HỌC & TÍNH TOÁN LỰC KÉO XÍCH
*(Tham chiếu Catalog Trang 10 - 25)*

### 3.1. Lực kéo tổng cộng trên xích ($F$)
$$F = F_{mat} + F_{chain} + F_{fric}$$
Trong đó:
- $F_{mat}$: Lực nâng hoặc kéo vật liệu vận chuyển.
- $F_{chain}$: Trọng lượng bản thân nhánh xích kéo.
- $F_{fric}$: Lực ma sát (ma sát trượt giữa má xích và ray dẫn hướng, hoặc ma sát lăn của con lăn $\mu = 0.05 \div 0.15$).

### 3.2. Kiểm tra áp suất khớp bản lề xích (Bearing Area Pressure $p_B$)
$$p_B = \frac{F}{A_B} \le [p_{perm}]$$
Trong đó:
- $A_B = d_1 \cdot b_{bush}$: Diện tích tiếp xúc hình chiếu giữa chốt trong và ống lót.
- $[p_{perm}]$: Áp suất cho phép của KettenWulf theo vật liệu (thường từ $2000 \div 3000\text{ N/cm}^2$).

### 3.3. Hệ số an toàn kéo đứt ($\nu$)
$$\nu = \frac{F_B}{F} \ge 6 \div 10$$
Với $F_B$ là tải trọng phá hủy tối thiểu (Breaking Load) của dòng xích trong Catalog.

---

## 4. CÁC TIÊU CHUẨN BIÊN DẠNG HỐC RĂNG ĐĨA XÍCH (TOOTHING STANDARDS)

### 4.1. KWN 017 – Tiêu chuẩn xích tải cào (ISO 1977 & DIN 8167 / DIN 8165)
*(Tham chiếu Catalog Trang 48)*

Đây là **tiêu chuẩn biên dạng răng mặc định và phổ biến nhất** của KettenWulf cho các hệ thống băng cào xích tải.

```
          \    /  <-- beta (Góc mở rãnh)
           \  /
   r2 ----> \/ <---- h3 (Đoạn sườn răng phẳng)
            || <---- u  (Độ hở đáy hốc răng)
           (  ) <--- r1 (Bán kính đáy hốc r1 = 0.51 * d1)
            --
```

#### Bảng công thức KWN 017:
| Ký hiệu | Đại lượng | Công thức chuẩn KettenWulf | Ghi chú kỹ thuật |
| :--- | :--- | :--- | :--- |
| $d_0$ | Vòng tròn chia (Pitch circle) | $d_0 = \frac{p}{\sin(180^\circ / z)}$ | Đi qua tâm các chốt xích |
| $d_f$ | Vòng chân răng (Root circle) | $d_f = d_0 - d_1$ | **Dung sai h11** (trang 48) |
| $d_a$ | Vòng đỉnh răng (Top diameter) | - Có con lăn: $d_a = d_0 + 0.4 \cdot d_1$<br>- Con lăn bảo vệ: $d_a = d_0 + 0.6 \cdot d_1$<br>- Không con lăn (ống lót): $d_a = d_0 + 0.8 \cdot d_1$ | Phụ thuộc kết cấu xích |
| $d_s$ | Vòng hạ bậc vành (Recess diameter) | $d_s = \frac{p}{\tan(\alpha / 2)} - g - 2 \cdot r_4$ | Ngăn má xích cạ vào vành đĩa |
| $\alpha$ | Góc phân chia răng | $\alpha = \frac{360^\circ}{z}$ | Trục đối xứng giữa 2 hốc |
| $\beta$ | Góc mở rãnh răng (Opening angle) | - $z = 6 \div 11$: $\beta = \mathbf{74^\circ}$<br>- $z = 12 \div 29$: $\beta = \mathbf{56^\circ}$<br>- $z \ge 30$: $\beta = \mathbf{38^\circ}$ | Tra theo bảng chuẩn trang 48 |
| $\gamma$ | Góc sườn răng (Flank angle) | $\gamma = \frac{\beta}{2} - \frac{180^\circ}{z} = \frac{\beta - \alpha}{2}$ | Dóng từ đường sườn răng đến trục đối xứng |
| $r_1$ | Bán kính đáy hốc răng | $r_1 = 0.51 \cdot d_1$ | Rộng hơn bán kính chốt 1% để thoát mạt |
| $r_2$ | Bán kính cong sườn đỉnh | $r_2 = 0.8 \cdot p$ | Cung lượn vuốt êm vào đỉnh răng |
| $h_3$ | Chiều dài đoạn thẳng sườn răng | $h_3 = 0.3 \cdot d_1$ | Đoạn nghiêng phẳng truyền lực tiếp xúc |
| $u$ | Khe hở đáy hốc răng | $u = 0.02 \cdot p$ | Khe hở bù co giãn nhiệt và dơ bẩn |
| $B_1$ | Chiều rộng vành răng đĩa xích | $B_1 = 0.9 \cdot b_1$ | Nhỏ hơn bề rộng trong má xích 10% |

---

### 4.2. KWN 015 – Tiêu chuẩn hốc răng sâu tối ưu lực phân bố
*(Tham chiếu Catalog Trang 47)*

Tiêu chuẩn nhà máy KWN 015 được thiết kế chuyên biệt cho các điều kiện làm việc cực kỳ khắc nghiệt: vật liệu hạt to dễ chèn kẹt hốc răng, lực kéo va đập lớn.

#### Điểm đặc thù của KWN 015:
- **Góc sườn $\gamma$ có thể tùy chỉnh**: Người thiết kế hoặc kỹ sư KettenWulf có thể chỉ định góc nghiêng sườn $\gamma$ tự do (thường từ $10^\circ \div 20^\circ$, mặc định $14.5^\circ$).
- **Góc mở $\beta$ được tính toán ngược từ $\gamma$**:
$$\beta = \left(\frac{\alpha}{2} + \gamma\right) \cdot 2 = \alpha + 2\gamma$$
- Các công thức kích thước cơ sở khác ($d_0, d_f, d_a, d_s, r_1, r_2, h_3, u, B_1$) hoàn toàn tương đương với KWN 017.

---

### 4.3. KWN 001 – Tiêu chuẩn đĩa xích con lăn truyền động (DIN 8187 / ISO 606)
*(Tham chiếu Catalog Trang 46)*

Dành riêng cho đĩa xích con lăn truyền động tiêu chuẩn DIN 8187 (06B-1, 08B-1, 10B-1, 12B-1, 16B-1, 20B-1...).

#### Bảng công thức KWN 001:
| Ký hiệu | Đại lượng | Công thức chuẩn KettenWulf |
| :--- | :--- | :--- |
| $d_0$ | Vòng chia | $d_0 = \frac{p}{\sin(180^\circ / z)}$ |
| $d_f$ | Vòng chân răng | $d_f = d_0 - d_1 \quad (\text{dung sai } h11)$ |
| $d_a$ | Vòng đỉnh răng | - $z \le 6$: $d_a = d_0 + 0.50 \cdot d_1$<br>- $z = 7 \div 12$: $d_a = d_0 + (0.50 \div 0.60) \cdot d_1$<br>- $z = 13 \div 25$: $d_a = d_0 + (0.60 \div 0.70) \cdot d_1$<br>- $z \ge 26$: $d_a = d_0 + (0.70 \div 0.80) \cdot d_1$ |
| $d_s$ | Vòng hạ vành | $d_s = d_0 - p$ |
| $r_1$ | Bán kính đáy hốc | $r_1 = 0.505 \cdot d_1 + 0.069 \cdot \sqrt[3]{d_1}$ |
| $r_2$ | Bán kính sườn răng | $r_2 = 0.008 \cdot d_1 \cdot (z_1^2 + 180)$ |
| $z_1$ | Hệ số số răng | - $z = 1 \div 6$: $z_1 = 6$<br>- $z = 7 \div 12$: $z_1 = 8$<br>- $z \ge 13$: $z_1 = 12$ |
| $X$ | Góc ôm đáy con lăn | - $z = 1 \div 6$: $X = 115^\circ$<br>- $z = 7 \div 12$: $X = 120^\circ$<br>- $z \ge 13$: $X = 125^\circ$ |
| $B_1$ | Chiều rộng răng | $B_1 = 0.9 \cdot b_1$ |

> [!IMPORTANT]
> **Quy tắc tiếp tuyến sườn răng KWN 001**: Tâm cung lượn sườn $C_2$ phải nằm phía trong thân răng ($C_2 = P_{bed} + r_2 \cdot \vec{u}_{dir}$), tạo thành bề mặt cong lồi hướng vào trong hốc, giúp con lăn đi vào ăn khớp trơn tru, không va chạm góc đỉnh răng.

---

### 4.4. KWN 016 – Tiêu chuẩn đĩa chốt lồng đèn (Lantern Pinion)
*(Tham chiếu Catalog Trang 49)*

Áp dụng cho các đĩa chốt lồng đèn:
- Modun ăn khớp: $m = \frac{p}{\pi}$
- Vòng chia: $d_0 = \frac{z \cdot p}{\pi}$
- Vòng chân: $d_f = d_0 - 2 \cdot (0.15 \cdot m + r_1)$
- Bán kính đáy hốc: $r_1 = 0.5 \cdot d_1$
- Chiều rộng răng: $B_1 = 3.3 \cdot m$
- Khe hở đỉnh răng: $S_1 = 0.04 \cdot m$

---

## 5. TÍNH TOÁN TRỤC, MAY-Ơ & THEN DIN 6885
*(Tham chiếu Catalog Trang 54 - 55)*

### 5.1. Công thức tính chiều dài then bằng ($l$) & may-ơ ($NL$)
$$l \approx \frac{0.736 \cdot P}{n} \cdot K \cdot \frac{1}{\left(\frac{d_w + t_2}{10}\right) \cdot \left(\frac{t_2}{10}\right)}$$
Hệ số áp suất bề mặt: $K = \frac{7162 \cdot 2}{p_{perm}}$
- Vật liệu gang GG 22: $p_{perm} \approx 55\text{ N/mm}^2 \implies K = 260$
- Vật liệu thép St 52-3: $p_{perm} \approx 90\text{ N/mm}^2 \implies K = 160$
- Vật liệu thép tôi C 45: $p_{perm} \approx 95\text{ N/mm}^2 \implies K = 150$

**Chiều dài may-ơ tổng thể ($NL$)**:
- Then đầu tròn: $NL = l + b + (3 \div 5)\text{ mm}$
- Then đầu vuông: $NL = l + (3 \div 5)\text{ mm}$

### 5.2. Bảng then bằng tiêu chuẩn DIN 6885-1 (Trang 55)
| Đường kính trục $d_w$ (mm) | Mặt cắt then $b \times h$ (mm) | Độ sâu rãnh trục $t_1$ (mm) | Dung sai $t_1$ | Độ sâu rãnh may-ơ $t_2$ (mm) | Dung sai $t_2$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| > 6 – 8 | 2 x 2 | 1.2 | +0.1 | 1.0 | +0.1 |
| > 8 – 10 | 3 x 3 | 1.8 | +0.1 | 1.4 | +0.1 |
| > 10 – 12 | 4 x 4 | 2.5 | +0.1 | 1.8 | +0.1 |
| > 12 – 17 | 5 x 5 | 3.0 | +0.1 | 2.3 | +0.1 |
| > 17 – 22 | 6 x 6 | 3.5 | +0.1 | 2.8 | +0.1 |
| > 22 – 30 | 8 x 7 | 4.0 | +0.2 | 3.3 | +0.2 |
| > 30 – 38 | 10 x 8 | 5.0 | +0.2 | 3.3 | +0.2 |
| > 38 – 44 | 12 x 8 | 5.0 | +0.2 | 3.3 | +0.2 |
| > 44 – 50 | 14 x 9 | 5.5 | +0.2 | 3.8 | +0.2 |
| > 50 – 58 | 16 x 10 | 6.0 | +0.2 | 4.3 | +0.2 |
| > 58 – 65 | 18 x 11 | 7.0 | +0.2 | 4.4 | +0.2 |
| > 65 – 75 | 20 x 12 | 7.5 | +0.2 | 4.9 | +0.2 |
| > 75 – 85 | 22 x 14 | 9.0 | +0.2 | 5.4 | +0.2 |
| > 85 – 95 | 25 x 14 | 9.0 | +0.2 | 5.4 | +0.2 |
| > 95 – 110 | 28 x 16 | 10.0 | +0.2 | 6.4 | +0.2 |
| > 110 – 130 | 32 x 18 | 11.0 | +0.2 | 7.4 | +0.2 |
| > 130 – 150 | 36 x 20 | 12.0 | +0.3 | 8.4 | +0.3 |
| > 150 – 170 | 40 x 22 | 13.0 | +0.3 | 9.4 | +0.3 |
| > 170 – 200 | 45 x 25 | 15.0 | +0.3 | 10.4 | +0.3 |
| > 200 – 230 | 50 x 28 | 17.0 | +0.3 | 11.4 | +0.3 |
| > 230 – 260 | 56 x 32 | 20.0 | +0.3 | 12.4 | +0.3 |
| > 260 – 290 | 63 x 32 | 20.0 | +0.3 | 12.4 | +0.3 |
| > 290 – 330 | 70 x 36 | 22.0 | +0.3 | 14.4 | +0.3 |
| > 330 – 380 | 80 x 40 | 25.0 | +0.3 | 15.4 | +0.3 |
| > 380 – 440 | 90 x 45 | 28.0 | +0.3 | 17.4 | +0.3 |
| > 440 – 500 | 100 x 50 | 31.0 | +0.3 | 19.5 | +0.3 |

---

## 6. CÁC DẠNG KẾT CẤU ĐĨA XÍCH
*(Tham chiếu Catalog Trang 56 - 57)*

1. **Đĩa xích cắt gọt nguyên khối (Cut from solid)**:
   - Đĩa phẳng (Plate wheel / Sprocket disk)
   - Đĩa có may-ơ 1 phía (One-sided hub)
   - Đĩa có may-ơ đối xứng (Symmetrical hub)
   - Đĩa có may-ơ lệch tâm (Asymmetrical hub)
2. **Đĩa xích hàn (Welded design)**:
   - May-ơ hàn ốp ngoài (Hub welded on)
   - May-ơ lồng hàn xuyên thân (Hub welded in)
3. **Đĩa xích ghép then / vành răng tháo rời (Segmented / Split sprockets)**:
   - Đĩa nửa tháo lắp không cần tháo trục (Split sprocket)
   - Vành răng bắt bu-lông phân đoạn (Bolted tooth segments) thay thế nhanh khi mòn răng.

---

## 7. BẢNG KÍCH THƯỚC HÌNH HỌC CHUẨN CỦA CÁC DÒNG XÍCH
*(Trích lục đầy đủ từ Trang 30 - 39)*

*(Chi tiết toàn văn toàn bộ 12 model MT, 12 model M, 11 model FVT, 11 model FV và các cỡ xích con lăn được lưu trữ tập trung tại file `docs/CHAIN_SERIES_CATALOG.md` và mã hóa cấu trúc tại `data/chain_catalogs.json`).*

---

## 8. QUY CHUẨN DUNG SAI & CHẾ TẠO

1. **Vòng chân răng $d_f$**: Dung sai âm **h11** theo ISO 286:
   - $d_f \le 50\text{ mm}$: $0 / -0.16\text{ mm}$
   - $d_f = 50 \div 80\text{ mm}$: $0 / -0.19\text{ mm}$
   - $d_f = 80 \div 120\text{ mm}$: $0 / -0.22\text{ mm}$
   - $d_f = 120 \div 180\text{ mm}$: $0 / -0.25\text{ mm}$
   - $d_f = 180 \div 250\text{ mm}$: $0 / -0.29\text{ mm}$
   - $d_f = 250 \div 315\text{ mm}$: $0 / -0.32\text{ mm}$
   - $d_f = 315 \div 400\text{ mm}$: $0 / -0.36\text{ mm}$
   - $d_f = 400 \div 500\text{ mm}$: $0 / -0.40\text{ mm}$
   - $d_f > 500\text{ mm}$: $0 / -0.50\text{ mm}$
2. **Lỗ trục $d_w$**: Dung sai **H7** tiêu chuẩn chế tạo cơ khí chính xác.
3. **Chiều rộng rãnh then $b$**: Dung sai **P9** (lắp chặt) hoặc **JS9** (lắp tiêu chuẩn).
4. **Vát mép đỉnh răng $b_a$ & bán kính $r_x$**:
   - Vát mép đỉnh: $b_a = (0.10 \div 0.15) \cdot p$
   - Bán kính lượn góc vành: $r_4 = (0.04 \div 0.08) \cdot p$
