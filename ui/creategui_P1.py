import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from tkinter import scrolledtext
from utils.log import log_message
from utils.utils import show_image, show_image_narrow, get_current_version, get_data_path
from utils.date import format_trans_time
from utils.Checkping import check_ping
from data.pba import get_data_pba_function_P1
from data.firmware import get_data_firmware_P1
from data.heater import get_data_heater_P1, get_heater_id_P1
from data.matching import get_data_matching_P1, get_main_pba_P1
from data.charge import get_data_charge_P1
from data.calibration import get_data_cali_P1
from data.verification import get_data_verifi_P1
from data.lcdled import get_data_mmi_P1
from data.sensor import get_data_vibration_P1
from data.snwriting import get_data_snwriting_P1
from data.final import get_data_final_P1
from data.Packing import get_data_deviceid, get_data_giftbox, get_data_film, get_data_sleeve, get_data_cartonbox, get_data_pallet, get_data_shiping, get_info_deviceid, get_info_giftbox, get_info_cartonbox
from data.weigh import get_data_weigh
from PIL import Image, ImageTk
from data.get_mcu_id import get_device_id_P1


class Data_P1EZ_Checker:
    
    def __init__(self, root):
        self.root = root
        self.is_running = False
        root.title(f"Each Stage Data Checker Version {get_current_version()}")
        root.geometry("965x825")
        # root.configure(bg='#888888')
        root.resizable(False, False)

        image_path = get_data_path('Resource/logo.png')
        image = Image.open(image_path)
        image = image.resize((150, 70), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        lbl_Logo = tk.Label(root, image=photo, anchor='nw')
        lbl_Logo.image = photo
        lbl_Logo.place(x=10, y=10, width=190, height=80)

        lbl_Name1 = tk.Label(root, text="P1 EACH STAGE", font=("Arial", 22, "bold italic"))
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

        lbl_Info = tk.Label(root, text="Infomation Checking", anchor="center", font=("Arial", 13, "bold"))
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



        #---------------------------------------------------------------------------------------------------
        self.result_firmware = ttk.Label(root, text="")
        self.result_firmware.place(x=25, y=200, width=70, height=70)
        self.label_firmware = ttk.Label(root, text="")
        self.label_firmware.place(x=100, y=215, width=35, height=40)
        self.name_firmware = ttk.Label(root, text="", anchor="center")
        self.name_firmware.place(x=10, y=270, width=100, height=20)

        self.result_pba = ttk.Label(root, text="")
        self.result_pba.place(x=145, y=200, width=70, height=70)
        self.label_pba = ttk.Label(root, text="")
        self.label_pba.place(x=220, y=215, width=35, height=40)
        self.name_pba = ttk.Label(root, text="", anchor="center")
        self.name_pba.place(x=130, y=270, width=100, height=20)

        self.result_heater = ttk.Label(root, text="")
        self.result_heater.place(x=265, y=200, width=70, height=70)
        self.label_heater = ttk.Label(root, text="")
        self.label_heater.place(x=340, y=215, width=35, height=40)
        self.name_heater = ttk.Label(root, text="", anchor="center")
        self.name_heater.place(x=250, y=270, width=100, height=20)

        self.result_matching = ttk.Label(root, text="")
        self.result_matching.place(x=385, y=200, width=70, height=70)
        self.label_matching = ttk.Label(root, text="")
        self.label_matching.place(x=460, y=215, width=35, height=40)
        self.name_matching = ttk.Label(root, text="", anchor="center")
        self.name_matching.place(x=370, y=270, width=100, height=20)

        self.result_charge = ttk.Label(root, text="")
        self.result_charge.place(x=505, y=200, width=70, height=70)
        self.label_charge = ttk.Label(root, text="")
        self.label_charge.place(x=580, y=215, width=35, height=40)
        self.name_charge = ttk.Label(root, text="", anchor="center")
        self.name_charge.place(x=490, y=270, width=100, height=20)

        self.result_cali = ttk.Label(root, text="")
        self.result_cali.place(x=625, y=200, width=70, height=70)
        self.label_cali = ttk.Label(root, text="")
        self.label_cali.place(x=700, y=215, width=35, height=40)
        self.name_cali = ttk.Label(root, text="", anchor="center")
        self.name_cali.place(x=610, y=270, width=100, height=20)

        self.result_verifi = ttk.Label(root, text="")
        self.result_verifi.place(x=745, y=200, width=70, height=70)
        self.label_verifi = ttk.Label(root, text="")
        self.label_verifi.place(x=820, y=215, width=35, height=40)
        self.name_verifi = ttk.Label(root, text="", anchor="center")
        self.name_verifi.place(x=730, y=270, width=100, height=20)

        self.result_puff = ttk.Label(root, text="")
        self.result_puff.place(x=865, y=200, width=70, height=70)
        self.label_puff = ttk.Label(root, text="")
        self.label_puff.place(x=880, y=300, width=35, height=40)
        self.name_puff = ttk.Label(root, text="", anchor="center")
        self.name_puff.place(x=850, y=270, width=100, height=20)

        self.result_sensor = ttk.Label(root, text="")
        self.result_sensor.place(x=865, y=350, width=70, height=70)
        self.label_sensor = ttk.Label(root, text="")
        self.label_sensor.place(x=820, y=365, width=35, height=40)
        self.name_sensor = ttk.Label(root, text="", anchor="center")
        self.name_sensor.place(x=850, y=420, width=100, height=20)

        self.result_sn = ttk.Label(root, text="")
        self.result_sn.place(x=745, y=350, width=70, height=70)
        self.label_sn = ttk.Label(root, text="")
        self.label_sn.place(x=700, y=365, width=35, height=40)
        self.name_sn = ttk.Label(root, text="", anchor="center")
        self.name_sn.place(x=730, y=420, width=100, height=20)

        self.result_final = ttk.Label(root, text="")
        self.result_final.place(x=625, y=350, width=70, height=70)
        self.label_final = ttk.Label(root, text="")
        self.label_final.place(x=580, y=365, width=35, height=40)
        self.name_final = ttk.Label(root, text="", anchor="center")
        self.name_final.place(x=610, y=420, width=100, height=20)

        self.result_device = ttk.Label(root, text="")
        self.result_device.place(x=505, y=350, width=70, height=70)
        self.label_device = ttk.Label(root, text="")
        self.label_device.place(x=460, y=365, width=35, height=40)
        self.name_device = ttk.Label(root, text="", anchor="center")
        self.name_device.place(x=490, y=420, width=100, height=20)

        self.result_giftbox = ttk.Label(root, text="")
        self.result_giftbox.place(x=385, y=350, width=70, height=70)
        self.label_giftbox = ttk.Label(root, text="")
        self.label_giftbox.place(x=340, y=365, width=35, height=40)
        self.name_giftbox = ttk.Label(root, text="", anchor="center")
        self.name_giftbox.place(x=370, y=420, width=100, height=20)

        self.result_film = ttk.Label(root, text="")
        self.result_film.place(x=265, y=350, width=70, height=70)
        self.label_film = ttk.Label(root, text="")
        self.label_film.place(x=220, y=365, width=35, height=40)
        self.name_film = ttk.Label(root, text="", anchor="center")
        self.name_film.place(x=250, y=420, width=100, height=20)

        self.result_sleeve = ttk.Label(root, text="")
        self.result_sleeve.place(x=145, y=350, width=70, height=70)
        self.label_sleeve = ttk.Label(root, text="")
        self.label_sleeve.place(x=100, y=365, width=35, height=40)
        self.name_sleeve = ttk.Label(root, text="", anchor="center")
        self.name_sleeve.place(x=130, y=420, width=100, height=20)

        self.result_weigh = ttk.Label(root, text="")
        self.result_weigh.place(x=25, y=350, width=70, height=70)
        self.label_weigh = ttk.Label(root, text="")
        self.label_weigh.place(x=40, y=450, width=35, height=40)
        self.name_weigh = ttk.Label(root, text="", anchor="center")
        self.name_weigh.place(x=10, y=420, width=100, height=20)

        self.result_carton = ttk.Label(root, text="")
        self.result_carton.place(x=25, y=500, width=70, height=70)
        self.label_carton = ttk.Label(root, text="")
        self.label_carton.place(x=100, y=515, width=35, height=40)
        self.name_carton = ttk.Label(root, text="", anchor="center")
        self.name_carton.place(x=10, y=570, width=100, height=20)

        self.result_pallet = ttk.Label(root, text="")
        self.result_pallet.place(x=145, y=500, width=70, height=70)
        self.label_pallet = ttk.Label(root, text="")
        self.label_pallet.place(x=220, y=515, width=35, height=40)
        self.name_pallet = ttk.Label(root, text="", anchor="center")
        self.name_pallet.place(x=130, y=570, width=100, height=20)

        self.result_ship = ttk.Label(root, text="")
        self.result_ship.place(x=265, y=500, width=70, height=70)
        self.name_ship = ttk.Label(root, text="", anchor="center")
        self.name_ship.place(x=250, y=570, width=100, height=20)


    def show_result_firmware(self, mcu_id, log):
        data, trans_time = get_data_firmware_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_firmware, 'Resource/OK.png')
            show_image_narrow(self.label_firmware, 'Resource/arrowtoleft.png')
            self.name_firmware.config(text="FIRMWARE", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Firmware kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_firmware, 'Resource/NG.png')
            show_image_narrow(self.label_firmware, 'Resource/arrowtoleft.png')
            self.name_firmware.config(text="FIRMWARE", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Firmware NG hoặc SKIP!.\n", "NG")
        # Delay Time

        self.root.after(200, self.show_result_pba, mcu_id, log)
        
        
    def show_result_pba(self,mcu_id,log):
        data, trans_time = get_data_pba_function_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_pba, 'Resource/OK.png')
            show_image_narrow(self.label_pba, 'Resource/arrowtoleft.png')
            self.name_pba.config(text="PBA_FUNCTION", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Function PBA kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_pba, 'Resource/NG.png')
            show_image_narrow(self.label_pba, 'Resource/arrowtoleft.png')
            self.name_pba.config(text="PBA_FUNCTION", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Function PBA NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_heater, mcu_id, log)

    def show_result_heater(self,mcu_id, log):
        data, trans_time = get_data_heater_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_heater, 'Resource/OK.png')
            show_image_narrow(self.label_heater, 'Resource/arrowtoleft.png')
            self.name_heater.config(text="HEATER_TEST", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Heater_Test kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_heater, 'Resource/NG.png')
            show_image_narrow(self.label_heater, 'Resource/arrowtoleft.png')
            self.name_heater.config(text="HEATER_TEST", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Heater_Test NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_matching, mcu_id, log)

    def show_result_matching(self,mcu_id, log):
        data, trans_time = get_data_matching_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_matching, 'Resource/OK.png')
            show_image_narrow(self.label_matching, 'Resource/arrowtoleft.png')
            self.name_matching.config(text="3QR_MATCHING", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Matching 3QR kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_matching, 'Resource/NG.png')
            show_image_narrow(self.label_matching, 'Resource/arrowtoleft.png')
            self.name_matching.config(text="3QR_MATCHING", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Matching 3QR NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_charge, mcu_id, log)

    def show_result_charge(self,mcu_id, log):
        data, trans_time = get_data_charge_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_charge, 'Resource/OK.png')
            show_image_narrow(self.label_charge, 'Resource/arrowtoleft.png')
            self.name_charge.config(text="CHARGE", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Charge kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_charge, 'Resource/NG.png')
            show_image_narrow(self.label_charge, 'Resource/arrowtoleft.png')
            self.name_charge.config(text="CHARGE", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Charge NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_cali, mcu_id, log)

    def show_result_cali(self,mcu_id, log):
        data, trans_time = get_data_cali_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_cali, 'Resource/OK.png')
            show_image_narrow(self.label_cali, 'Resource/arrowtoleft.png')
            self.name_cali.config(text="CALIBRATION", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Calibration kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_cali, 'Resource/NG.png')
            show_image_narrow(self.label_cali, 'Resource/arrowtoleft.png')
            self.name_cali.config(text="CALIBRATION", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Calibration NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_verifi, mcu_id, log)

    def show_result_verifi(self,mcu_id, log):
        data, trans_time = get_data_verifi_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_verifi, 'Resource/OK.png')
            show_image_narrow(self.label_verifi, 'Resource/arrowtoleft.png')
            self.name_verifi.config(text="VERIFICATION", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Verification kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_verifi, 'Resource/NG.png')
            show_image_narrow(self.label_verifi, 'Resource/arrowtoleft.png')
            self.name_verifi.config(text="VERIFICATION", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Verification NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_MMI, mcu_id, log)

    def show_result_MMI(self,mcu_id, log):
        data, trans_time = get_data_mmi_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_puff, 'Resource/OK.png')
            show_image_narrow(self.label_puff, 'Resource/arrowtodown.png')
            self.name_puff.config(text="MMI", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn MMI kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_puff, 'Resource/NG.png')
            show_image_narrow(self.label_puff, 'Resource/arrowtodown.png')
            self.name_puff.config(text="MMI", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn MMI NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_vibration, mcu_id, log)

    def show_result_vibration(self,mcu_id, log):
        data, trans_time = get_data_vibration_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_sensor, 'Resource/OK.png')
            show_image_narrow(self.label_sensor, 'Resource/arrowtoright.png')
            self.name_sensor.config(text="VIBRATION", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Vibration kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_sensor, 'Resource/NG.png')
            show_image_narrow(self.label_sensor, 'Resource/arrowtoright.png')
            self.name_sensor.config(text="VIBRATION", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Vibration NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_snwriting, mcu_id, log)

    def show_result_snwriting(self,mcu_id, log):
        data, trans_time = get_data_snwriting_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_sn, 'Resource/OK.png')
            show_image_narrow(self.label_sn, 'Resource/arrowtoright.png')
            self.name_sn.config(text="SN_WRITING", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn SN Writing kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_sn, 'Resource/NG.png')
            show_image_narrow(self.label_sn, 'Resource/arrowtoright.png')
            self.name_sn.config(text="SN_WRITING", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn SN Writing NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_final, mcu_id, log)

    def show_result_final(self,mcu_id, log):
        data, trans_time = get_data_final_P1(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'OK':
            show_image(self.result_final, 'Resource/OK.png')
            show_image_narrow(self.label_final, 'Resource/arrowtoright.png')
            self.name_final.config(text="FINAL_TEST", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Final Test kết quả OK vào lúc {trans_time}.\n", "OK")
        else:
            show_image(self.result_final, 'Resource/NG.png')
            show_image_narrow(self.label_final, 'Resource/arrowtoright.png')
            self.name_final.config(text="FINAL_TEST", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Final Test NG or SKIP!.\n", "NG")
        self.root.after(200, self.show_result_deviceid, mcu_id, log)

    def show_result_deviceid(self,mcu_id, log):
        data, trans_time = get_data_deviceid(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_device, 'Resource/NG.png')
            show_image_narrow(self.label_device, 'Resource/arrowtoright.png')
            self.name_device.config(text="MES_ATTACH", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Device ID Attach NG or SKIP!.\n", "NG")
            
        else:
            show_image(self.result_device, 'Resource/OK.png')
            show_image_narrow(self.label_device, 'Resource/arrowtoright.png')
            self.name_device.config(text="MES_ATTACH", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Device ID Attach kết quả OK vào lúc {trans_time}.\n", "OK")
        self.root.after(200, self.show_result_giftbox, mcu_id, log)

    def show_result_giftbox(self,mcu_id, log):
        data, trans_time = get_data_giftbox(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_giftbox, 'Resource/NG.png')
            show_image_narrow(self.label_giftbox, 'Resource/arrowtoright.png')
            self.name_giftbox.config(text="GIFTBOX", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Giftbox NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_giftbox, 'Resource/OK.png')
            show_image_narrow(self.label_giftbox, 'Resource/arrowtoright.png')
            self.name_giftbox.config(text="GIFTBOX", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Giftbox kết quả OK vào lúc {trans_time}.\n", "OK")
        self.root.after(200, self.show_result_film, mcu_id, log)
    
    def show_result_film(self,mcu_id, log):
        data, trans_time = get_data_film(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_film, 'Resource/NG.png')
            show_image_narrow(self.label_film, 'Resource/arrowtoright.png')
            self.name_film.config(text="FILM_GUIDE", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Film Guide NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_film, 'Resource/OK.png')
            show_image_narrow(self.label_film, 'Resource/arrowtoright.png')
            self.name_film.config(text="FILM_GUIDE", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Film Guide kết quả OK vào lúc {trans_time}.\n", "OK")
            
        self.root.after(200, self.show_result_sleeve, mcu_id, log)
    
    def show_result_sleeve(self,mcu_id, log):
        data, trans_time = get_data_sleeve(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_sleeve, 'Resource/NG.png')
            show_image_narrow(self.label_sleeve, 'Resource/arrowtoright.png')
            self.name_sleeve.config(text="SLEEVE", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Sleeve NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_sleeve, 'Resource/OK.png')
            show_image_narrow(self.label_sleeve, 'Resource/arrowtoright.png')
            self.name_sleeve.config(text="SLEEVE", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Sleeve kết quả OK vào lúc {trans_time}.\n", "OK")
        self.root.after(200, self.show_result_weigh, mcu_id, log)

    def show_result_weigh(self,mcu_id, log):
        data, trans_time = get_data_weigh(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_weigh, 'Resource/NG.png')
            show_image_narrow(self.label_weigh, 'Resource/arrowtodown.png')
            self.name_weigh.config(text="WEIGH", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Weigh NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_weigh, 'Resource/OK.png')
            show_image_narrow(self.label_weigh, 'Resource/arrowtodown.png')
            self.name_weigh.config(text="WEIGH", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Weigh kết quả OK vào lúc {trans_time}.\n", "OK")
        self.root.after(200, self.show_result_carton, mcu_id, log)

    def show_result_carton(self,mcu_id, log):
        data, trans_time = get_data_cartonbox(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_carton, 'Resource/NG.png')
            show_image_narrow(self.label_carton, 'Resource/arrowtoleft.png')
            self.name_carton.config(text="CARTON_BOX", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Cartonbox NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_carton, 'Resource/OK.png')
            show_image_narrow(self.label_carton, 'Resource/arrowtoleft.png')
            self.name_carton.config(text="CARTON_BOX", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Cartonbox kết quả OK vào lúc {trans_time}.\n", "OK")
        self.root.after(200, self.show_result_pallet, mcu_id, log)

    def show_result_pallet(self,mcu_id, log):
        data, trans_time = get_data_pallet(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_pallet, 'Resource/NG.png')
            show_image_narrow(self.label_pallet, 'Resource/arrowtoleft.png')
            self.name_pallet.config(text="PALLET", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Pallet NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_pallet, 'Resource/OK.png')
            show_image_narrow(self.label_pallet, 'Resource/arrowtoleft.png')
            self.name_pallet.config(text="PALLET", font=("Arial", 9, "bold"))
            log_message(log, f"Kiểm tra MCU_ID: {mcu_id} công đoạn Pallet kết quả OK vào lúc {trans_time}.\n", "OK")
        self.root.after(200, self.show_result_shipping, mcu_id, log)

    def show_result_shipping(self,mcu_id, log):
        data, trans_time = get_data_shiping(mcu_id)
        if trans_time:
            trans_time = format_trans_time(trans_time)
        
        if data == 'SKIP':
            show_image(self.result_ship, 'Resource/NG.png')
            self.name_ship.config(text="SHIPPING", font=("Arial", 9, "bold"))
            log_message(log, f"MCU_ID: {mcu_id} công đoạn Shipping NG or SKIP!.\n", "NG")
        else:
            show_image(self.result_ship, 'Resource/OK.png')
            self.name_ship.config(text="SHIPPING", font=("Arial", 9, "bold"))
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

        mcu_id = get_device_id_P1(Device_id)
        if len(mcu_id) == 17:
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
        if len(mcu_id) != 17:
            messagebox.showwarning("Warning", "MCU_ID sai định dạng, vui lòng kiểm tra lại.")
            self.Input_MCUID.delete(0,tk.END)
            return
        if not mcu_id.startswith("P"):
            messagebox.showwarning("Warning", "MCU_ID sai định dạng, vui lòng kiểm tra lại.")
            self.Input_MCUID.delete(0, tk.END)
            return
        self.start(mcu_id)
        self.Input_MCUID.delete(0,tk.END)

    def start(self,mcu_id):
        self.is_running = True 

        self.Log.configure(state='normal')
        self.Log.delete(1.0, tk.END)
        self.Log.configure(state="disabled")

        self.result_firmware.config(text="", image="")
        self.label_firmware.config(text="", image="")
        self.name_firmware.config(text="")

        self.result_pba.config(text="", image="")
        self.label_pba.config(text="", image="")
        self.name_pba.config(text="")

        self.result_heater.config(text="", image="")
        self.label_heater.config(text="", image="")
        self.name_heater.config(text="")

        self.result_matching.config(text="", image="")
        self.label_matching.config(text="", image="")
        self.name_matching.config(text="")

        self.result_charge.config(text="", image="")
        self.label_charge.config(text="", image="")
        self.name_charge.config(text="")

        self.result_cali.config(text="", image="")
        self.label_cali.config(text="", image="")
        self.name_cali.config(text="")

        self.result_verifi.config(text="", image="")
        self.label_verifi.config(text="", image="")
        self.name_verifi.config(text="")

        self.result_puff.config(text="", image="")
        self.label_puff.config(text="", image="")
        self.name_puff.config(text="")

        self.result_sensor.config(text="", image="")
        self.label_sensor.config(text="", image="")
        self.name_sensor.config(text="")

        self.result_sn.config(text="", image="")
        self.label_sn.config(text="", image="")
        self.name_sn.config(text="")

        self.result_final.config(text="", image="")
        self.label_final.config(text="", image="")
        self.name_final.config(text="")

        self.result_device.config(text="", image="")
        self.label_device.config(text="", image="")
        self.name_device.config(text="")

        self.result_giftbox.config(text="", image="")
        self.label_giftbox.config(text="", image="")
        self.name_giftbox.config(text="")

        self.result_film.config(text="", image="")
        self.label_film.config(text="", image="")
        self.name_film.config(text="")

        self.result_sleeve.config(text="", image="")
        self.label_sleeve.config(text="", image="")
        self.name_sleeve.config(text="")

        self.result_weigh.config(text="", image="")
        self.label_weigh.config(text="", image="")
        self.name_weigh.config(text="")

        self.result_carton.config(text="", image="")
        self.label_carton.config(text="", image="")
        self.name_carton.config(text="")

        self.result_pallet.config(text="", image="")
        self.label_pallet.config(text="", image="")
        self.name_pallet.config(text="")

        self.result_ship.config(text="", image="")
        self.name_ship.config(text="")


        self.data_MCULabel.config(text=f"{mcu_id}")
        
        heater_id = get_heater_id_P1(mcu_id)
        self.data_HeaterLabel.config(text=f"{heater_id}")

        main_pba = get_main_pba_P1(mcu_id)
        self.data_MainPBALabel.config(text=f"{main_pba}")

        device_id = get_info_deviceid(mcu_id)
        self.data_DeviceLabel.config(text=f"{device_id}")

        giftbox_id = get_info_giftbox(mcu_id)
        self.data_GiftboxLabel.config(text=f"{giftbox_id}")

        cartonbox_id = get_info_cartonbox(mcu_id)
        self.data_CartonLabel.config(text=f"{cartonbox_id}")


        self.root.after(200, self.show_result_firmware, mcu_id, self.Log)



def create_gui_P1(create_login_ui, create_gui_P230, create_gui_P4, create_gui_P140):
    def logout():
        root_P1.destroy()
        create_login_ui()

    def switch_to_P230():
        root_P1.destroy()
        create_gui_P230(create_login_ui, create_gui_P1, create_gui_P4, create_gui_P140)

    def switch_to_P4():
        root_P1.destroy()
        create_gui_P4(create_login_ui, create_gui_P1, create_gui_P230, create_gui_P140)

    def switch_to_P140():
        root_P1.destroy()
        create_gui_P140(create_login_ui, create_gui_P1, create_gui_P230, create_gui_P4)


    root_P1 = tk.Tk()
    icon_mesconnect = ttk.Label(root_P1, text="")
    icon_mesconnect.place(x=10, y=795, width=25, height=25)
    name_mesconnect = ttk.Label(root_P1, text="", anchor="w")
    name_mesconnect.place(x=40, y=795, width=200, height=25)
    Copyright = ttk.Label(root_P1, text="Powered by ITM Semiconductor Vietnam Company Limited - IT Team. Copyright © 2024 all rights reserved.", anchor="w")
    Copyright.place(x=380, y=795, width=570, height=25)

    menubar = tk.Menu(root_P1)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Chuyển sang ECIGA-P2 3.0", command=switch_to_P230)
    file_menu.add_command(label="Chuyển sang ECIGA-P4", command=switch_to_P4)
    file_menu.add_command(label="Chuyển sang ECIGA-P140", command=switch_to_P140)
    file_menu.add_command(label="Đăng xuất", command=logout)
    menubar.add_cascade(label="Menu", menu=file_menu)
    
    root_P1.config(menu=menubar)

    check_ping(icon_mesconnect, name_mesconnect)

    ui = Data_P1EZ_Checker(root_P1)
    root_P1.mainloop()

