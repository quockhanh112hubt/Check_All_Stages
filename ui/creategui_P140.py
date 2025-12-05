import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from tkinter import scrolledtext
from utils.log import log_message
from utils.date import format_trans_time
from utils.utils import show_image, show_image_narrow, get_current_version, get_data_path
from utils.Checkping import check_ping
from data.pba import get_data_pba_function_P140
from data.firmware import get_data_firmware_P140
from data.heater_module import get_data_heater_module_aging_P140, get_data_heater_module_function_P140, get_data_cover_heater_function_P140, get_heater_id_P140
from data.matching import get_data_matching_P140, get_main_pba_P140
from data.lcdled import get_data_lcdled_P140
from data.charge import get_data_charge_P140
from data.calibration import get_data_cali_P140
from data.verification import get_data_verifi_P140
from data.snwriting import get_data_snwriting_P140
from data.final import get_data_final_P140
from data.smart_mmi import get_data_smart_on_off_P140, get_data_mmi_check_P140
from data.Packing import *
from data.weigh import get_data_weigh
from data.get_mcu_id import get_device_id_P140
from PIL import Image, ImageTk

class Data_P140_Checker:
    
    def __init__(self, root):
        self.root = root
        self.is_running = False
        root.title(f"Each Stage Data Checker Version {get_current_version()}")
        root.geometry("965x825")
        root.resizable(False, False)

        image_path = get_data_path('Resource/logo.png')
        image = Image.open(image_path)
        image = image.resize((150, 70), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        lbl_Logo = tk.Label(root, image=photo, anchor='nw')
        lbl_Logo.image = photo
        lbl_Logo.place(x=10, y=10, width=190, height=80)

        lbl_Name1 = tk.Label(root, text="P140 EACH STAGE", font=("Arial", 22, "bold italic"))
        lbl_Name1.place(x=210, y=20, width=290, height=25)
        lbl_Name = tk.Label(root, text="DATA CHECKER", font=("Arial", 22, "bold italic"))
        lbl_Name.place(x=300, y=60, width=240, height=25)

        lbl_DeviceID = tk.Label(root, text="Nhập vào Device_ID:", font=("Arial", 14), anchor='w')
        lbl_DeviceID.place(x=10, y=110, width=185, height=30)
        self.device_button = ttk.Button(root, text="DEVICE_ID CHECK", command=self.search_mcu_id)
        self.device_button.place(x=520, y=110, width=150, height=30)
        self.Input_DeviceID = tk.Entry(font=tkFont.Font(family="Arial", size=20))
        self.Input_DeviceID.place(x=200, y=110, width=310, height=30)

        def on_enter_device(event):
            self.search_mcu_id()
            self.Input_DeviceID.delete(0,tk.END)
        self.Input_DeviceID.bind("<Return>", on_enter_device)

        lbl_MCUID = tk.Label(root, text="Nhập vào MCU_ID:", font=("Arial", 14), anchor='w')
        lbl_MCUID.place(x=10, y=150, width=185, height=30)
        self.submit_button = ttk.Button(root, text="MCU_ID CHECK", command=self.clear_main)
        self.submit_button.place(x=520, y=150, width=150, height=30)
        self.Input_MCUID = tk.Entry(font=tkFont.Font(family="Arial", size=20))
        self.Input_MCUID.place(x=200, y=150, width=310, height=30)

        def on_enter(event):
            self.clear_main()
            self.Input_MCUID.delete(0,tk.END)
        self.Input_MCUID.bind("<Return>", on_enter)

        self.Log = scrolledtext.ScrolledText(root, font=("Arial", 11))
        self.Log.place(x=10, y=600, width=940, height=190)
        self.Log.configure(state='disabled')
        self.Log.tag_config("OK", foreground="green")
        self.Log.tag_config("NG", foreground="red")
        self.Log.tag_config("SKIP", foreground="black")

        lbl_Info = tk.Label(root, text="Information Checking", anchor="center", font=("Arial", 13, "bold"))
        lbl_Info.place(x=680, y=10, width=280, height=20)
        lbl_Line = tk.Label(root, text="-----------------------------------------------", anchor="center", font=("Arial", 12, "bold"))
        lbl_Line.place(x=680, y=30, width=280, height=20)

        lbl_MCULabel = tk.Label(root, text="MCU_ID:", anchor="w", font=("Arial", 11, "bold"))
        lbl_MCULabel.place(x=680, y=60, width=80, height=20)
        lbl_HeaterLabel = tk.Label(root, text="Heater_ID:", anchor="w", font=("Arial", 11, "bold"))
        lbl_HeaterLabel.place(x=680, y=80, width=80, height=20)
        lbl_MainPBALabel = tk.Label(root, text="Main_PBA:", anchor="w", font=("Arial", 11, "bold"))
        lbl_MainPBALabel.place(x=680, y=100, width=80, height=20)
        lbl_DeviceLabel = tk.Label(root, text="Device_ID:", anchor="w", font=("Arial", 11, "bold"))
        lbl_DeviceLabel.place(x=680, y=120, width=80, height=20)
        lbl_GiftboxLabel = tk.Label(root, text="Giftbox:", anchor="w", font=("Arial", 11, "bold"))
        lbl_GiftboxLabel.place(x=680, y=140, width=80, height=20)
        lbl_CartonLabel = tk.Label(root, text="Cartonbox:", anchor="w", font=("Arial", 11, "bold"))
        lbl_CartonLabel.place(x=680, y=160, width=80, height=20)

        self.data_MCULabel = tk.Label(root, text="", anchor="w", font=("Arial", 11, "bold"))
        self.data_MCULabel.place(x=765, y=60, width=195, height=20)
        self.data_HeaterLabel = tk.Label(root, text="", anchor="w", font=("Arial", 11, "bold"))
        self.data_HeaterLabel.place(x=765, y=80, width=195, height=20)
        self.data_MainPBALabel = tk.Label(root, text="", anchor="w", font=("Arial", 11, "bold"))
        self.data_MainPBALabel.place(x=765, y=100, width=195, height=20)
        self.data_DeviceLabel = tk.Label(root, text="", anchor="w", font=("Arial", 11, "bold"))
        self.data_DeviceLabel.place(x=765, y=120, width=195, height=20)
        self.data_GiftboxLabel = tk.Label(root, text="", anchor="w", font=("Arial", 11, "bold"))
        self.data_GiftboxLabel.place(x=765, y=140, width=195, height=20)
        self.data_CartonLabel = tk.Label(root, text="", anchor="w", font=("Arial", 11, "bold"))
        self.data_CartonLabel.place(x=765, y=160, width=195, height=20)

        # ROW 1 - 8 stages (left to right)
        # Firmware
        self.result_firmware = ttk.Label(root, text="")
        self.result_firmware.place(x=10, y=200, width=70, height=70)
        self.label_firmware = ttk.Label(root, text="")
        self.label_firmware.place(x=85, y=215, width=30, height=40)
        self.name_firmware = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_firmware.place(x=5, y=270, width=80, height=20)

        # PBA_Function
        self.result_pba = ttk.Label(root, text="")
        self.result_pba.place(x=120, y=200, width=70, height=70)
        self.label_pba = ttk.Label(root, text="")
        self.label_pba.place(x=195, y=215, width=30, height=40)
        self.name_pba = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_pba.place(x=115, y=270, width=80, height=20)

        # Heater_Module_Aging
        self.result_heater_aging = ttk.Label(root, text="")
        self.result_heater_aging.place(x=230, y=200, width=70, height=70)
        self.label_heater_aging = ttk.Label(root, text="")
        self.label_heater_aging.place(x=305, y=215, width=30, height=40)
        self.name_heater_aging = ttk.Label(root, text="", anchor="center", font=("Arial", 7, "bold"))
        self.name_heater_aging.place(x=225, y=270, width=80, height=20)

        # Heater_Module_Function
        self.result_heater_func = ttk.Label(root, text="")
        self.result_heater_func.place(x=340, y=200, width=70, height=70)
        self.label_heater_func = ttk.Label(root, text="")
        self.label_heater_func.place(x=415, y=215, width=30, height=40)
        self.name_heater_func = ttk.Label(root, text="", anchor="center", font=("Arial", 7, "bold"))
        self.name_heater_func.place(x=335, y=270, width=80, height=20)

        # Cover_Heater_Function
        self.result_cover_heater = ttk.Label(root, text="")
        self.result_cover_heater.place(x=450, y=200, width=70, height=70)
        self.label_cover_heater = ttk.Label(root, text="")
        self.label_cover_heater.place(x=525, y=215, width=30, height=40)
        self.name_cover_heater = ttk.Label(root, text="", anchor="center", font=("Arial", 7, "bold"))
        self.name_cover_heater.place(x=445, y=270, width=80, height=20)

        # 3QR_Matching
        self.result_matching = ttk.Label(root, text="")
        self.result_matching.place(x=560, y=200, width=70, height=70)
        self.label_matching = ttk.Label(root, text="")
        self.label_matching.place(x=635, y=215, width=30, height=40)
        self.name_matching = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_matching.place(x=555, y=270, width=80, height=20)

        # LCD_LED
        self.result_lcdled = ttk.Label(root, text="")
        self.result_lcdled.place(x=670, y=200, width=70, height=70)
        self.label_lcdled = ttk.Label(root, text="")
        self.label_lcdled.place(x=745, y=215, width=30, height=40)
        self.name_lcdled = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_lcdled.place(x=665, y=270, width=80, height=20)

        # Charge
        self.result_charge = ttk.Label(root, text="")
        self.result_charge.place(x=780, y=200, width=70, height=70)
        self.label_charge = ttk.Label(root, text="")
        self.label_charge.place(x=790, y=295, width=30, height=40)
        self.name_charge = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_charge.place(x=775, y=270, width=80, height=20)

        # ROW 2 - 8 stages (right to left)
        # Calibration
        self.result_cali = ttk.Label(root, text="")
        self.result_cali.place(x=780, y=340, width=70, height=70)
        self.label_cali = ttk.Label(root, text="")
        self.label_cali.place(x=745, y=355, width=30, height=40)
        self.name_cali = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_cali.place(x=775, y=410, width=80, height=20)

        # Verification
        self.result_verifi = ttk.Label(root, text="")
        self.result_verifi.place(x=670, y=340, width=70, height=70)
        self.label_verifi = ttk.Label(root, text="")
        self.label_verifi.place(x=635, y=355, width=30, height=40)
        self.name_verifi = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_verifi.place(x=665, y=410, width=80, height=20)

        # SN_Writing
        self.result_sn = ttk.Label(root, text="")
        self.result_sn.place(x=560, y=340, width=70, height=70)
        self.label_sn = ttk.Label(root, text="")
        self.label_sn.place(x=525, y=355, width=30, height=40)
        self.name_sn = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_sn.place(x=555, y=410, width=80, height=20)

        # Smart_On_Off
        self.result_smart = ttk.Label(root, text="")
        self.result_smart.place(x=450, y=340, width=70, height=70)
        self.label_smart = ttk.Label(root, text="")
        self.label_smart.place(x=415, y=355, width=30, height=40)
        self.name_smart = ttk.Label(root, text="", anchor="center", font=("Arial", 7, "bold"))
        self.name_smart.place(x=445, y=410, width=80, height=20)

        # MMI_Check
        self.result_mmi = ttk.Label(root, text="")
        self.result_mmi.place(x=340, y=340, width=70, height=70)
        self.label_mmi = ttk.Label(root, text="")
        self.label_mmi.place(x=305, y=355, width=30, height=40)
        self.name_mmi = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_mmi.place(x=335, y=410, width=80, height=20)

        # Final_Test
        self.result_final = ttk.Label(root, text="")
        self.result_final.place(x=230, y=340, width=70, height=70)
        self.label_final = ttk.Label(root, text="")
        self.label_final.place(x=195, y=355, width=30, height=40)
        self.name_final = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_final.place(x=225, y=410, width=80, height=20)

        # Device_ID
        self.result_device = ttk.Label(root, text="")
        self.result_device.place(x=120, y=340, width=70, height=70)
        self.label_device = ttk.Label(root, text="")
        self.label_device.place(x=85, y=355, width=30, height=40)
        self.name_device = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_device.place(x=115, y=410, width=80, height=20)

        # Giftbox
        self.result_giftbox = ttk.Label(root, text="")
        self.result_giftbox.place(x=10, y=340, width=70, height=70)
        self.label_giftbox = ttk.Label(root, text="")
        self.label_giftbox.place(x=20, y=435, width=30, height=40)
        self.name_giftbox = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_giftbox.place(x=5, y=410, width=80, height=20)

        # ROW 3 - 5 stages (left to right) - Packing stages
        # Sleeve
        self.result_sleeve = ttk.Label(root, text="")
        self.result_sleeve.place(x=10, y=480, width=70, height=70)
        self.label_sleeve = ttk.Label(root, text="")
        self.label_sleeve.place(x=85, y=495, width=30, height=40)
        self.name_sleeve = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_sleeve.place(x=5, y=550, width=80, height=20)

        # Weigh
        self.result_weigh = ttk.Label(root, text="")
        self.result_weigh.place(x=120, y=480, width=70, height=70)
        self.label_weigh = ttk.Label(root, text="")
        self.label_weigh.place(x=195, y=495, width=30, height=40)
        self.name_weigh = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_weigh.place(x=115, y=550, width=80, height=20)

        # Cartonbox
        self.result_carton = ttk.Label(root, text="")
        self.result_carton.place(x=230, y=480, width=70, height=70)
        self.label_carton = ttk.Label(root, text="")
        self.label_carton.place(x=305, y=495, width=30, height=40)
        self.name_carton = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_carton.place(x=225, y=550, width=80, height=20)

        # Pallet
        self.result_pallet = ttk.Label(root, text="")
        self.result_pallet.place(x=340, y=480, width=70, height=70)
        self.label_pallet = ttk.Label(root, text="")
        self.label_pallet.place(x=415, y=495, width=30, height=40)
        self.name_pallet = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_pallet.place(x=335, y=550, width=80, height=20)

        # Shipping
        self.result_ship = ttk.Label(root, text="")
        self.result_ship.place(x=450, y=480, width=70, height=70)
        self.name_ship = ttk.Label(root, text="", anchor="center", font=("Arial", 8, "bold"))
        self.name_ship.place(x=445, y=550, width=80, height=20)

    def show_result(self, mcu_id, log, get_data_function, result_widget, label_widget, name_widget, name_text, arrow_image, log_prefix):
        data, trans_time = get_data_function(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)

        if data == 'OK':
            show_image(result_widget, 'Resource/OK.png')
            show_image_narrow(label_widget, arrow_image)
            name_widget.config(text=name_text)
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn {log_prefix} kết quả OK vào lúc {trans_time}.\n", "OK")
        elif data == 'NG':
            show_image(result_widget, 'Resource/NG.png')
            show_image_narrow(label_widget, arrow_image)
            name_widget.config(text=name_text)
            log_message(log, f"MCU_ID: {mcu_id} công đoạn {log_prefix} NG!.\n", "NG")
        else:
            show_image(result_widget, 'Resource/None.png')
            show_image_narrow(label_widget, arrow_image)
            name_widget.config(text=name_text)
            log_message(log, f"MCU_ID: {mcu_id} công đoạn {log_prefix} SKIP!.\n", "SKIP")

    def show_result_packing(self, mcu_id, log, get_data_function, result_widget, label_widget, name_widget, name_text, arrow_image, log_prefix):
        data, trans_time = get_data_function(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(result_widget, 'Resource/None.png')
            show_image_narrow(label_widget, arrow_image)
            name_widget.config(text=name_text)
            log_message(log, f"MCU_ID: {mcu_id} công đoạn {log_prefix} SKIP!.\n", "SKIP")
        else:
            show_image(result_widget, 'Resource/OK.png')
            name_widget.config(text=name_text)
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn {log_prefix} kết quả OK vào lúc {trans_time}.\n", "OK")

    # Row 1 stages
    def show_result_firmware(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_firmware_P140, self.result_firmware, self.label_firmware, self.name_firmware, "FIRMWARE", 'Resource/arrowtoleft.png', "Firmware")
        self.root.after(5, self.show_result_pba, mcu_id, log)

    def show_result_pba(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_pba_function_P140, self.result_pba, self.label_pba, self.name_pba, "PBA", 'Resource/arrowtoleft.png', "PBA Function")
        self.root.after(5, self.show_result_heater_aging, mcu_id, log)

    def show_result_heater_aging(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_heater_module_aging_P140, self.result_heater_aging, self.label_heater_aging, self.name_heater_aging, "HTR_AGING", 'Resource/arrowtoleft.png', "Heater Module Aging")
        self.root.after(5, self.show_result_heater_func, mcu_id, log)

    def show_result_heater_func(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_heater_module_function_P140, self.result_heater_func, self.label_heater_func, self.name_heater_func, "HTR_FUNC", 'Resource/arrowtoleft.png', "Heater Module Function")
        self.root.after(5, self.show_result_cover_heater, mcu_id, log)

    def show_result_cover_heater(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_cover_heater_function_P140, self.result_cover_heater, self.label_cover_heater, self.name_cover_heater, "CVR_HTR", 'Resource/arrowtoleft.png', "Cover Heater Function")
        self.root.after(5, self.show_result_matching, mcu_id, log)

    def show_result_matching(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_matching_P140, self.result_matching, self.label_matching, self.name_matching, "3QR_MATCH", 'Resource/arrowtoleft.png', "3QR Matching")
        self.root.after(5, self.show_result_lcdled, mcu_id, log)

    def show_result_lcdled(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_lcdled_P140, self.result_lcdled, self.label_lcdled, self.name_lcdled, "LCD_LED", 'Resource/arrowtoleft.png', "LCD LED")
        self.root.after(5, self.show_result_charge, mcu_id, log)

    def show_result_charge(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_charge_P140, self.result_charge, self.label_charge, self.name_charge, "CHARGE", 'Resource/arrowtodown.png', "Charge")
        self.root.after(5, self.show_result_cali, mcu_id, log)

    # Row 2 stages
    def show_result_cali(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_cali_P140, self.result_cali, self.label_cali, self.name_cali, "CALI", 'Resource/arrowtoright.png', "Calibration")
        self.root.after(5, self.show_result_verifi, mcu_id, log)

    def show_result_verifi(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_verifi_P140, self.result_verifi, self.label_verifi, self.name_verifi, "VERIFI", 'Resource/arrowtoright.png', "Verification")
        self.root.after(5, self.show_result_snwriting, mcu_id, log)

    def show_result_snwriting(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_snwriting_P140, self.result_sn, self.label_sn, self.name_sn, "SN_WRITE", 'Resource/arrowtoright.png', "SN Writing")
        self.root.after(5, self.show_result_smart, mcu_id, log)

    def show_result_smart(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_smart_on_off_P140, self.result_smart, self.label_smart, self.name_smart, "SMART", 'Resource/arrowtoright.png', "Smart On Off")
        self.root.after(5, self.show_result_mmi, mcu_id, log)

    def show_result_mmi(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_mmi_check_P140, self.result_mmi, self.label_mmi, self.name_mmi, "MMI", 'Resource/arrowtoright.png', "MMI Check")
        self.root.after(5, self.show_result_final, mcu_id, log)

    def show_result_final(self, mcu_id, log):
        self.show_result(mcu_id, log, get_data_final_P140, self.result_final, self.label_final, self.name_final, "FINAL", 'Resource/arrowtoright.png', "Final Test")
        self.root.after(5, self.show_result_deviceid, mcu_id, log)

    def show_result_deviceid(self, mcu_id, log):
        self.show_result_packing(mcu_id, log, get_data_deviceid, self.result_device, self.label_device, self.name_device, "DEVICE_ID", 'Resource/arrowtoright.png', "Device ID")
        self.root.after(5, self.show_result_giftbox, mcu_id, log)

    def show_result_giftbox(self, mcu_id, log):
        self.show_result_packing(mcu_id, log, get_data_giftbox, self.result_giftbox, self.label_giftbox, self.name_giftbox, "GIFTBOX", 'Resource/arrowtodown.png', "Giftbox")
        self.root.after(5, self.show_result_sleeve, mcu_id, log)

    # Row 3 stages
    def show_result_sleeve(self, mcu_id, log):
        self.show_result_packing(mcu_id, log, get_data_sleeve, self.result_sleeve, self.label_sleeve, self.name_sleeve, "SLEEVE", 'Resource/arrowtoleft.png', "Sleeve")
        self.root.after(5, self.show_result_weigh, mcu_id, log)

    def show_result_weigh(self, mcu_id, log):
        self.show_result_packing(mcu_id, log, get_data_weigh, self.result_weigh, self.label_weigh, self.name_weigh, "WEIGH", 'Resource/arrowtoleft.png', "Weigh")
        self.root.after(5, self.show_result_carton, mcu_id, log)

    def show_result_carton(self, mcu_id, log):
        self.show_result_packing(mcu_id, log, get_data_cartonbox, self.result_carton, self.label_carton, self.name_carton, "CARTON", 'Resource/arrowtoleft.png', "Cartonbox")
        self.root.after(5, self.show_result_pallet, mcu_id, log)

    def show_result_pallet(self, mcu_id, log):
        self.show_result_packing(mcu_id, log, get_data_pallet, self.result_pallet, self.label_pallet, self.name_pallet, "PALLET", 'Resource/arrowtoleft.png', "Pallet")
        self.root.after(5, self.show_result_shipping, mcu_id, log)

    def show_result_shipping(self, mcu_id, log):
        data, trans_time = get_data_shiping(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_ship, 'Resource/None.png')
            self.name_ship.config(text="SHIP")
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Shipping SKIP!.\n", "SKIP")
        else:
            show_image(self.result_ship, 'Resource/OK.png')
            self.name_ship.config(text="SHIP")
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Shipping kết quả OK vào lúc {trans_time}.\n", "OK")
        self.is_running = False

    def search_mcu_id(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Chương trình đang chạy. Vui lòng chờ.")
            return

        Device_id = self.Input_DeviceID.get().strip()
        if not Device_id:
            messagebox.showwarning("Warning", "Device_ID không được để trống.")
            return
        if len(Device_id) != 14:
            messagebox.showwarning("Warning", "Device_ID sai định dạng, vui lòng kiểm tra lại.")
            self.Input_DeviceID.delete(0,tk.END)
            return
        if not Device_id.startswith("I"):
            messagebox.showwarning("Warning", "Device_ID phải bắt đầu bằng 'I'.")
            self.Input_DeviceID.delete(0, tk.END)
            return

        mcu_id = get_device_id_P140(Device_id)
        if len(mcu_id) >= 16:
            self.start(mcu_id)
        else:
             messagebox.showwarning("Warning", "Device_ID không có thông tin xác thực!. Vui lòng kiểm tra lại.")
        self.Input_DeviceID.delete(0, tk.END)
        return

    def clear_main(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Chương trình đang chạy. Vui lòng chờ.")
            return

        mcu_id = self.Input_MCUID.get().strip()
        if not mcu_id:
            messagebox.showwarning("Warning", "MCU_ID không được để trống.")
            return
        if not mcu_id.startswith("_ALU"):
            messagebox.showwarning("Warning", "MCU_ID phải bắt đầu bằng '_ALU'.")
            self.Input_MCUID.delete(0, tk.END)
            return
        self.start(mcu_id)
        self.Input_MCUID.delete(0,tk.END)

    def start(self, mcu_id):
        self.is_running = True 

        self.Log.configure(state='normal')
        self.Log.delete(1.0, tk.END)
        self.Log.configure(state="disabled")

        # Clear all result widgets
        widgets = [
            (self.result_firmware, self.label_firmware, self.name_firmware),
            (self.result_pba, self.label_pba, self.name_pba),
            (self.result_heater_aging, self.label_heater_aging, self.name_heater_aging),
            (self.result_heater_func, self.label_heater_func, self.name_heater_func),
            (self.result_cover_heater, self.label_cover_heater, self.name_cover_heater),
            (self.result_matching, self.label_matching, self.name_matching),
            (self.result_lcdled, self.label_lcdled, self.name_lcdled),
            (self.result_charge, self.label_charge, self.name_charge),
            (self.result_cali, self.label_cali, self.name_cali),
            (self.result_verifi, self.label_verifi, self.name_verifi),
            (self.result_sn, self.label_sn, self.name_sn),
            (self.result_smart, self.label_smart, self.name_smart),
            (self.result_mmi, self.label_mmi, self.name_mmi),
            (self.result_final, self.label_final, self.name_final),
            (self.result_device, self.label_device, self.name_device),
            (self.result_giftbox, self.label_giftbox, self.name_giftbox),
            (self.result_sleeve, self.label_sleeve, self.name_sleeve),
            (self.result_weigh, self.label_weigh, self.name_weigh),
            (self.result_carton, self.label_carton, self.name_carton),
            (self.result_pallet, self.label_pallet, self.name_pallet),
        ]

        for result, label, name in widgets:
            result.config(text="", image="")
            label.config(text="", image="")
            name.config(text="")

        self.result_ship.config(text="", image="")
        self.name_ship.config(text="")

        self.data_MCULabel.config(text=f"{mcu_id}")
        
        heater_id = get_heater_id_P140(mcu_id)
        self.data_HeaterLabel.config(text=f"{heater_id}")

        main_pba = get_main_pba_P140(mcu_id)
        self.data_MainPBALabel.config(text=f"{main_pba}")

        device_id = get_info_deviceid(mcu_id)
        self.data_DeviceLabel.config(text=f"{device_id}")

        giftbox_id = get_info_giftbox(mcu_id)
        self.data_GiftboxLabel.config(text=f"{giftbox_id}")

        cartonbox_id = get_info_cartonbox(mcu_id)
        self.data_CartonLabel.config(text=f"{cartonbox_id}")

        self.root.after(5, self.show_result_firmware, mcu_id, self.Log)

def create_gui_P140(create_login_ui, create_gui_P1, create_gui_P230, create_gui_P4):
    def logout():
        root_P140.destroy()
        create_login_ui()

    def switch_to_P1():
        root_P140.destroy()
        create_gui_P1(create_login_ui, create_gui_P230, create_gui_P4, create_gui_P140)

    def switch_to_P230():
        root_P140.destroy()
        create_gui_P230(create_login_ui, create_gui_P1, create_gui_P4, create_gui_P140)

    def switch_to_P4():
        root_P140.destroy()
        create_gui_P4(create_login_ui, create_gui_P1, create_gui_P230, create_gui_P140)

    root_P140 = tk.Tk()
    icon_mesconnect = ttk.Label(root_P140, text="")
    icon_mesconnect.place(x=10, y=795, width=25, height=25)
    name_mesconnect = ttk.Label(root_P140, text="", anchor="w")
    name_mesconnect.place(x=40, y=795, width=200, height=25)
    Copyright = ttk.Label(root_P140, text="Powered by ITM Semiconductor Vietnam Company Limited - IT Team. Copyright © 2024 all rights reserved.", anchor="w")
    Copyright.place(x=380, y=795, width=570, height=25)

    menubar = tk.Menu(root_P140)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Chuyển sang ECIGA-P1", command=switch_to_P1)
    file_menu.add_command(label="Chuyển sang ECIGA-P2 3.0", command=switch_to_P230)
    file_menu.add_command(label="Chuyển sang ECIGA-P4", command=switch_to_P4)
    file_menu.add_command(label="Đăng xuất", command=logout)
    menubar.add_cascade(label="Menu", menu=file_menu)
    
    root_P140.config(menu=menubar)

    check_ping(icon_mesconnect, name_mesconnect)

    ui = Data_P140_Checker(root_P140)
    root_P140.mainloop()
