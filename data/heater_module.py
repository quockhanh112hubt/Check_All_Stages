import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_data_heater_module_aging_P140(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
                MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT HEATER.TOTAL_JUDGMENT, HEATER.TRANS_TIME, RANK() OVER (ORDER BY HEATER.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P140_HEATER_MODULE_AGING_HISTORY HEATER
                INNER JOIN MIGHTY.ADC_P140_SNRW_HISTORY SNRW ON SNRW.HEATER_MODULE_ID = HEATER.HEATER_MODULE_ID
                WHERE SNRW.MCU_ID = :mcu_id
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

def get_data_heater_module_function_P140(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
                MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT HEATER.TOTAL_JUDGMENT, HEATER.TRANS_TIME, RANK() OVER (ORDER BY HEATER.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P140_HEATER_MODULE_FUNCTION_HISTORY HEATER
                INNER JOIN MIGHTY.ADC_P140_SNRW_HISTORY SNRW ON SNRW.HEATER_MODULE_ID = HEATER.HEATER_MODULE_ID
                WHERE SNRW.MCU_ID = :mcu_id
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

def get_data_cover_heater_function_P140(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
            MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT HEATER.TOTAL_JUDGMENT, HEATER.TRANS_TIME, RANK() OVER (ORDER BY HEATER.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P140_COVER_HEATER_FUNCTION_HISTORY HEATER
                INNER JOIN MIGHTY.ADC_P140_ID_MATCHING_HISTORY MATCHING ON MATCHING.COVER_HEATER_ID = HEATER.COVER_HEATER_ID
                INNER JOIN MIGHTY.ADC_P140_PBA_FUNCTION_HISTORY PBA ON PBA.PBA_ID = MATCHING.PBA_ID
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

def get_heater_id_P140(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.COVER_HEATER_ID), 'SKIP') AS RESULT 
            FROM (
                SELECT HEATER.COVER_HEATER_ID, MATCHING.TRANS_TIME, 
                    ROW_NUMBER() OVER (ORDER BY MATCHING.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P140_COVER_HEATER_FUNCTION_HISTORY HEATER
                INNER JOIN MIGHTY.ADC_P140_ID_MATCHING_HISTORY MATCHING 
                    ON MATCHING.COVER_HEATER_ID = HEATER.COVER_HEATER_ID
                INNER JOIN MIGHTY.ADC_P140_PBA_FUNCTION_HISTORY PBA 
                    ON PBA.PBA_ID = MATCHING.PBA_ID
                WHERE PBA.MCU_ID = :mcu_id
            ) R
            WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return 'NO DATA'
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def get_heater_module_id_P140(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.HEATER_MODULE_ID), 'SKIP') AS RESULT 
            FROM (
                SELECT HEATER_MODULE_ID,
                    ROW_NUMBER() OVER (ORDER BY SNWR.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P140_SNRW_HISTORY SNWR
                WHERE APPLY_FLAG = 'Y' AND SNWR.MCU_ID = :mcu_id
            ) R
            WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return 'NO DATA'
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
