
#Cell 4: Định Nghĩa Hàm save_camera_parameters


def save_camera_parameters(ret, camera_matrix, distortion_coefficients, camera_label):
    if ret:
        # Tạo tên file riêng dựa trên camera_label để tránh ghi đè
        np.save(f"camera_matrix_{camera_label}.npy", camera_matrix)
        np.save(f"distortion_coefficients_{camera_label}.npy", distortion_coefficients)

        print(f"✅ Hiệu chỉnh camera {camera_label} thành công!")
        print(f"📌 Camera Matrix {camera_label}:\n", camera_matrix)
        print(f"📌 Distortion Coefficients {camera_label}:\n", distortion_coefficients)
    else:
        print(f"❌ Hiệu chỉnh camera {camera_label} thất bại! Kiểm tra lại ảnh đầu vào.")




#Cell 5: Hiệu Chỉnh Camera Trái và Phải (Calibration Cá Nhân)



chessboard_size = (8, 5)  # Số ô - 1 trên bảng checkerboard
# Kích thước thực tế của mỗi ô vuông (mm)
square_size = 32
left_path = r"D:/left/*.jpg"
right_path = r"D:/right/*.jpg"


# Hiệu chỉnh camera trái
K1, D1, ret1 = calibrate_camera(left_path, chessboard_size, square_size)
print("Ma trận nội tại của Camera Trái (K1):\n", K1)
print("Hệ số méo của Camera Trái (D1):\n", D1)

# Lưu thông số camera trái
save_camera_parameters(ret1, K1, D1, "left")

# Hiệu chỉnh camera phải
K2, D2, ret2 = calibrate_camera(right_path, chessboard_size, square_size)
print("Ma trận nội tại của Camera Phải (K2):\n", K2)
print("Hệ số méo của Camera Phải (D2):\n", D2)

# Lưu thông số camera phải
save_camera_parameters(ret2, K2, D2, "right")



#Cell 6: Stereo Calibration (Hiệu Chỉnh Stereo)


# Thực hiện stereo calibration dựa trên các cặp ảnh đồng thời của 2 camera
ret_stereo, R, T, E, F, newK1, newD1, newK2, newD2 = stereo_calibrate(
    left_path, right_path, chessboard_size, square_size, K1, D1, K2, D2
)

if ret_stereo is not None:
    if ret_stereo:
        print("✅ Stereo calibration thành công!")
        print("Ma trận quay (R):\n", R)
        print("Vector dịch chuyển (T):\n", T)
        baseline = np.linalg.norm(T)
        print("Baseline (khoảng cách giữa 2 camera):", baseline)
    else:
        print("❌ Stereo calibration thất bại!")
else:
    print("❌ Stereo calibration không thực hiện được do thiếu dữ liệu.")