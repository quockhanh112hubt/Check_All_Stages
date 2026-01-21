import urllib.request
import subprocess
import os
import configparser
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from ui.creategui_P230_v2 import create_gui_P230_v2
from ui.creategui_P4_v2 import create_gui_P4_v2
from ui.creategui_P1_v2 import create_gui_P1_v2
from ui.creategui_P140_v2 import create_gui_P140_v2
from utils.utils import get_current_version
from utils.db_config import get_db_connection
from utils.config_manager import get_program_directory, get_ftp_settings
import qrcode
from PIL import Image, ImageTk

# Đường dẫn tới thư mục chứa các file chương trình (loaded from config.json)
PROGRAM_DIRECTORY = get_program_directory()
UPDATE_SCRIPT_EXECUTABLE = os.path.join(PROGRAM_DIRECTORY, "update_script.exe")

# Đường dẫn tới FTP Server (loaded from config.json)
FTP_SETTINGS = get_ftp_settings()
VERSION_URL = f"ftp://{FTP_SETTINGS['user']}:{FTP_SETTINGS['password']}@{FTP_SETTINGS['server']}/{FTP_SETTINGS['directory']}version.txt"

def save_login_info(username, password):
    config = configparser.ConfigParser()
    config['LOGIN'] = {'username': username, 'password': password}
    with open('login_info.ini', 'w') as configfile:
        config.write(configfile)

def load_login_info():
    config = configparser.ConfigParser()
    config.read('login_info.ini')
    if 'LOGIN' in config:
        return config['LOGIN']['username'], config['LOGIN']['password']
    return None, None


def create_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

def forgot_password():
    # Tạo QR code
    contact_info = "https://zalo.me/0944187335"
    qr_code_path = "contact_info_qr.png"
    create_qr_code(contact_info, qr_code_path)

    # Tạo cửa sổ thông báo
    popup = tk.Toplevel()
    popup.title("Forgot Password")
    popup.geometry("450x450")
    popup.resizable(False, False)

    # Hiển thị thông báo
    message = tk.Label(popup, text="Hãy liên hệ Khánh IT để reset mật khẩu của bạn!\n", font=("Arial Bold", 12), wraplength=280, justify="center")
    message.pack(pady=10)

    # Hiển thị QR code
    qr_image = Image.open(qr_code_path)
    qr_photo = ImageTk.PhotoImage(qr_image)
    qr_label = tk.Label(popup, image=qr_photo)
    qr_label.image = qr_photo  # Lưu tham chiếu để tránh bị garbage collected
    qr_label.pack(pady=10)

    # Nút đóng cửa sổ
    close_button = tk.Button(popup, text="CLOSE", command=popup.destroy, bg='#00796b', fg='#CCFFFF', font=("Arial", 12))
    close_button.place(relx=0.5, y=350, anchor='center', width=120, height=30)

    popup.mainloop()


def open_settings():
    """Mở cửa sổ cài đặt"""
    from utils.config_manager import load_config, save_config
    
    config = load_config()
    
    # Tạo cửa sổ settings
    settings_window = tk.Toplevel()
    settings_window.title("Settings - Cài đặt hệ thống")
    settings_window.geometry("700x770")
    settings_window.resizable(False, False)
    settings_window.configure(bg='#003366')
    
    # Làm cho cửa sổ settings thành modal (chỉ mở được 1 cái và phải đóng nó trước)
    settings_window.transient(root)  # Gắn vào cửa sổ root
    settings_window.grab_set()  # Chặn tương tác với cửa sổ khác
    settings_window.focus_set()  # Focus vào cửa sổ settings
    
    # Title
    title = tk.Label(settings_window, text="⚙️ SYSTEM SETTINGS", fg='#66CCFF', bg='#003366', font=("Arial Black", 16))
    title.pack(pady=20)
    
    # Frame chính
    main_frame = tk.Frame(settings_window, bg='#003366')
    main_frame.pack(padx=20, pady=10, fill='both', expand=True)
    
    # --- Program Settings ---
    program_label = tk.Label(main_frame, text="📁 PROGRAM SETTINGS", fg='#66CCFF', bg='#003366', font=("Arial Bold", 12))
    program_label.pack(anchor='w', pady=(10, 5))
    
    # Program Directory
    prog_dir_frame = tk.Frame(main_frame, bg='#e0f7fa', bd=1, relief='solid')
    prog_dir_frame.pack(fill='x', pady=5)
    tk.Label(prog_dir_frame, text="Program Directory:", bg='#e0f7fa', font=("Arial", 10)).pack(anchor='w', padx=5, pady=2)
    prog_dir_entry = tk.Entry(prog_dir_frame, bd=0, bg='white', font=("Arial", 10))
    prog_dir_entry.pack(fill='x', padx=5, pady=2)
    prog_dir_entry.insert(0, config['program_settings']['program_directory'])
    
    # FTP Settings Section
    ftp_label = tk.Label(main_frame, text="🌐 FTP UPDATE SETTINGS", fg='#66CCFF', bg='#003366', font=("Arial Bold", 12))
    ftp_label.pack(anchor='w', pady=(10, 5))
    
    ftp_entries = {}
    
    # FTP Server
    ftp_server_frame = tk.Frame(main_frame, bg='#e0f7fa', bd=1, relief='solid')
    ftp_server_frame.pack(fill='x', pady=3)
    tk.Label(ftp_server_frame, text="FTP Server:", bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
    ftp_server_entry = tk.Entry(ftp_server_frame, bd=0, bg='white', font=("Arial", 10))
    ftp_server_entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
    ftp_server_entry.insert(0, config['program_settings'].get('ftp_server', '10.62.102.5'))
    ftp_entries['server'] = ftp_server_entry
    
    # FTP User
    ftp_user_frame = tk.Frame(main_frame, bg='#e0f7fa', bd=1, relief='solid')
    ftp_user_frame.pack(fill='x', pady=3)
    tk.Label(ftp_user_frame, text="FTP User:", bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
    ftp_user_entry = tk.Entry(ftp_user_frame, bd=0, bg='white', font=("Arial", 10))
    ftp_user_entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
    ftp_user_entry.insert(0, config['program_settings'].get('ftp_user', 'update'))
    ftp_entries['user'] = ftp_user_entry
    
    # FTP Password
    ftp_pass_frame = tk.Frame(main_frame, bg='#e0f7fa', bd=1, relief='solid')
    ftp_pass_frame.pack(fill='x', pady=3)
    tk.Label(ftp_pass_frame, text="FTP Password:", bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
    ftp_pass_entry = tk.Entry(ftp_pass_frame, bd=0, bg='white', font=("Arial", 10), show='*')
    ftp_pass_entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
    ftp_pass_entry.insert(0, config['program_settings'].get('ftp_password', 'update'))
    ftp_entries['password'] = ftp_pass_entry
    
    # FTP Directory
    ftp_dir_frame = tk.Frame(main_frame, bg='#e0f7fa', bd=1, relief='solid')
    ftp_dir_frame.pack(fill='x', pady=3)
    tk.Label(ftp_dir_frame, text="FTP Directory:", bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
    ftp_dir_entry = tk.Entry(ftp_dir_frame, bd=0, bg='white', font=("Arial", 10))
    ftp_dir_entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
    ftp_dir_entry.insert(0, config['program_settings'].get('ftp_directory', 'KhanhDQ/Update_Program/Check_All_Stage/'))
    ftp_entries['directory'] = ftp_dir_entry
    
    # --- Database Settings ---
    db_label = tk.Label(main_frame, text="💾 DATABASE SETTINGS", fg='#66CCFF', bg='#003366', font=("Arial Bold", 12))
    db_label.pack(anchor='w', pady=(15, 5))
    
    # Connection Type Selection
    conn_type_frame = tk.Frame(main_frame, bg='#e0f7fa', bd=1, relief='solid')
    conn_type_frame.pack(fill='x', pady=5)
    tk.Label(conn_type_frame, text="Connection Type:", bg='#e0f7fa', font=("Arial Bold", 10)).pack(anchor='w', padx=5, pady=2)
    
    conn_type_var = tk.StringVar(value=config['database_settings'].get('connection_type', 'oracledb'))
    
    radio_frame = tk.Frame(conn_type_frame, bg='#e0f7fa')
    radio_frame.pack(anchor='w', padx=20, pady=5)
    tk.Radiobutton(radio_frame, text="oracledb (Thin Mode - No Client Needed)", variable=conn_type_var, 
                   value='oracledb', bg='#e0f7fa', font=("Arial", 10)).pack(anchor='w')
    tk.Radiobutton(radio_frame, text="cx_Oracle (Requires Oracle Client)", variable=conn_type_var, 
                   value='cx_oracle', bg='#e0f7fa', font=("Arial", 10)).pack(anchor='w')
    
    # Container frame for database config (will switch based on connection type)
    db_config_container = tk.Frame(main_frame, bg='#003366')
    db_config_container.pack(fill='x', pady=5)
    
    # Variables to hold entry widgets
    db_entries = {}
    
    def show_oracledb_config():
        """Show oracledb configuration fields"""
        # Clear container
        for widget in db_config_container.winfo_children():
            widget.destroy()
        
        db_entries.clear()
        oracle_config = config['database_settings'].get('oracledb', {})
        
        fields = [
            ('User:', 'user'),
            ('Password:', 'password'),
            ('Host:', 'host'),
            ('Port:', 'port'),
            ('Service Name:', 'service_name')
        ]
        
        for label_text, field_name in fields:
            field_frame = tk.Frame(db_config_container, bg='#e0f7fa', bd=1, relief='solid')
            field_frame.pack(fill='x', pady=3)
            tk.Label(field_frame, text=label_text, bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
            entry = tk.Entry(field_frame, bd=0, bg='white', font=("Arial", 10))
            entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
            
            if field_name == 'password':
                entry.config(show='*')
            
            entry.insert(0, str(oracle_config.get(field_name, '')))
            db_entries[field_name] = entry
    
    def show_cx_oracle_config():
        """Show cx_Oracle configuration fields"""
        # Clear container
        for widget in db_config_container.winfo_children():
            widget.destroy()
        
        db_entries.clear()
        cx_config = config['database_settings'].get('cx_oracle', {})
        
        # User
        field_frame = tk.Frame(db_config_container, bg='#e0f7fa', bd=1, relief='solid')
        field_frame.pack(fill='x', pady=3)
        tk.Label(field_frame, text="User:", bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
        user_entry = tk.Entry(field_frame, bd=0, bg='white', font=("Arial", 10))
        user_entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
        user_entry.insert(0, cx_config.get('user', ''))
        db_entries['user'] = user_entry
        
        # Password
        field_frame = tk.Frame(db_config_container, bg='#e0f7fa', bd=1, relief='solid')
        field_frame.pack(fill='x', pady=3)
        tk.Label(field_frame, text="Password:", bg='#e0f7fa', font=("Arial", 10), width=15, anchor='w').pack(side='left', padx=5, pady=2)
        pass_entry = tk.Entry(field_frame, bd=0, bg='white', font=("Arial", 10), show='*')
        pass_entry.pack(side='left', fill='x', expand=True, padx=5, pady=2)
        pass_entry.insert(0, cx_config.get('password', ''))
        db_entries['password'] = pass_entry
        
        # DSN (multi-line)
        dsn_frame = tk.Frame(db_config_container, bg='#e0f7fa', bd=1, relief='solid')
        dsn_frame.pack(fill='x', pady=3)
        tk.Label(dsn_frame, text="DSN String:", bg='#e0f7fa', font=("Arial Bold", 10)).pack(anchor='w', padx=5, pady=2)
        dsn_text = tk.Text(dsn_frame, bd=0, bg='white', font=("Courier New", 9), height=4, wrap='word')
        dsn_text.pack(fill='x', padx=5, pady=2)
        dsn_text.insert('1.0', cx_config.get('dsn', ''))
        db_entries['dsn'] = dsn_text
    
    def on_connection_type_change():
        """Handle connection type radio button change"""
        if conn_type_var.get() == 'oracledb':
            show_oracledb_config()
        else:
            show_cx_oracle_config()
    
    # Bind radio buttons to change handler
    conn_type_var.trace('w', lambda *args: on_connection_type_change())
    
    # Show initial config
    on_connection_type_change()
    
    # Buttons frame
    button_frame = tk.Frame(settings_window, bg='#003366')
    button_frame.pack(pady=20)
    
    def save_settings():
        """Lưu cài đặt vào file config.json"""
        try:
            connection_type = conn_type_var.get()
            
            # Build database settings based on connection type
            if connection_type == 'oracledb':
                db_settings = {
                    "connection_type": "oracledb",
                    "oracledb": {
                        "user": db_entries['user'].get(),
                        "password": db_entries['password'].get(),
                        "host": db_entries['host'].get(),
                        "port": int(db_entries['port'].get()),
                        "service_name": db_entries['service_name'].get()
                    },
                    "cx_oracle": config['database_settings'].get('cx_oracle', {})
                }
            else:  # cx_oracle
                dsn_value = db_entries['dsn'].get('1.0', 'end-1c').strip()
                db_settings = {
                    "connection_type": "cx_oracle",
                    "oracledb": config['database_settings'].get('oracledb', {}),
                    "cx_oracle": {
                        "user": db_entries['user'].get(),
                        "password": db_entries['password'].get(),
                        "dsn": dsn_value
                    }
                }
            
            new_config = {
                "program_settings": {
                    "program_directory": prog_dir_entry.get(),
                    "ftp_server": ftp_entries['server'].get(),
                    "ftp_user": ftp_entries['user'].get(),
                    "ftp_password": ftp_entries['password'].get(),
                    "ftp_directory": ftp_entries['directory'].get()
                },
                "database_settings": db_settings
            }
            
            if save_config(new_config):
                messagebox.showinfo("Success", "Settings saved successfully!\n\nPlease restart the application for changes to take effect.")
                settings_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to save settings!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")
    
    def test_connection():
        """Test database connection với cài đặt hiện tại"""
        try:
            connection_type = conn_type_var.get()
            
            if connection_type == 'oracledb':
                import oracledb
                test_config = {
                    'user': db_entries['user'].get(),
                    'password': db_entries['password'].get(),
                    'host': db_entries['host'].get(),
                    'port': int(db_entries['port'].get()),
                    'service_name': db_entries['service_name'].get()
                }
                
                connection = oracledb.connect(
                    user=test_config['user'],
                    password=test_config['password'],
                    host=test_config['host'],
                    port=test_config['port'],
                    service_name=test_config['service_name']
                )
                connection.close()
                messagebox.showinfo("Success", "✓ oracledb connection successful!")
            else:  # cx_oracle
                import cx_Oracle
                test_config = {
                    'user': db_entries['user'].get(),
                    'password': db_entries['password'].get(),
                    'dsn': db_entries['dsn'].get('1.0', 'end-1c').strip()
                }
                
                connection = cx_Oracle.connect(
                    user=test_config['user'],
                    password=test_config['password'],
                    dsn=test_config['dsn']
                )
                connection.close()
                messagebox.showinfo("Success", "✓ cx_Oracle connection successful!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"✗ Connection failed:\n{str(e)}")
    
    # Save button
    save_btn = tk.Button(button_frame, text="💾 SAVE", command=save_settings, 
                        bg='#00796b', fg='white', font=("Arial", 12), width=12)
    save_btn.pack(side='left', padx=10)
    
    # Test connection button
    test_btn = tk.Button(button_frame, text="🔌 TEST DB", command=test_connection, 
                        bg='#0277bd', fg='white', font=("Arial", 12), width=12)
    test_btn.pack(side='left', padx=10)
    
    # Cancel button
    cancel_btn = tk.Button(button_frame, text="✖ CANCEL", command=settings_window.destroy, 
                          bg='#c62828', fg='white', font=("Arial", 12), width=12)
    cancel_btn.pack(side='left', padx=10)


def connect_to_oracle():
    connection = get_db_connection()
    return connection

def login():
    username = entry_username.get()
    password = entry_password.get()
    selected_option = option_var.get()
    remember_me_checked = remember_me_var.get()

    connection = connect_to_oracle()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM USER_DATA WHERE USERNAME = :1 AND PASSWORD = :2", (username, password))
    user = cursor.fetchone()
    connection.close()

    if user:
        if remember_me_checked:
            save_login_info(username, password)
        else:
            save_login_info("", "")
        
        root.destroy()
        
        if selected_option == "ECIGA-P1EZ":
            create_gui_P1_v2(create_login_ui, create_gui_P230_v2, create_gui_P4_v2, create_gui_P140_v2)
        elif selected_option == "ECIGA-P2 3.0":
            create_gui_P230_v2(create_login_ui, create_gui_P1_v2, create_gui_P4_v2, create_gui_P140_v2)
        elif selected_option == "ECIGA-P4":
            create_gui_P4_v2(create_login_ui, create_gui_P1_v2, create_gui_P230_v2, create_gui_P140_v2)
        elif selected_option == "ECIGA-P140":
            create_gui_P140_v2(create_login_ui, create_gui_P1_v2, create_gui_P230_v2, create_gui_P4_v2)
    else:
        messagebox.showerror("Thông báo", "Sai tên đăng nhập hoặc mật khẩu.")


def get_latest_version():
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            latest_version = response.read().decode('utf-8').strip()
        return latest_version
    except Exception as e:
        print(f"Không thể lấy phiên bản mới nhất: {e}")
        return None

def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()
    
    if latest_version and latest_version > current_version:
        initiate_update()

def initiate_update():
    print("Đang chuẩn bị cập nhật và khởi động lại chương trình...")
    process = subprocess.Popen([UPDATE_SCRIPT_EXECUTABLE])
    print(f"Đã khởi chạy {UPDATE_SCRIPT_EXECUTABLE}, PID: {process.pid}")
    sys.exit()

def cancel():
    root.destroy
    sys.exit()

def create_login_ui():
    global root, entry_username, entry_password, option_var, remember_me_var

    root = tk.Tk()
    root.title(f"Each Stage Data Checker Version {get_current_version()}")
    root.geometry("800x550")
    root.configure(bg='#00a99d')
    root.resizable(False, False)

    # Tải ảnh nền
    background_image = Image.open("Resource/background.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    canvas = tk.Canvas(root, width=400, height=450)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    # Nút Settings ở góc trên bên phải
    settings_btn = tk.Button(root, text="⚙️ Settings", command=open_settings, 
                            bg='#0277bd', fg='white', font=("Arial", 10, "bold"), 
                            cursor="hand2", relief='raised', bd=2)
    settings_btn.place(x=690, y=10, width=100, height=35)

    # Frame chính giữa
    frame = tk.Frame(root, bg='#003366', bd=0)
    frame.place(relx=0.5, rely=0.5, anchor='center', width=350, height=400)

    # Icon người dùng
    user_name = tk.Label(frame, bg='#003366', text="CHECK_ALL_STAGE", fg='#66CCFF', font=("Arial Black", 18))
    user_name.place(relx=0.5, y=15, anchor='center')
    user_icon = tk.Label(frame, bg='#003366', text="ITM Semiconductor Vietnam", fg='#66CCFF', font=("Cascadia Mono SemiBold", 9))
    user_icon.place(relx=0.5, y=40, anchor='center')

    # Tiêu đề đăng nhập
    title = tk.Label(frame, text="LOGIN", fg='#66CCFF', bg='#003366', font=("Arial Black", 16))
    title.place(relx=0.5, y=80, anchor='center')

    # Tên đăng nhập
    username_frame = tk.Frame(frame, bg='#e0f7fa', bd=1, relief='solid')
    username_frame.place(relx=0.5, y=120, anchor='center', width=300, height=40)
    user_icon_label = tk.Label(username_frame, text="👤", bg='#e0f7fa', font=("Arial", 18))
    user_icon_label.place(x=10, y=5, width=30, height=30)
    entry_username = tk.Entry(username_frame, bd=0, bg='#e0f7fa', font=("Arial", 12))
    entry_username.place(x=50, y=5, width=240, height=30)

    # Mật khẩu
    password_frame = tk.Frame(frame, bg='#e0f7fa', bd=1, relief='solid')
    password_frame.place(relx=0.5, y=170, anchor='center', width=300, height=40)
    pass_icon_label = tk.Label(password_frame, text="🔒", bg='#e0f7fa', font=("Arial", 18))
    pass_icon_label.place(x=10, y=5, width=30, height=30)
    entry_password = tk.Entry(password_frame, show="*", bd=0, bg='#e0f7fa', font=("Arial", 12))
    entry_password.place(x=50, y=5, width=240, height=30)

    # Tạo combobox cho các lựa chọn
    option_var = tk.StringVar()
    option_frame = tk.Frame(frame, bg='#e0f7fa', bd=1, relief='solid')
    option_frame.place(relx=0.5, y=220, anchor='center', width=300, height=40)
    combo = ttk.Combobox(option_frame, textvariable=option_var, font=("Arial", 12), state="readonly")
    combo['values'] = ("ECIGA-P1EZ", "ECIGA-P2 3.0", "ECIGA-P4", "ECIGA-P140")
    combo.place(relx=0.5, rely=0.5, anchor='center', width=240, height=30)
    combo.current(3)

    # Nút đăng nhập
    login_button = tk.Button(frame, text="LOGIN", command=login, bg='#00796b', fg='#003366', font=("Arial", 14))
    login_button.place(relx=0.5, y=270, anchor='center', width=150, height=40)
    root.bind('<Return>', lambda event: login())

    # Các tùy chọn bổ sung (ví dụ như ghi nhớ đăng nhập, quên mật khẩu)
    additional_options = tk.Frame(frame, bg='#CCFFFF')
    additional_options.place(relx=0.5, y=360, anchor='center', width=300, height=40)

    # Remember me
    remember_me_var = tk.BooleanVar()
    remember_me = tk.Checkbutton(additional_options, text="Remember me", variable=remember_me_var, bg='#CCFFFF')
    remember_me.pack(side="left", padx=10)

    # Forgot password
    forgot_password_label = tk.Label(additional_options, text="Forgot password?", fg='#00796b', bg='#CCFFFF', cursor="hand2")
    forgot_password_label.pack(side="right", padx=10)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    # Load saved login info
    saved_username, saved_password = load_login_info()
    if saved_username and saved_password:
        entry_username.insert(0, saved_username)
        entry_password.insert(0, saved_password)
        remember_me_var.set(True)

    root.mainloop()


if __name__ == "__main__":
    check_for_updates()
    create_login_ui()

