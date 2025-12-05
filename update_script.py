import os
import sys
import zipfile
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from ftplib import FTP
import json

def get_app_directory():
    """Get application directory (works for both .py and .exe)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def load_settings():
    """Load settings from config.json or use defaults"""
    try:
        app_dir = get_app_directory()
        settings_path = os.path.join(app_dir, 'config.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Extract program_settings
                return config.get('program_settings', {})
    except Exception as e:
        print(f"Failed to load settings: {e}, using defaults")
    
    # Return default settings
    return {
        'program_directory': 'C:\\Check_All_Stage',
        'ftp_server': '10.62.102.5',
        'ftp_user': 'update',
        'ftp_password': 'update',
        'ftp_directory': 'KhanhDQ/Update_Program/Check_All_Stage/'
    }

# Load settings
settings = load_settings()

# Đường dẫn tới thư mục chứa các file chương trình
PROGRAM_DIRECTORY = settings.get('program_directory', 'C:\\Check_All_Stage')
CURRENT_VERSION_FILE = os.path.join(PROGRAM_DIRECTORY, "version.txt")
MAIN_EXECUTABLE = os.path.join(PROGRAM_DIRECTORY, "Check_All_Stage.exe")
UPDATE_ZIP_PATH = os.path.join(PROGRAM_DIRECTORY, "update.zip")
VERSION_FLAG_FILE = os.path.join(PROGRAM_DIRECTORY, "version_flag.txt")

# Đường dẫn tới FTP Server
FTP_SERVER = settings.get('ftp_server', '10.62.102.5')
FTP_USER = settings.get('ftp_user', 'update')
FTP_PASS = settings.get('ftp_password', 'update')
FTP_DIRECTORY = settings.get('ftp_directory', 'KhanhDQ/Update_Program/Check_All_Stage/')

def get_current_version():
    """Get current version from version flag file"""
    if os.path.exists(VERSION_FLAG_FILE):
        with open(VERSION_FLAG_FILE, "r") as file:
            return file.read().strip()
    return "0.0.0"

def set_current_version(version):
    """Save current version to flag file"""
    with open(VERSION_FLAG_FILE, "w") as file:
        file.write(version)

def update_version_file(new_version):
    """Update version.txt file"""
    with open(CURRENT_VERSION_FILE, "w") as file:
        file.write(new_version)

def compare_versions(version1, version2):
    """Compare two version strings (e.g., '1.0.0' vs '1.0.1')"""
    try:
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        # Pad with zeros if needed
        while len(v1_parts) < len(v2_parts):
            v1_parts.append(0)
        while len(v2_parts) < len(v1_parts):
            v2_parts.append(0)
        
        # Compare
        for v1, v2 in zip(v1_parts, v2_parts):
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0
    except:
        # Fallback to string comparison
        if version1 > version2:
            return 1
        elif version1 < version2:
            return -1
        return 0

def get_latest_version():
    """Get latest version from FTP server"""
    temp_file = "latest_version.txt"
    try:
        ftp = FTP(FTP_SERVER)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_DIRECTORY)
        
        with open(temp_file, "wb") as file:
            ftp.retrbinary("RETR version.txt", file.write)
        ftp.quit()
        
        with open(temp_file, "r") as file:
            latest_version = file.read().strip()
        
        os.remove(temp_file)
        return latest_version
    except Exception as e:
        print(f"Không thể lấy phiên bản mới nhất: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return None

def download_update(progress_var):
    """Download update.zip from FTP server with progress"""
    try:
        ftp = FTP(FTP_SERVER)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.cwd(FTP_DIRECTORY)
        
        total_size = ftp.size("update.zip")
        block_size = 8192
        downloaded_size = 0
        
        with open(UPDATE_ZIP_PATH, 'wb') as file:
            def callback(data):
                nonlocal downloaded_size
                file.write(data)
                downloaded_size += len(data)
                percent = min(100, round(downloaded_size * 100 / total_size))
                progress_var.set(percent)
                root.update_idletasks()
            
            ftp.retrbinary("RETR update.zip", callback, block_size)
        
        ftp.quit()
        print("Tải bản cập nhật thành công.")
        return True
    except Exception as e:
        print(f"Không thể tải bản cập nhật: {e}")
        messagebox.showerror("Lỗi", f"Không thể tải bản cập nhật!\n\nChi tiết: {str(e)}")
        return False

def apply_update():
    """Extract update.zip to program directory"""
    try:
        print("Đang giải nén file cập nhật...")
        with zipfile.ZipFile(UPDATE_ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(PROGRAM_DIRECTORY)
        
        # Clean up
        if os.path.exists(UPDATE_ZIP_PATH):
            os.remove(UPDATE_ZIP_PATH)
        
        print("Cập nhật hoàn tất.")
        return True
    except Exception as e:
        print(f"Lỗi khi thực hiện cập nhật: {e}")
        messagebox.showerror("Lỗi", f"Không thể giải nén bản cập nhật!\n\nChi tiết: {str(e)}")
        return False

def restart_program(root):
    try:
        if os.path.exists(MAIN_EXECUTABLE):
            process = subprocess.Popen([MAIN_EXECUTABLE])
            print(f"Đã khởi chạy lại chương trình, PID: {process.pid}")
            close_window(root)
            sys.exit()
        else:
            print(f"Không tìm thấy tệp {MAIN_EXECUTABLE}")
            messagebox.showerror("Lỗi", f"Không tìm thấy tệp {MAIN_EXECUTABLE}")
    except Exception as e:
        print(f"Lỗi khi khởi động lại chương trình: {e}")
        messagebox.showerror("Lỗi", f"Lỗi khi khởi động lại chương trình: {e}")

def show_update_window(update_action):
    global root
    root = tk.Tk()
    root.title("Đang cập nhật")
    root.geometry("420x150")
    root.resizable(False, False) 
    
    label = tk.Label(root, text="Đang thực hiện cập nhật...", font=("Arial", 14))
    label.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", variable=progress_var, maximum=100)
    progress.pack(side="left", padx=(10, 0))
    
    percent_label = tk.Label(frame, text="0%", font=("Arial", 14))
    percent_label.pack(side="left", padx=(10, 0))
    def update_percent_label(*args):
        percent_label.config(text=f"{progress_var.get()}%")
    progress_var.trace("w", update_percent_label)


    def run_update():
        update_action(root, progress_var)
    
    threading.Thread(target=run_update).start()
    root.mainloop()

def close_window(root):
    root.destroy()

if __name__ == "__main__":
    def update_action(root, progress_var):
        """Main update logic"""
        try:
            # Check if version file exists
            if not os.path.exists(CURRENT_VERSION_FILE):
                messagebox.showerror("Lỗi", "Không tìm thấy tệp version.txt. Hãy kiểm tra lại!")
                close_window(root)
                sys.exit()

            # Download update
            if not download_update(progress_var):
                close_window(root)
                sys.exit()
            
            # Get version info from downloaded zip
            new_version = "0.0.0"
            try:
                with zipfile.ZipFile(UPDATE_ZIP_PATH, 'r') as zip_ref:
                    new_version_file = zip_ref.open('version.txt')
                    new_version = new_version_file.read().decode('utf-8').strip()
                    new_version_file.close()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lấy thông tin phiên bản từ Server!\n\nChi tiết: {str(e)}")
                close_window(root)
                sys.exit()
            
            # Compare versions
            current_version = get_current_version()
            
            # Check if update is needed
            if compare_versions(new_version, current_version) > 0:
                # New version is greater
                time.sleep(1)
                
                if not apply_update():
                    close_window(root)
                    sys.exit()
                
                # Update version files
                update_version_file(new_version)
                set_current_version(new_version)
                
                messagebox.showinfo("Thành công", f"Cập nhật thành công lên phiên bản {new_version}!")
                restart_program(root)
            else:
                # Already up to date
                messagebox.showinfo("Thông báo", f"Chương trình đã ở phiên bản mới nhất ({current_version}).")
                restart_program(root)
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi trong quá trình cập nhật:\n\n{str(e)}")
            close_window(root)
            sys.exit()
    
    show_update_window(update_action)
