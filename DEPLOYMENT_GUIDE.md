# 📦 CHECK_ALL_STAGE - DEPLOYMENT PACKAGE

## 📋 Mô tả
Phần mềm kiểm tra dữ liệu từng giai đoạn sản xuất cho các sản phẩm ECIGA.

## 📁 Cấu trúc thư mục cần thiết

```
Check_All_Stage/
├── Check_All_Stage.exe          ⚠️ BẮT BUỘC - File chương trình chính
├── config.json                   ⚠️ BẮT BUỘC - File cấu hình hệ thống
├── login_info.ini               ✅ TỰ ĐỘNG - Lưu thông tin đăng nhập (tự tạo)
└── Resource/                    ⚠️ BẮT BUỘC - Thư mục chứa hình ảnh
    ├── background.jpg
    ├── Icon.ico
    ├── logo.png
    ├── OK.png
    ├── NG.png
    ├── Check.png
    ├── green.png
    ├── red.png
    ├── arrowtoright.png
    ├── arrowtoleft.png
    ├── arrowtodown.png
    ├── bg.png
    ├── None.png
    └── Check.gif
```

## 🚀 Cách cài đặt

### Bước 1: Giải nén
Giải nén file zip vào thư mục bạn muốn cài đặt (ví dụ: `C:\Check_All_Stage`)

### Bước 2: Kiểm tra cấu trúc
Đảm bảo có đủ các file và thư mục như trên

### Bước 3: Chạy chương trình
Double-click vào `Check_All_Stage.exe`

## ⚙️ Cấu hình

### Lần đầu chạy:
1. Click nút **⚙️ Settings** ở góc trên bên phải
2. Cấu hình các thông số:

#### 📁 Program Settings:
- **Program Directory**: Thư mục chứa chương trình (mặc định: `C:\Check_All_Stage`)
- **FTP Base URL**: URL máy chủ FTP để update

#### 💾 Database Settings:
Chọn loại kết nối:

**Option 1: oracledb (Khuyến nghị)**
- ✅ Không cần cài Oracle Client
- ✅ Nhẹ và nhanh
- Cấu hình: User, Password, Host, Port, Service Name

**Option 2: cx_Oracle**
- ⚠️ Cần cài Oracle Client
- Cấu hình: User, Password, DSN String

3. Click **🔌 TEST DB** để test kết nối
4. Click **💾 SAVE** để lưu
5. **Restart** chương trình

## 👤 Đăng nhập

### Tài khoản:
- Username và Password được quản lý trong database
- Liên hệ IT để tạo tài khoản

### Chọn sản phẩm:
- ECIGA-P1EZ
- ECIGA-P2 3.0
- ECIGA-P4
- ECIGA-P140

### Remember me:
✅ Tick vào để lưu thông tin đăng nhập

### Quên mật khẩu:
Click "Forgot password?" để xem thông tin liên hệ IT

## 🔄 Update chương trình

Chương trình tự động kiểm tra update khi khởi động.
- Nếu có phiên bản mới, sẽ tự động download và cài đặt
- Chương trình sẽ tự động restart sau khi update

## 📝 Yêu cầu hệ thống

- **OS**: Windows 7/8/10/11 (64-bit)
- **RAM**: Tối thiểu 2GB
- **Disk**: 100MB trống
- **Network**: Kết nối mạng để truy cập database

## 🐛 Khắc phục sự cố

### Lỗi: "Cannot connect to database"
✅ Kiểm tra:
1. Kết nối mạng
2. Cấu hình database trong Settings
3. Click **🔌 TEST DB** để test kết nối

### Lỗi: "Missing Resource files"
✅ Giải pháp:
- Đảm bảo thư mục `Resource` nằm cùng thư mục với file .exe
- Kiểm tra đủ các file hình ảnh trong thư mục Resource

### Lỗi: "Login failed"
✅ Kiểm tra:
1. Username/Password đúng chưa
2. Tài khoản đã được tạo trong database chưa
3. Liên hệ IT nếu cần reset mật khẩu

### Chương trình không khởi động
✅ Thử:
1. Chạy với quyền Administrator
2. Kiểm tra Windows Defender/Antivirus có chặn không
3. Xóa file `login_info.ini` và chạy lại

## 📞 Hỗ trợ

### Liên hệ IT:
- **Khánh IT**: https://zalo.me/0944187335
- Scan QR code trong "Forgot Password"

## 📌 Lưu ý quan trọng

⚠️ **Không xóa hoặc sửa các file sau:**
- `config.json` - Chứa cấu hình hệ thống
- Thư mục `Resource` - Chứa hình ảnh cần thiết

✅ **An toàn khi xóa:**
- `login_info.ini` - Sẽ tự động tạo lại khi đăng nhập

📌 **Backup quan trọng:**
- Backup file `config.json` trước khi update/thay đổi

## 🔐 Bảo mật

- Mật khẩu trong `config.json` lưu dạng plain text
- Không chia sẻ file `config.json` ra bên ngoài
- Không chia sẻ file `login_info.ini` cho người khác

## 📊 Version Info

Build với:
- PyInstaller 6.17.0
- Python 3.13.2
- oracledb 3.4.1
- Pillow 12.0.0
- QRCode 8.2

---

**© 2025 ITM Semiconductor Vietnam**
