import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
from utils.log import log_message
from utils.date import format_trans_time
from utils.utils import get_current_version, get_data_path
from utils.Checkping import check_ping
from utils.thread_utils import StageChecker, BackgroundTask
from data.pba import get_data_pba_function_P4
from data.firmware import get_data_firmware_P4
from data.heater import get_data_heater_P4, get_heater_id_P4
from data.leak import get_data_leak_P4
from data.matching import get_data_matching_P4, get_main_pba_P4
from data.sleep import get_data_sleep_P4
from data.lcdled import get_data_display_P4
from data.charge import get_data_charge_P4
from data.calibration import get_data_cali_P4
from data.verification import get_data_verifi_P4
from data.puffing import get_data_puffing_P4
from data.sensor import get_data_optical_cali_P4
from data.snwriting import get_data_snwriting_P4
from data.final import get_data_final_P4
from data.Packing import *
from data.weigh import get_data_weigh
from data.get_mcu_id import get_device_id_P4
from PIL import Image, ImageTk

# Corporate color scheme
COLORS = {
    'primary': '#1e3a8a',
    'secondary': '#2563eb',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'light': '#f1f5f9',
    'dark': '#1e293b',
    'white': '#ffffff',
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'border': '#e2e8f0',
    'hover': '#dbeafe'
}

class ModernStageCard(tk.Frame):
    def __init__(self, parent, stage_name, **kwargs):
        super().__init__(parent, bg=COLORS['white'], relief='flat', bd=0)
        self.stage_name = stage_name
        self.status = 'pending'
        self.configure(highlightbackground=COLORS['border'], highlightthickness=1)
        self.status_canvas = tk.Canvas(self, width=55, height=55, bg=COLORS['white'], 
                                       highlightthickness=0, bd=0)
        self.status_canvas.pack(pady=(12, 8))
        self.status_circle = self.status_canvas.create_oval(12, 12, 43, 43, 
                                                             fill=COLORS['light'], 
                                                             outline=COLORS['border'], width=2)
        self.name_label = tk.Label(self, text=stage_name, font=('Segoe UI', 9, 'bold'),
                                   bg=COLORS['white'], fg=COLORS['text_primary'])
        self.name_label.pack(pady=(0, 6))
        self.status_label = tk.Label(self, text='Pending', font=('Segoe UI', 8),
                                     bg=COLORS['white'], fg=COLORS['text_secondary'])
        self.status_label.pack(pady=(0, 12))
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        
    def _on_enter(self, event):
        self.configure(bg=COLORS['hover'])
        self.status_canvas.configure(bg=COLORS['hover'])
        self.name_label.configure(bg=COLORS['hover'])
        self.status_label.configure(bg=COLORS['hover'])
        
    def _on_leave(self, event):
        self.configure(bg=COLORS['white'])
        self.status_canvas.configure(bg=COLORS['white'])
        self.name_label.configure(bg=COLORS['white'])
        self.status_label.configure(bg=COLORS['white'])
    
    def update_status(self, status, trans_time=''):
        self.status = status
        color_map = {
            'pending': (COLORS['light'], COLORS['border'], '●', 'Pending'),
            'running': (COLORS['warning'], COLORS['warning'], '◐', 'Running...'),
            'ok': (COLORS['success'], COLORS['success'], '✓', trans_time if trans_time else 'OK'),
            'ng': (COLORS['danger'], COLORS['danger'], '✗', 'Failed'),
            'skip': (COLORS['text_secondary'], COLORS['text_secondary'], '○', 'Skipped')
        }
        fill_color, outline_color, symbol, status_text = color_map.get(status, color_map['pending'])
        self.status_canvas.itemconfig(self.status_circle, fill=fill_color, outline=outline_color)
        if status_text:
            self.status_label.config(text=status_text, font=('Segoe UI', 8),
                                   fg=COLORS['text_primary'] if status == 'ok' else COLORS['text_secondary'])

class Data_P4_Checker_V2:
    def __init__(self, root):
        self.root = root
        self.is_running = False
        self.stage_checker = None
        self.stage_cards = {}
        root.title(f"P4 Production Data Tracker v{get_current_version()}")
        root.geometry("1400x850")
        root.configure(bg=COLORS['light'])
        root.resizable(True, True)
        
        main_container = tk.Frame(root, bg=COLORS['light'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        self._create_header(main_container)
        self._create_input_section(main_container)
        content_frame = tk.Frame(main_container, bg=COLORS['light'])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        left_column = tk.Frame(content_frame, bg=COLORS['light'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self._create_stages_section(left_column)
        right_column = tk.Frame(content_frame, bg=COLORS['light'])
        right_column.pack(side='right', fill='y', padx=(10, 0))
        self._create_info_panel(right_column)
        self._create_log_section(main_container)
        
    def _create_header(self, parent):
        header = tk.Frame(parent, bg=COLORS['white'], height=90)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        try:
            image_path = get_data_path('Resource/logo.png')
            image = Image.open(image_path)
            image = image.resize((65, 65), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(header, image=photo, bg=COLORS['white'])
            logo_label.image = photo
            logo_label.pack(side='left', padx=25, pady=12)
        except:
            pass
        title_frame = tk.Frame(header, bg=COLORS['white'])
        title_frame.pack(side='left', fill='y', pady=15, padx=5)
        title = tk.Label(title_frame, text="P4 PRODUCTION LINE", 
                        font=('Segoe UI', 22, 'bold'),
                        bg=COLORS['white'], fg=COLORS['primary'])
        title.pack(anchor='w')
        subtitle = tk.Label(title_frame, text="Each Stage Data Tracker & Validator",
                          font=('Segoe UI', 10),
                          bg=COLORS['white'], fg=COLORS['text_secondary'])
        subtitle.pack(anchor='w', pady=(3, 0))
        version_badge = tk.Label(header, text=f"v{get_current_version()}", 
                                font=('Segoe UI', 9, 'bold'),
                                bg=COLORS['secondary'], fg=COLORS['white'],
                                padx=12, pady=6)
        version_badge.pack(side='right', padx=25)
        
    def _create_input_section(self, parent):
        input_frame = tk.Frame(parent, bg=COLORS['white'], relief='flat')
        input_frame.pack(fill='x', pady=(0, 20))
        inner = tk.Frame(input_frame, bg=COLORS['white'])
        inner.pack(fill='x', padx=40, pady=25)
        device_frame = tk.Frame(inner, bg=COLORS['white'])
        device_frame.pack(fill='x', pady=(0, 18))
        device_label = tk.Label(device_frame, text="Device ID", 
                               font=('Segoe UI', 11, 'bold'),
                               bg=COLORS['white'], fg=COLORS['text_primary'],
                               width=12, anchor='e')
        device_label.pack(side='left', padx=(0, 20))
        self.Input_DeviceID = tk.Entry(device_frame, font=('Segoe UI', 11),
                                       relief='solid', bd=1,
                                       highlightbackground=COLORS['border'],
                                       highlightcolor=COLORS['secondary'],
                                       highlightthickness=2)
        self.Input_DeviceID.pack(side='left', fill='x', expand=True, ipady=10)
        self.Input_DeviceID.bind("<Return>", lambda e: self.search_mcu_id())
        device_btn = tk.Button(device_frame, text="🔍 CHECK", 
                              command=self.search_mcu_id,
                              font=('Segoe UI', 10, 'bold'),
                              bg=COLORS['secondary'], fg=COLORS['white'],
                              relief='flat', cursor='hand2',
                              padx=25, pady=10,
                              activebackground=COLORS['primary'])
        device_btn.pack(side='left', padx=(20, 0))
        mcu_frame = tk.Frame(inner, bg=COLORS['white'])
        mcu_frame.pack(fill='x')
        mcu_label = tk.Label(mcu_frame, text="MCU ID", 
                            font=('Segoe UI', 11, 'bold'),
                            bg=COLORS['white'], fg=COLORS['text_primary'],
                            width=12, anchor='e')
        mcu_label.pack(side='left', padx=(0, 20))
        self.Input_MCUID = tk.Entry(mcu_frame, font=('Segoe UI', 11),
                                    relief='solid', bd=1,
                                    highlightbackground=COLORS['border'],
                                    highlightcolor=COLORS['secondary'],
                                    highlightthickness=2)
        self.Input_MCUID.pack(side='left', fill='x', expand=True, ipady=10)
        self.Input_MCUID.bind("<Return>", lambda e: self.clear_main())
        mcu_btn = tk.Button(mcu_frame, text="🔍 CHECK", 
                           command=self.clear_main,
                           font=('Segoe UI', 10, 'bold'),
                           bg=COLORS['secondary'], fg=COLORS['white'],
                           relief='flat', cursor='hand2',
                           padx=25, pady=10,
                           activebackground=COLORS['primary'])
        mcu_btn.pack(side='left', padx=(20, 0))
        
    def _create_stages_section(self, parent):
        stages_container = tk.Frame(parent, bg=COLORS['white'], relief='flat')
        stages_container.pack(fill='both', expand=True)
        title_frame = tk.Frame(stages_container, bg=COLORS['white'])
        title_frame.pack(fill='x', padx=25, pady=(20, 15))
        title = tk.Label(title_frame, text="Production Stages", 
                        font=('Segoe UI', 13, 'bold'),
                        bg=COLORS['white'], fg=COLORS['primary'])
        title.pack(side='left')
        progress_label = tk.Label(title_frame, text="23 Stages", 
                                 font=('Segoe UI', 10),
                                 bg=COLORS['white'], fg=COLORS['text_secondary'])
        progress_label.pack(side='right')
        self.progress_label = progress_label
        canvas = tk.Canvas(stages_container, bg=COLORS['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(stages_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=25, pady=(0, 25))
        scrollbar.pack(side="right", fill="y", pady=(0, 25))
        self.stages_canvas = canvas
        
        stages_config = [
            ("Production Stages", [
                ("Firmware", "FIRMWARE"), ("PBA Function", "PBA"), ("Heater", "HEATER"),
                ("Leak Test", "LEAK"), ("3QR Matching", "3QR_MATCH"), ("Sleep", "SLEEP"),
                ("Display", "DISPLAY"), ("Charge Test", "CHARGE"), ("Calibration", "CALI"),
                ("Verification", "VERIFI"), ("Puffing", "PUFFING"), ("Optical Cali", "OPTICAL"),
                ("SN Writing", "SN_WRITE"), ("Final Test", "FINAL"),
            ]),
            ("Packaging Stages", [
                ("Device ID", "DEVICE_ID"), ("Giftbox", "GIFTBOX"), ("Film", "FILM"),
                ("Sleeve", "SLEEVE"), ("Weighing", "WEIGH"), ("Cartonbox", "CARTON"),
                ("Pallet", "PALLET"), ("Shipping", "SHIP"),
            ])
        ]
        
        for section_title, stages in stages_config:
            section_header_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
            section_header_frame.pack(fill='x', padx=15, pady=(20, 12))
            section_header = tk.Label(section_header_frame, text=section_title,
                                     font=('Segoe UI', 11, 'bold'),
                                     bg=COLORS['white'], fg=COLORS['primary'], anchor='w')
            section_header.pack(side='left')
            divider = tk.Frame(section_header_frame, bg=COLORS['border'], height=2)
            divider.pack(side='left', fill='x', expand=True, padx=(15, 0))
            grid_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
            grid_frame.pack(fill='x', padx=15, pady=(0, 5))
            for idx, (display_name, key) in enumerate(stages):
                card = ModernStageCard(grid_frame, display_name)
                row = idx // 7
                col = idx % 7
                card.grid(row=row, column=col, padx=6, pady=6, sticky='ew')
                grid_frame.columnconfigure(col, weight=1, minsize=145)
                self.stage_cards[key] = card
    
    def _create_info_panel(self, parent):
        info_container = tk.Frame(parent, bg=COLORS['white'], width=320, relief='flat')
        info_container.pack(fill='both', expand=True)
        info_container.pack_propagate(False)
        title_frame = tk.Frame(info_container, bg=COLORS['white'])
        title_frame.pack(padx=25, pady=(20, 20))
        title = tk.Label(title_frame, text="📋 Product Information",
                        font=('Segoe UI', 12, 'bold'),
                        bg=COLORS['white'], fg=COLORS['primary'])
        title.pack()
        divider = tk.Frame(info_container, bg=COLORS['border'], height=1)
        divider.pack(fill='x', padx=25, pady=(0, 15))
        info_canvas = tk.Canvas(info_container, bg=COLORS['white'], highlightthickness=0)
        info_scrollbar = ttk.Scrollbar(info_container, orient="vertical", command=info_canvas.yview)
        info_frame = tk.Frame(info_canvas, bg=COLORS['white'])
        info_frame.bind("<Configure>", lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all")))
        info_canvas.create_window((0, 0), window=info_frame, anchor="nw", width=295)
        info_canvas.configure(yscrollcommand=info_scrollbar.set)
        info_canvas.pack(side="left", fill="both", expand=True, padx=(25, 0))
        info_scrollbar.pack(side="right", fill="y", padx=(0, 5))
        def _on_mousewheel(event):
            info_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        info_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.info_labels = {}
        info_items = [
            ("🔑 MCU ID", "mcu_id"), ("🔥 Heater ID", "heater_id"),
            ("⚡ Main PBA", "main_pba"), ("📱 Device ID", "device_id"),
            ("🎁 Giftbox", "giftbox"), ("📦 Cartonbox", "cartonbox")
        ]
        for label_text, key in info_items:
            item_frame = tk.Frame(info_frame, bg=COLORS['white'])
            item_frame.pack(fill='x', padx=5, pady=10)
            label = tk.Label(item_frame, text=label_text,
                           font=('Segoe UI', 9, 'bold'),
                           bg=COLORS['white'], fg=COLORS['text_secondary'], anchor='w')
            label.pack(fill='x')
            value = tk.Label(item_frame, text="—", font=('Segoe UI', 10),
                           bg=COLORS['white'], fg=COLORS['text_primary'],
                           anchor='w', wraplength=260, justify='left')
            value.pack(fill='x', pady=(3, 0))
            self.info_labels[key] = value
        
    def _create_log_section(self, parent):
        log_frame = tk.Frame(parent, bg=COLORS['white'], relief='flat')
        log_frame.pack(fill='x', pady=(20, 0))
        title = tk.Label(log_frame, text="📄 Activity Log",
                        font=('Segoe UI', 11, 'bold'),
                        bg=COLORS['white'], fg=COLORS['primary'])
        title.pack(anchor='w', padx=25, pady=(18, 12))
        log_container = tk.Frame(log_frame, bg=COLORS['border'])
        log_container.pack(fill='x', padx=25, pady=(0, 25))
        self.Log = scrolledtext.ScrolledText(log_container, font=('Consolas', 9),
                                             bg='#f8fafc', fg=COLORS['text_primary'],
                                             relief='flat', height=8, padx=10, pady=8)
        self.Log.pack(fill='x', padx=1, pady=1)
        self.Log.configure(state='disabled')
        self.Log.tag_config("OK", foreground=COLORS['success'], font=('Consolas', 9, 'bold'))
        self.Log.tag_config("NG", foreground=COLORS['danger'], font=('Consolas', 9, 'bold'))
        self.Log.tag_config("SKIP", foreground=COLORS['text_secondary'])

    def auto_scroll_to_card(self, stage_key):
        try:
            card = self.stage_cards.get(stage_key)
            if card:
                self.stages_canvas.update_idletasks()
                card_y = card.winfo_y()
                card_height = card.winfo_height()
                canvas_height = self.stages_canvas.winfo_height()
                scroll_region = self.stages_canvas.bbox("all")
                if scroll_region:
                    total_height = scroll_region[3]
                    target_y = card_y - (canvas_height / 2) + (card_height / 2)
                    scroll_fraction = max(0, min(1, target_y / total_height))
                    self.stages_canvas.yview_moveto(scroll_fraction)
        except:
            pass
    
    def show_result(self, mcu_id, stage_key, get_data_function, log_prefix):
        self.auto_scroll_to_card(stage_key)
        data, trans_time = get_data_function(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        card = self.stage_cards.get(stage_key)
        if not card:
            return
        if data == 'OK':
            card.update_status('ok', trans_time)
            log_message(self.Log, f"✓ {log_prefix}: OK at {trans_time}\n", "OK")
        elif data == 'NG':
            card.update_status('ng')
            log_message(self.Log, f"✗ {log_prefix}: FAILED\n", "NG")
        else:
            card.update_status('skip')
            log_message(self.Log, f"○ {log_prefix}: Skipped\n", "SKIP")
    
    def search_mcu_id(self):
        if self.is_running:
            messagebox.showwarning("System Busy", "A check is currently in progress.")
            return
        Device_id = self.Input_DeviceID.get().strip()
        if not Device_id:
            messagebox.showwarning("Input Required", "Please enter a Device ID.")
            return
        if len(Device_id) != 14 or not Device_id.startswith("I"):
            messagebox.showwarning("Invalid Format", "Device ID must be 14 characters starting with 'I'.")
            self.Input_DeviceID.delete(0, tk.END)
            return
        mcu_id = get_device_id_P4(Device_id)
        if len(mcu_id) >= 16:
            self.start(mcu_id)
        else:
            messagebox.showwarning("Not Found", "Device ID not found.")
        self.Input_DeviceID.delete(0, tk.END)

    def clear_main(self):
        if self.is_running:
            messagebox.showwarning("System Busy", "A check is currently in progress.")
            return
        mcu_id = self.Input_MCUID.get().strip()
        if not mcu_id:
            messagebox.showwarning("Input Required", "Please enter an MCU ID.")
            return
        self.start(mcu_id)
        self.Input_MCUID.delete(0, tk.END)

    def start(self, mcu_id):
        self.is_running = True
        self.Log.configure(state='normal')
        self.Log.delete(1.0, tk.END)
        self.Log.configure(state='disabled')
        for card in self.stage_cards.values():
            card.update_status('pending')
        self.stages_canvas.yview_moveto(0.0)
        
        def load_info():
            return {
                'heater_id': get_heater_id_P4(mcu_id),
                'main_pba': get_main_pba_P4(mcu_id),
                'device_id': get_info_deviceid(mcu_id),
                'giftbox': get_info_giftbox(mcu_id),
                'cartonbox': get_info_cartonbox(mcu_id)
            }
        
        def update_info_panel(info):
            if info:
                self.info_labels['mcu_id'].config(text=mcu_id)
                self.info_labels['heater_id'].config(text=info['heater_id'])
                self.info_labels['main_pba'].config(text=info['main_pba'])
                self.info_labels['device_id'].config(text=info['device_id'])
                self.info_labels['giftbox'].config(text=info['giftbox'])
                self.info_labels['cartonbox'].config(text=info['cartonbox'])
        
        bg_task = BackgroundTask(self.root)
        bg_task.run_async(load_info, update_info_panel)
        self.root.after(100, self._start_background_checks, mcu_id)
    
    def _start_background_checks(self, mcu_id):
        stage_configs = [
            ('FIRMWARE', get_data_firmware_P4, 'Firmware'),
            ('PBA', get_data_pba_function_P4, 'PBA Function'),
            ('HEATER', get_data_heater_P4, 'Heater'),
            ('LEAK', get_data_leak_P4, 'Leak Test'),
            ('3QR_MATCH', get_data_matching_P4, '3QR Matching'),
            ('SLEEP', get_data_sleep_P4, 'Sleep'),
            ('DISPLAY', get_data_display_P4, 'Display'),
            ('CHARGE', get_data_charge_P4, 'Charge Test'),
            ('CALI', get_data_cali_P4, 'Calibration'),
            ('VERIFI', get_data_verifi_P4, 'Verification'),
            ('PUFFING', get_data_puffing_P4, 'Puffing'),
            ('OPTICAL', get_data_optical_cali_P4, 'Optical Cali'),
            ('SN_WRITE', get_data_snwriting_P4, 'SN Writing'),
            ('FINAL', get_data_final_P4, 'Final Test'),
            ('DEVICE_ID', get_data_deviceid, 'Device ID'),
            ('GIFTBOX', get_data_giftbox, 'Giftbox'),
            ('FILM', get_data_film, 'Film'),
            ('SLEEVE', get_data_sleeve, 'Sleeve'),
            ('WEIGH', get_data_weigh, 'Weighing'),
            ('CARTON', get_data_cartonbox, 'Cartonbox'),
            ('PALLET', get_data_pallet, 'Pallet'),
            ('SHIP', get_data_shiping, 'Shipping'),
        ]
        self.stage_checker = StageChecker(self.root, self._update_stage_result)
        self.stage_checker.run_checks(mcu_id, stage_configs, on_complete=self._on_checks_complete)
    
    def _update_stage_result(self, stage_key, data, trans_time):
        self.auto_scroll_to_card(stage_key)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        card = self.stage_cards.get(stage_key)
        if not card:
            return
        if data == 'OK':
            card.update_status('ok', trans_time)
            log_message(self.Log, f"✓ {card.stage_name}: OK at {trans_time}\n", "OK")
        elif data == 'NG':
            card.update_status('ng')
            log_message(self.Log, f"✗ {card.stage_name}: FAILED\n", "NG")
        elif data == 'SKIP':
            card.update_status('skip')
            log_message(self.Log, f"○ {card.stage_name}: Skipped\n", "SKIP")
        else:
            card.update_status('ok', trans_time if trans_time else 'OK')
            log_message(self.Log, f"✓ {card.stage_name}: OK at {trans_time}\n", "OK")
    
    def _on_checks_complete(self):
        self.is_running = False
        log_message(self.Log, f"\n✓ All checks completed successfully\n", "OK")
        self.root.after(100, lambda: self.stages_canvas.yview_moveto(1.0))


def create_gui_P4_v2(create_login_ui, create_gui_P1, create_gui_P230, create_gui_P140):
    def logout():
        root_P4.destroy()
        create_login_ui()
    def switch_to_P1():
        root_P4.destroy()
        create_gui_P1(create_login_ui, create_gui_P230, create_gui_P4_v2, create_gui_P140)
    def switch_to_P230():
        root_P4.destroy()
        create_gui_P230(create_login_ui, create_gui_P1, create_gui_P4_v2, create_gui_P140)
    def switch_to_P140():
        root_P4.destroy()
        create_gui_P140(create_login_ui, create_gui_P1, create_gui_P230, create_gui_P4_v2)

    root_P4 = tk.Tk()
    
    # Modern Status Bar
    status_frame = tk.Frame(root_P4, bg=COLORS['dark'], height=35)
    status_frame.pack(side='bottom', fill='x')
    status_frame.pack_propagate(False)
    
    # Database Connection Status (Left side)
    db_status_label = tk.Label(status_frame, 
                               text="⚪ Checking database...",
                               font=('Segoe UI', 9, 'bold'),
                               bg=COLORS['dark'], 
                               fg='#94a3b8',  # Slate gray
                               padx=15, pady=8)
    db_status_label.pack(side='left')
    
    # Copyright Notice (Right side)
    Copyright = tk.Label(status_frame, text="ITM Semiconductor Vietnam © 2024 | IT Team",
                        font=('Segoe UI', 8), bg=COLORS['dark'], fg=COLORS['light'])
    Copyright.pack(side='right', padx=20)
    
    menubar = tk.Menu(root_P4)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Switch to P1", command=switch_to_P1)
    file_menu.add_command(label="Switch to P230", command=switch_to_P230)
    file_menu.add_command(label="Switch to P140", command=switch_to_P140)
    file_menu.add_separator()
    file_menu.add_command(label="Logout", command=logout)
    menubar.add_cascade(label="Menu", menu=file_menu)
    root_P4.config(menu=menubar)
    
    # Start database connection check
    check_ping(db_status_label)
    ui = Data_P4_Checker_V2(root_P4)
    root_P4.mainloop()
