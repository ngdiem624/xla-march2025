
#Cell 2: Định Nghĩa Hàm calibrate_camera


def calibrate_camera(image_pattern, chessboard_size, square_size):
    
      
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Chuẩn bị tọa độ 3D của các góc trên bảng caro
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

    # Danh sách lưu điểm 3D và điểm 2D
    objpoints = []  
    imgpoints = []  

    # Đọc tất cả ảnh trong thư mục
    images = glob.glob(image_pattern)

    if len(images) == 0:
            print("❌ Không tìm thấy ảnh trong thư mục 'image_pattern'. Kiểm tra lại đường dẫn!")
    else:
        print(f"🔍 Đã tìm thấy {len(images)} ảnh để hiệu chỉnh: {images}")

    for fname in images:
        img = cv2.imread(fname)
    
        if img is None:
            print(f"⚠️ Không thể đọc ảnh {fname}. Kiểm tra lại file!")
            continue
        # Chuyển ảnh sang dạng xám
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # --- BẮT ĐẦU PHẦN ENHANCE ẢNH ---
        # Sử dụng CLAHE để tăng cường độ tương phản của ảnh
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        # --- KẾT THÚC PHẦN ENHANCE ẢNH ---
        # Tìm góc bảng caro
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            # Vẽ và hiển thị góc tìm được
            cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
            cv2.imshow('Chessboard', img)
            cv2.waitKey(500)
        else:
            print(f"⚠️ Không tìm thấy góc trong ảnh {fname}. Hãy kiểm tra lại bảng caro.")
            cv2.imshow("Ảnh lỗi", img)
            cv2.waitKey(1000)  

    cv2.destroyAllWindows()

    # Hiệu chỉnh camera nếu có đủ dữ liệu
    if len(objpoints) > 0 and len(imgpoints) > 0:
        print("📷 Đang hiệu chỉnh camera...")
        ret, K, D, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        return K, D, ret
    else:
        print("❌ Không có đủ dữ liệu để hiệu chỉnh camera.")