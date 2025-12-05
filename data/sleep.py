import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_data_sleep(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
            MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT SLEEP.TOTAL_JUDGMENT, SLEEP.TRANS_TIME, RANK() OVER (ORDER BY SLEEP.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P3_SLEEP_INSPECTION_HISTORY SLEEP
                INNER JOIN MIGHTY.ADC_P3_MATCHING_HISTORY MATCHING ON MATCHING.HEATER_ID = SLEEP.HEATER_ID
                INNER JOIN MIGHTY.ADC_P3_PBA_FUNCTION_HISTORY PBA ON PBA.PBA_QR_CODE = MATCHING.PBA_ID
                WHERE PBA.MCU_ID = :mcu_id
            ) R
            WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return (result[0], result[1]) if result else ('SKIP', None)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return ('SKIP', None)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_data_sleep_P4(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
            MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT SLEEP.TOTAL_JUDGMENT, SLEEP.TRANS_TIME, RANK() OVER (ORDER BY SLEEP.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P4_SLEEP_INSPECTION_HISTORY SLEEP
                INNER JOIN MIGHTY.ADC_P4_ID_MATCHING_HISTORY MATCHING ON MATCHING.HEATER_ID = SLEEP.HEATER_ID
                INNER JOIN MIGHTY.ADC_P4_PBA_FUNCTION_HISTORY PBA ON PBA.PBA_QR_CODE = MATCHING.PBA_ID
                WHERE PBA.MCU_ID = :mcu_id
            ) R
            WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return (result[0], result[1]) if result else ('SKIP', None)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return ('SKIP', None)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()