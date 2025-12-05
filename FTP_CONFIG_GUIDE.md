# 📡 FTP UPDATE CONFIGURATION GUIDE

## 🔄 Thay đổi cấu trúc FTP Settings

### ❌ Format cũ (deprecated):
```json
{
  "program_settings": {
    "ftp_base_url": "ftp://update:update@192.168.110.12/KhanhDQ/P3/Update/"
  }
}
```

### ✅ Format mới (recommended):
```json
{
  "program_settings": {
    "ftp_server": "10.62.102.5",
    "ftp_user": "update",
    "ftp_password": "update",
    "ftp_directory": "KhanhDQ/Update_Program/Check_All_Stage/"
  }
}
```

## 🎯 Lý do thay đổi:

1. **Dễ quản lý**: Mỗi thông số riêng biệt, dễ chỉnh sửa
2. **Tương thích update_script.py**: Script update cần từng thông số riêng
3. **Bảo mật tốt hơn**: Password riêng biệt, dễ thay đổi
4. **Linh hoạt**: Có thể đổi server/user/pass độc lập

## ⚙️ Cấu hình trong Settings

### Giao diện mới:

```
🌐 FTP UPDATE SETTINGS
┌────────────────────────────────────────┐
│ FTP Server:    10.62.102.5            │
├────────────────────────────────────────┤
│ FTP User:      update                  │
├────────────────────────────────────────┤
│ FTP Password:  ******                  │
├────────────────────────────────────────┤
│ FTP Directory: KhanhDQ/Update_Program/ │
│                Check_All_Stage/        │
└────────────────────────────────────────┘
```

### Các field:

- **FTP Server**: IP hoặc hostname của FTP server
- **FTP User**: Username để đăng nhập FTP
- **FTP Password**: Password (hiển thị dạng ******)
- **FTP Directory**: Đường dẫn thư mục chứa update files trên server

## 📁 Cấu trúc thư mục FTP Server

```
FTP Root/
└── KhanhDQ/
    └── Update_Program/
        └── Check_All_Stage/
            ├── version.txt         ← File chứa số version mới nhất
            └── update.zip          ← File zip chứa bản update
```

### File `version.txt`:
```
1.0.1
```
Chỉ chứa số version, VD: `1.0.1`, `2.3.0`, etc.

### File `update.zip`:
Nén các file sau:
```
update.zip
├── Check_All_Stage.exe
├── version.txt
└── (các file khác cần update)
```

## 🔧 Cách sử dụng

### 1. Trong Settings UI:

1. Mở chương trình
2. Click **⚙️ Settings**
3. Tìm section **🌐 FTP UPDATE SETTINGS**
4. Nhập thông tin FTP của bạn
5. Click **💾 SAVE**
6. Restart app

### 2. Trong code (Check_All_Stage.py):

```python
from utils.config_manager import get_ftp_settings

# Lấy FTP settings
FTP_SETTINGS = get_ftp_settings()

# Sử dụng
server = FTP_SETTINGS['server']       # '10.62.102.5'
user = FTP_SETTINGS['user']           # 'update'
password = FTP_SETTINGS['password']   # 'update'
directory = FTP_SETTINGS['directory'] # 'KhanhDQ/...'

# Build FTP URL
version_url = f"ftp://{user}:{password}@{server}/{directory}version.txt"
```

### 3. Trong update_script.py:

```python
from ftplib import FTP
import json

# Load settings từ config.json
with open('config.json') as f:
    config = json.load(f)

settings = config['program_settings']

# Connect to FTP
ftp = FTP(settings['ftp_server'])
ftp.login(settings['ftp_user'], settings['ftp_password'])
ftp.cwd(settings['ftp_directory'])

# Download files
ftp.retrbinary('RETR version.txt', open('version.txt', 'wb').write)
ftp.retrbinary('RETR update.zip', open('update.zip', 'wb').write)
```

## 🔄 Migration tự động

Config cũ sẽ **tự động** chuyển sang format mới khi app khởi động:

### Before:
```json
{
  "program_settings": {
    "ftp_base_url": "ftp://user:pass@192.168.1.100/path/to/update/"
  }
}
```

### After (tự động):
```json
{
  "program_settings": {
    "ftp_server": "192.168.1.100",
    "ftp_user": "user",
    "ftp_password": "pass",
    "ftp_directory": "path/to/update/"
  }
}
```

## 🧪 Test FTP Connection

### Từ Settings UI:
1. Mở Settings
2. Cấu hình FTP settings
3. Click **💾 SAVE**
4. App sẽ thử kết nối khi check update

### Manual test với Python:
```python
from ftplib import FTP

try:
    ftp = FTP('10.62.102.5')
    ftp.login('update', 'update')
    ftp.cwd('KhanhDQ/Update_Program/Check_All_Stage/')
    files = ftp.nlst()
    print("Files:", files)
    ftp.quit()
    print("✓ Connection successful!")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

## 🔐 Security Notes

- ⚠️ Password lưu dạng **plain text** trong config.json
- 🔒 Không chia sẻ file config.json
- 🛡️ Giới hạn quyền truy cập FTP server
- 📝 Thường xuyên đổi password FTP

## 📊 Ví dụ cấu hình thực tế

### Production:
```json
{
  "program_settings": {
    "ftp_server": "10.62.102.5",
    "ftp_user": "update_prod",
    "ftp_password": "SecurePass123!",
    "ftp_directory": "Production/Check_All_Stage/"
  }
}
```

### Testing:
```json
{
  "program_settings": {
    "ftp_server": "192.168.1.100",
    "ftp_user": "test_user",
    "ftp_password": "testpass",
    "ftp_directory": "Testing/Check_All_Stage/"
  }
}
```

### Local development:
```json
{
  "program_settings": {
    "ftp_server": "localhost",
    "ftp_user": "dev",
    "ftp_password": "dev",
    "ftp_directory": "dev/updates/"
  }
}
```

## 🐛 Troubleshooting

### Lỗi: "Cannot connect to FTP server"
✅ Kiểm tra:
- FTP Server có chạy không?
- IP/hostname đúng chưa?
- Firewall có chặn port 21 không?

### Lỗi: "Login failed"
✅ Kiểm tra:
- Username/password đúng chưa?
- User có quyền truy cập không?

### Lỗi: "Directory not found"
✅ Kiểm tra:
- Đường dẫn directory đúng chưa?
- User có quyền vào thư mục đó không?
- Thư mục có tồn tại trên server không?

### Lỗi: "File not found"
✅ Kiểm tra:
- File `version.txt` có trong thư mục không?
- File `update.zip` có trong thư mục không?
- Tên file đúng chính xác không? (case-sensitive)

---

**© 2025 ITM Semiconductor Vietnam**
