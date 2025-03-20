

#Cell 7: Stereo Rectification & Tính Toạ Độ 3D



# ========== 1) NẠP MA TRẬN HIỆU CHỈNH (CALIBRATION) ==========
newK1 = np.load("camera_matrix_left.npy")
newD1 = np.load("distortion_coefficients_left.npy")
newK2 = np.load("camera_matrix_right.npy")
newD2 = np.load("distortion_coefficients_right.npy")

R = np.eye(3, dtype=np.float32)  # Ma trận quay (ví dụ)
T = np.array([[60.0], [0.0], [0.0]])  # baseline ~60 mm (ví dụ)
image_size = (640, 480)

# ========== 2) ĐỌC ẢNH TRÁI - PHẢI ==========
left_img = cv2.imread("D:/anh_nhan_dang_dc/21.jpg")
right_img = cv2.imread("D:/anh_nhan_dang_dc/22.jpg")

if left_img is None or right_img is None:
    print("Không đọc được ảnh. Kiểm tra đường dẫn!")
    import sys
    sys.exit(1)

left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

# ========== 3) STEREO RECTIFY ==========
R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
    newK1, newD1, newK2, newD2, image_size, R, T, alpha=0
)

left_map1, left_map2 = cv2.initUndistortRectifyMap(
    newK1, newD1, R1, P1, image_size, cv2.CV_16SC2
)
right_map1, right_map2 = cv2.initUndistortRectifyMap(
    newK2, newD2, R2, P2, image_size, cv2.CV_16SC2
)

left_rect = cv2.remap(left_gray, left_map1, left_map2, cv2.INTER_LINEAR)
right_rect = cv2.remap(right_gray, right_map1, right_map2, cv2.INTER_LINEAR)

# ========== 4) CHO PHÉP NHẬP TỌA ĐỘ BÊN TRÁI ==========
# Ví dụ: nhập "200,150" => x=200, y=150
print("Nhập toạ độ (uL, vL) của điểm bên ảnh trái (ví dụ: 320,240): ")
user_input = input().strip()  # Đọc chuỗi từ console

# Tách chuỗi
try:
    uL_str, vL_str = user_input.split(',')
    uL, vL = int(uL_str), int(vL_str)
except:
    print("❌ Lỗi khi phân tích toạ độ, dùng mặc định (320,240).")
    uL, vL = 320, 240

# Kiểm tra toạ độ có nằm trong ảnh không
h, w = left_rect.shape
if not (0 <= uL < w and 0 <= vL < h):
    print("❌ Toạ độ nằm ngoài ảnh. Dùng mặc định (320,240).")
    uL, vL = 320, 240

print(f"Điểm ảnh trái (uL, vL) = ({uL}, {vL})")

# ========== 5) TÌM ĐIỂM TƯƠNG ỨNG BÊN PHẢI QUA TEMPLATE MATCHING ==========
patch_size = 15
x1 = max(0, uL - patch_size)
y1 = max(0, vL - patch_size)
x2 = min(w, uL + patch_size)
y2 = min(h, vL + patch_size)

patch_left = left_rect[y1:y2, x1:x2]

res = cv2.matchTemplate(right_rect, patch_left, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(res)

best_xR, best_yR = max_loc
best_uR = best_xR + (x2 - x1)//2
best_vR = best_yR + (y2 - y1)//2

print(f"Điểm ảnh phải (uR, vR) = ({best_uR}, {best_vR}), score = {max_val:.3f}")

# ========== 6) TÍNH TOẠ ĐỘ 3D BẰNG TRIANGULATEPOINTS ==========
ptsL = np.array([[(uL, vL)]], dtype=np.float32).transpose(1, 0, 2)
ptsR = np.array([[(best_uR, best_vR)]], dtype=np.float32).transpose(1, 0, 2)

pts4D = cv2.triangulatePoints(P1, P2, ptsL, ptsR)
pts3D = pts4D / pts4D[3]  # (X, Y, Z, 1)

X, Y, Z = pts3D[0, 0], pts3D[1, 0], pts3D[2, 0]

dist = math.sqrt(X**2 + Y**2 + Z**2)

print(f"\nToạ độ 3D tính được: X={X:.2f}, Y={Y:.2f}, Z={Z:.2f}")
print(f"Khoảng cách = {dist:.2f} mm")

# ========== 7) HIỂN THỊ ==========
left_show = cv2.cvtColor(left_rect, cv2.COLOR_GRAY2BGR)
right_show = cv2.cvtColor(right_rect, cv2.COLOR_GRAY2BGR)

cv2.circle(left_show, (uL, vL), 5, (0,0,255), -1)
cv2.circle(right_show, (best_uR, best_vR), 5, (0,0,255), -1)

cv2.imshow("Left", left_show)
cv2.imshow("Right", right_show)
cv2.waitKey(0)
cv2.destroyAllWindows()
