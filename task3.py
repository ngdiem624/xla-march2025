
#Cell 3: Định Nghĩa Hàm stereo_calibrate



def stereo_calibrate(left_image_pattern, right_image_pattern, chessboard_size, square_size, K1, D1, K2, D2):
    """
    Thực hiện stereo calibration với các cặp ảnh từ camera trái và phải.
    
    Tham số:
      left_image_pattern, right_image_pattern: mẫu đường dẫn ảnh cho camera trái và phải.
      chessboard_size: kích thước bàn caro (số góc bên trong).
      square_size: kích thước thực tế của mỗi ô.
      K1, D1, K2, D2: thông số nội tại và hệ số méo của 2 camera đã hiệu chỉnh.
    
    Trả về: ret, R, T, E, F, cùng với các thông số nội tại (nếu có cập nhật).
    """
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Tọa độ 3D của các góc
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

    objpoints = []       # danh sách điểm 3D (chung cho các cặp ảnh)
    imgpoints_left = []  # danh sách điểm 2D từ camera trái
    imgpoints_right = [] # danh sách điểm 2D từ camera phải

    left_images = glob.glob(left_image_pattern)
    right_images = glob.glob(right_image_pattern)
    left_images.sort()
    right_images.sort()

    if len(left_images) == 0 or len(right_images) == 0:
        print("❌ Không tìm thấy ảnh cho stereo calibration. Kiểm tra lại đường dẫn!")
        return None, None, None, None, None, None, None, None, None

    print(f"🔍 Stereo calibration sử dụng {min(len(left_images), len(right_images))} cặp ảnh.")

    # Duyệt qua các cặp ảnh
    for left_fname, right_fname in zip(left_images, right_images):
        left_img = cv2.imread(left_fname)
        right_img = cv2.imread(right_fname)
        if left_img is None or right_img is None:
            print(f"⚠️ Không đọc được cặp ảnh: {left_fname}, {right_fname}")
            continue
        left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

        ret_left, corners_left = cv2.findChessboardCorners(left_gray, chessboard_size, None)
        ret_right, corners_right = cv2.findChessboardCorners(right_gray, chessboard_size, None)

        if ret_left and ret_right:
            objpoints.append(objp)
            imgpoints_left.append(corners_left)
            imgpoints_right.append(corners_right)
            # Hiển thị góc tìm được (tùy chọn)
            cv2.drawChessboardCorners(left_img, chessboard_size, corners_left, ret_left)
            cv2.drawChessboardCorners(right_img, chessboard_size, corners_right, ret_right)
            cv2.imshow("Left", left_img)
            cv2.imshow("Right", right_img)
            cv2.waitKey(500)
        else:
            print(f"⚠️ Không tìm thấy góc đủ trong cặp ảnh: {left_fname} và {right_fname}")
    cv2.destroyAllWindows()

    # Giả sử kích thước ảnh lấy từ ảnh trái (phải nhất quán)
    image_size = left_gray.shape[::-1]

    # Thực hiện stereo calibration (fix intrinsic vì đã biết K1, D1, K2, D2)
    flags = cv2.CALIB_FIX_INTRINSIC
    ret, newK1, newD1, newK2, newD2, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints_left, imgpoints_right,
        K1, D1, K2, D2,
        image_size,
        criteria=criteria,
        flags=flags
    )

    return ret, R, T, E, F, newK1, newD1, newK2, newD2