# KETTENWULF SPROCKET CAD STUDIO (v2.0)
**Phần Mềm Mô Phỏng Động Học & Thiết Kế Đĩa Xích Tải Nặng Tiêu Chuẩn Quốc Tế**

Hệ thống tính toán hình học, mô phỏng động học 2D ăn khớp xích mượt mà và xuất bản vẽ kỹ thuật CAD DXF (R12 / AC1009) chuẩn xác phục vụ gia công cơ khí chế tạo, tích hợp trọn bộ dữ liệu từ:
- **KettenWulf Engineering Catalog** (92 trang - Đức)
- **ScanChain High Precision Conveyor Chains & Sprockets** (Thụy Điển / Bắc Âu)
- **Tiêu chuẩn Quốc tế**: ISO 1977, ISO 606, DIN 8165, DIN 8167, DIN 8187, DIN 6885-1, ISO 128, ISO 129.

---

## 🚀 TRẢI NGHIỆM TRỰC TUYẾN (LIVE DEMO)
- **Vercel Deployment**: Sẵn sàng triển khai 1-click lên Vercel (`https://your-project.vercel.app`).
- **Mã nguồn**: Quản lý tập trung trên GitHub.

---

## 👥 MÔ HÌNH 5 CHUYÊN GIA DỰ ÁN (PROJECT ARCHITECTURE)

Dự án được xây dựng và giám sát theo quy trình khép kín 5 vai trò chuyên gia:
1. **Trưởng Ban Tiêu Chuẩn & Dữ Liệu Xích (Chain Standards Specialist):** Quản lý SSOT (Single Source of Truth), trích xuất và chuẩn hóa thông số catalog gốc từ KettenWulf, ScanChain, Tsubaki.
2. **Kỹ sư Trưởng Thiết Kế Kết Cấu & May-ơ (Senior Mechanical Design Specialist):** Quy định tỷ lệ hình học đĩa xích ($D_n, L_n, d_w$), phân tách rõ ràng kích thước chế tạo hình học vs kiểm nghiệm ứng suất then DIN 6885.
3. **Kỹ sư Lập Trình Thuật Toán CAD & Web Engine (Lead CAD Algorithm & Web Architect):** Phát triển thuật toán hình học giải tích, ma trận biến đổi SVG, bộ giải phóng to thu nhỏ (Pan/Zoom) và xuất DXF R12.
4. **Họa Viên Trưởng CAD & Kỹ Thuật Thị Giác (Lead CAD Draftsman & Visual Specialist):** Chuẩn hóa đường nét kỹ thuật ISO 128 (nét đậm, nét đứt chân răng, nét gạch chấm tâm, gạch mặt cắt kim loại ANSI 31 nghiêng 45°), hệ thống dóng kích thước ISO 129, giao diện Dark Mode chống mỏi mắt.
5. **Trưởng Ban Kiểm Định Độc Lập QA/QC (Senior Engineering Auditor):** Kiểm toán chéo 100% giữa tài liệu gốc PDF, công thức toán học và file DXF xuất xưởng trước khi nghiệm thu.

---

## 📐 CÁC CHẾ ĐỘ QUAN SÁT & BẢN VẼ KỸ THUẬT

1. **Toàn Bộ Đĩa Xích 2D & Mô Phỏng Động Học:**
   - Biên dạng răng CAD chính xác từng micromet.
   - Mô phỏng dải xích con lăn/ống lót ăn khớp chuyển động mượt mà với thanh trượt điều tốc ($0.1x \div 2.0x$).
   - Vòng tròn cơ sở: Vòng đỉnh $d_a$, Vòng chia $d_0$, Vòng chân $d_f$ (dung sai h11), Bậc thân đĩa $d_s$, Lỗ trục $d_w$ và then DIN 6885.

2. **Chi Tiết Hốc Răng (Macro):**
   - Phóng to 1 hốc răng trung tâm với phân màu layer CAD chuyên biệt.
   - Thể hiện rõ: Đáy phẳng $u$, Cung đáy $r_1$, Đoạn sườn thẳng $h_3$, Cung đỉnh $r_2$, Con lăn tiếp xúc, Góc mở $\beta$ và Góc sườn $\gamma$.

3. **Bản Vẽ Mặt Cắt Dọc Trục A-A (Axial Section View A-A):**
   - Bản vẽ mặt cắt toàn phần đối xứng gồm **Cả Nửa Trên và Nửa Dưới** theo chuẩn ISO 128 / TCVN 8-24.
   - Trục tâm quay nằm ngang (Shaft Centerline) chạy xuyên qua khoảng rỗng lỗ trục $d_w$.
   - Thể hiện rãnh then chuẩn DIN 6885-1 ($b \times t_2$) trên may-ơ.
   - Thân kim loại được gạch mặt cắt kim loại ANSI 31 nghiêng 45° đồng nhất cả hai nửa. Răng để nguyên không gạch theo chuẩn quốc tế.
   - Tự động nạp kích thước May-ơ công nghiệp chuẩn ScanChain / KettenWulf (Type A đĩa phẳng, Type B may-ơ 1 phía, Type C may-ơ 2 phía đối xứng).

---

## 🛠 HƯỚNG DẪN TRIỂN KHAI LÊN GITHUB & VERCEL

### Bước 1: Khởi tạo và Đẩy lên GitHub (Push to GitHub)
Mở PowerShell tại thư mục dự án:
```powershell
# 1. Khởi tạo Git
git init

# 2. Thêm toàn bộ mã nguồn sạch (đã loại bỏ PDF nặng nhờ .gitignore)
git add .
git commit -m "feat: KettenWulf & ScanChain Industrial CAD Sprocket Engine (v2.0)"

# 3. Đặt nhánh chính là main
git branch -M main

# 4. Tạo 1 repository mới trên GitHub (ví dụ: https://github.com/USERNAME/xich-tai-nang)
# Sau đó liên kết và đẩy code:
git remote add origin https://github.com/USERNAME/xich-tai-nang.git
git push -u origin main
```

### Bước 2: Triển khai 1-Click lên Vercel (Deploy to Vercel)
1. Đăng nhập [Vercel.com](https://vercel.com/) bằng tài khoản GitHub của bạn.
2. Nhấn nút **Add New...** -> **Project**.
3. Chọn Repository `xich-tai-nang` vừa đẩy lên từ danh sách GitHub.
4. Ở phần thiết lập:
   - **Framework Preset**: Chọn `Other` (dự án web tĩnh thuần HTML5/CSS3/ES6).
   - **Root Directory**: Để trống `./`.
5. Nhấn **Deploy**.
6. Chỉ sau 15-30 giây, website sẽ hoạt động trực tiếp tại địa chỉ công khai: `https://xich-tai-nang.vercel.app`!
Mỗi khi bạn `git push` cập nhật code mới, Vercel sẽ tự động cập nhật bản mới nhất ngay lập tức.

---

## 🧪 KIỂM TOÁN HỆ THỐNG (TESTING & AUDIT)
Chạy bộ kiểm thử tự động QA:
```powershell
python tests/run_all_tests.py
```
---
*Được phát triển với Google Antigravity – Kiến trúc phần mềm cơ khí chuyên sâu.*
