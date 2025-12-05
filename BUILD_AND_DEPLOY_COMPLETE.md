# 🎯 CHECK_ALL_STAGE - COMPLETE BUILD & DEPLOYMENT GUIDE

## 📦 TẠO FILE EXE

### Phương pháp 1: Build tất cả (Khuyến nghị) ⭐
```batch
# Build cả Check_All_Stage.exe và update_script.exe
build_all.bat
```

Batch này sẽ:
1. ✅ Xóa build cũ
2. ✅ Cài đặt/cập nhật packages
3. ✅ Build Check_All_Stage.exe (~28 MB)
4. ✅ Build update_script.exe (~11 MB)
5. ✅ Copy cả 2 exe ra thư mục gốc

### Phương pháp 2: Build riêng từng file
```batch
# Build chỉ Check_All_Stage.exe
build_exe.bat

# Build chỉ update_script.exe
build_update_script.bat
```

### Phương pháp 3: Thủ công
```powershell
# Build Check_All_Stage
pyinstaller --clean Check_All_Stage.spec

# Build update_script
pyinstaller --clean update_script.spec
```

---

## 📤 TẠO PACKAGE PHÂN PHỐI

### Tự động (Khuyến nghị) ⭐
```batch
# Chạy sau khi đã build exe thành công
create_distribution_package.bat
```

Package sẽ được tạo trong: `Check_All_Stage_Distribution/`

### Cấu trúc package:
```
Check_All_Stage_Distribution/
├── Check_All_Stage.exe     (~28 MB) - Main application
├── update_script.exe       (~11 MB) - Auto-update utility
├── config.json             (< 1 KB)  - Configuration
├── README.md              (User guide)
└── Resource/              (Images & icons)
    ├── background.jpg
    ├── Icon.ico
    ├── logo.png
    └── ... (14 files total)
```

**Total package size: ~40 MB**

---

## 🎁 CHUẨN BỊ PHÂN PHỐI

### Bước 1: Test package
```batch
# Chạy thử trong thư mục distribution
cd Check_All_Stage_Distribution
Check_All_Stage.exe
```

### Bước 2: Tạo file ZIP
```powershell
# Nén thư mục thành ZIP
Compress-Archive -Path Check_All_Stage_Distribution -DestinationPath Check_All_Stage_v1.0.zip
```

### Bước 3: Gửi cho người dùng
- Gửi file ZIP qua email/network
- Người dùng giải nén và chạy

---

## 🛠️ FILES QUAN TRỌNG

### Build Files:
- ✅ `build_all.bat` - Build tất cả executables (RECOMMENDED)
- ✅ `build_exe.bat` - Build chỉ Check_All_Stage.exe
- ✅ `build_update_script.bat` - Build chỉ update_script.exe
- ✅ `Check_All_Stage.spec` - PyInstaller config cho main app
- ✅ `update_script.spec` - PyInstaller config cho updater
- ✅ `hook-oracledb.py` - Custom hook cho oracledb/cryptography
- ✅ `requirements.txt` - Dependencies list
- ✅ `BUILD_GUIDE.md` - Hướng dẫn build chi tiết

### Deployment Files:
- ✅ `create_distribution_package.bat` - Tạo package tự động
- ✅ `DEPLOYMENT_GUIDE.md` - Hướng dẫn người dùng

### Application Files:
- ✅ `Check_All_Stage.py` - Main program
- ✅ `update_script.py` - Update utility program
- ✅ `config.json` - Configuration
- ✅ `Resource/` - Images & icons
- ✅ `ui/` - UI modules
- ✅ `data/` - Data modules
- ✅ `utils/` - Utility modules

---

## 📝 WORKFLOW HOÀN CHỈNH

### Khi phát triển:
```batch
# 1. Code xong, test bằng Python
python Check_All_Stage.py
python update_script.py

# 2. Build cả 2 exe
build_all.bat

# 3. Tạo package phân phối
create_distribution_package.bat

# 4. Test package
cd Check_All_Stage_Distribution
Check_All_Stage.exe

# 5. Nén và phân phối
# (Dùng Windows Explorer hoặc command)
```

### Khi update:
```batch
# 1. Sửa code
# 2. Update version trong utils/utils.py
# 3. Chạy lại workflow trên
# 4. Upload lên FTP server (cho auto-update)
```

---

## 🔍 KIỂM TRA TRƯỚC KHI PHÂN PHỐI

### Checklist:
- [ ] Build thành công không có lỗi
- [ ] File Check_All_Stage.exe chạy được
- [ ] File update_script.exe chạy được
- [ ] Login thành công
- [ ] Database connection OK (cả 2 loại)
- [ ] Settings mở và lưu được
- [ ] FTP settings đầy đủ và đúng
- [ ] Tất cả hình ảnh hiển thị đúng
- [ ] Test cả 4 loại sản phẩm (P1, P4, P230, P140)
- [ ] Auto-update hoạt động (nếu có FTP server)
- [ ] File README.md đầy đủ thông tin

---

## 📊 THÔNG TIN BUILD

### Build Output:
- **Check_All_Stage.exe**: ~28 MB
- **update_script.exe**: ~11 MB
- **Total Package**: ~40 MB (with resources)
- **Compression**: UPX enabled
- **Console**: Disabled (GUI only)
- **Icon**: Resource\Icon.ico

### Dependencies Included:
- Python 3.13.2
- PyInstaller 6.17.0
- oracledb 3.4.1
- Pillow 12.0.0
- QRCode 8.2
- tkinter (built-in)
- All custom modules (ui, data, utils)

### Hidden Imports:
- All UI modules (creategui_*)
- All data modules (calibration, pba, etc.)
- All utils modules (db_config, config_manager, etc.)
- Database drivers (oracledb, cx_Oracle)
- Image libraries (PIL, qrcode)

---

## 🐛 TROUBLESHOOTING BUILD

### Error: "Module not found"
**Giải pháp**: Thêm vào `hiddenimports` trong Check_All_Stage.spec

### Error: "Cannot find Resource files"
**Giải pháp**: Kiểm tra `datas` section trong .spec file

### Error: "Import error: oracledb"
**Giải pháp**: 
```bash
pip install oracledb
```

### Error: "Import error: cx_Oracle"
**Giải pháp** (Optional):
```bash
pip install cx-Oracle
```
Note: cx_Oracle chỉ cần nếu dùng connection type cx_Oracle

### Build quá lâu:
- Bình thường: 30-60 giây
- Nếu > 2 phút: Kill và build lại
- Xóa cache: `Remove-Item -Recurse C:\Users\Admin\AppData\Local\pyinstaller`

### File exe quá lớn:
- Hiện tại: ~24 MB là OK
- Nếu > 100 MB: Có thể thêm excludes trong .spec
- Không nên exclude quá nhiều, dễ bị thiếu module

---

## 📈 VERSION MANAGEMENT

### Update version:
1. Sửa trong `utils/utils.py`:
```python
def get_current_version():
    return "1.0.1"  # Tăng version
```

2. Upload lên FTP:
   - File: `version.txt` với nội dung "1.0.1"
   - File: `Check_All_Stage.exe` (new version)

3. User sẽ tự động update khi mở app

---

## 💡 TIPS & TRICKS

### Build nhanh hơn:
- Không thay đổi .spec → PyInstaller cache faster
- Clean build chỉ khi cần thiết: `--clean`

### Giảm size:
- Thêm excludes: numpy, matplotlib, pandas, scipy (nếu không dùng)
- Đã loại trừ trong .spec file rồi

### Debug build errors:
- Xem file: `build/Check_All_Stage/warn-Check_All_Stage.txt`
- Chạy với console=True để xem errors
- Test import từng module riêng

### Test package:
- Chạy trên máy sạch (không có Python)
- Test trên Windows khác versions
- Test với/không có internet
- Test với database settings khác nhau

---

## 📞 SUPPORT

**Khánh IT**: https://zalo.me/0944187335

---

**© 2025 ITM Semiconductor Vietnam**

*Document created: December 4, 2025*
