Hiệu chỉnh Camera Stereo 
(Stereo Camera Calibration)

I.Cơ sở lý thuyết 

Giới Thiệu Camera Stereo

Hệ thống camera stereo sử dụng 2 cảm biến ảnh đặt cách nhau 1 khoảng cố định (baseline) để mô phỏng thị giác lập thể của con người


Nguyên lý hoạt động 
Nguyên lý hoạt động dựa trên:
Thị sai (Parallax): Độ lệch vị trí pixel của cùng vật thể trên 2 ảnh
Tam giác hóa: Tính toán khoảng cách dùng công thức hình học

Trong đó:
Z: Khoảng cách đến vật thể
f: Tiêu cự camera
B: Baseline (khoảng cách giữa 2 camera)
d: Disparity (độ lệch pixel)

So Sánh với Các Phương Pháp Đo Khoảng Cách Khác

Phương Pháp
Nguyên Lý Hoạt Động
Phạm Vi Hiệu Quả
Độ Chính Xác
Ưu Điểm
Nhược Điểm
Ứng Dụng Điển Hình
Camera Stereo
Thị sai lập thể + tam giác hóa
0.5m - 20m
±1-5%
Chi phí thấp, đo thụ động
Phụ thuộc ánh sáng/texture bề mặt
Robot, xe tự hành, 3D scanning
LiDAR
Phát xung laser + đo thời gian phản hồi
1m - 200m+
±1-2cm
Độ chính xác cao, tốc độ nhanh
Giá thành cao, kích thước lớn
Ô tô tự lái, lập bản đồ 3D
ToF Camera
Đo thời gian bay của photon
0.1m - 5m
±1-3cm
Tốc độ cao (160 fps), kích thước nhỏ
Nhạy cảm với ánh sáng môi trường
Smartphone AR, làm mờ

Lý do lựa chọn phương pháp Camera Stereo:
Camera stereo sử dụng nguyên lý thị sai lập thể và tam giác hóa, là các phương pháp hình học tương đối đơn giản. Không cần các thành phần phức tạp như laser (LiDAR) hoặc cảm biến thời gian (ToF).
Camera và ống kính là các thành phần phổ biến và dễ dàng tìm thấy trên thị trường với nhiều mức giá khác nhau. 
Hệ thống này hoạt động bằng cách ghi lại hình ảnh từ hai camera và phân tích sự khác biệt (disparity) giữa các hình ảnh này. Sự khác biệt này là do vị trí của vật thể khác nhau trên hai hình ảnh, và nó được sử dụng để tính toán khoảng cách mà không cần phát tín hiệu.

