# 📘 DATABASE CONFIGURATION GUIDE

## ⚠️ IMPORTANT: Migrated from cx_Oracle to python-oracledb

**Date: December 3, 2025**  
The application has been migrated from `cx_Oracle` to `python-oracledb` (thin mode) for better compatibility with Oracle servers, especially those using JDBC-like connections.

### 🔄 Migration Benefits:
- ✅ **Pure Python** - No Oracle Instant Client needed
- ✅ **Cross-platform** - Works on Windows/Linux/Mac without native libraries
- ✅ **JDBC-compatible** - Same behavior as DBeaver/ojdbc8
- ✅ **No ORA-12637 errors** - Resolves packet receive failures
- ✅ **Easier deployment** - Just `pip install oracledb`

---

## Thay đổi thông tin kết nối Database

### ⚙️ File cần sửa:
```
utils/db_config.py
```

### 📝 Các thông số có thể thay đổi:

#### 1. **Thay đổi IP Address của Database Server:**
```python
# Dòng 6-12 trong utils/db_config.py
DB_CONFIG = {
    'user': 'mighty',
    'password': 'mighty',
    'host': '10.162.200.20',  # ← Thay đổi IP ở đây
    'port': 1521,              # ← Thay đổi port nếu cần
    'service_name': 'ITMVPACKMES'  # ← Service name của Oracle
}
```

#### 2. **Thay đổi Username/Password:**
```python
DB_CONFIG = {
    'user': 'mighty',         # ← Thay đổi username
    'password': 'mighty',     # ← Thay đổi password
    'host': '10.162.200.20',
    'port': 1521,
    'service_name': 'ITMVPACKMES'
}
```

#### 3. **Thay đổi Service Name hoặc SID:**
```python
# Option A: Using Service Name (recommended)
DB_CONFIG = {
    'user': 'mighty',
    'password': 'mighty',
    'host': '10.162.200.20',
    'port': 1521,
    'service_name': 'ITMVPACKMES'  # ← Service name
}

# Option B: Using SID (if needed)
DB_CONFIG = {
    'user': 'mighty',
    'password': 'mighty',
    'host': '10.162.200.20',
    'port': 1521,
    'sid': 'ORCL'  # ← Use 'sid' instead of 'service_name'
}
```

### ✅ Ưu điểm của centralized config:
- ✓ **Chỉ sửa 1 file duy nhất** (utils/db_config.py) thay vì sửa 20+ files
- ✓ **Dễ maintenance** - Tất cả connection đều sử dụng cùng config
- ✓ **Giảm lỗi** - Không lo sót file nào khi thay đổi
- ✓ **Consistent** - Đảm bảo tất cả modules đều dùng cùng connection info

### 🔧 Ví dụ thay đổi IP từ 192.168.35.20 → 192.168.35.30:

**Trước:**
```python
'dsn': '(DESCRIPTION=(LOAD_BALANCE=yes)(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.35.20)(PORT=1521))...'
```

**Sau:**
```python
'dsn': '(DESCRIPTION=(LOAD_BALANCE=yes)(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.35.30)(PORT=1521))...'
```

### 📋 Danh sách các module đã được refactor:
✓ calibration.py
✓ cartridge.py
✓ charge.py
✓ final.py
✓ firmware.py
✓ get_mcu_id.py
✓ heater.py
✓ heater_module.py
✓ inductive.py
✓ lcdled.py
✓ leak.py
✓ matching.py
✓ Packing.py
✓ pba.py
✓ puffing.py
✓ sensor.py
✓ sleep.py
✓ smart_mmi.py
✓ snwriting.py
✓ verification.py
✓ weigh.py
✓ Check_All_Stage.py (login function)

### 🚀 Restart sau khi thay đổi:
Sau khi sửa `utils/db_config.py`, cần **restart chương trình** để áp dụng thay đổi.

---
📅 Refactored: December 3, 2025
🔧 Refactoring Tool: refactor_db_connections.py
