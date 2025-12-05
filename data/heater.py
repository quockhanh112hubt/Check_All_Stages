import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_data_heater(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
            MAX(R.TRANS_TIME) AS TRANS_TIME 
        FROM (
            SELECT SLEEP.TOTAL_JUDGMENT, SLEEP.TRANS_TIME, RANK() OVER (ORDER BY SLEEP.TRANS_TIME DESC) AS RNK
            FROM MIGHTY.ADC_P3_RESISTANCE_TEST_HISTORY SLEEP
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

def get_heater_id(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
                SELECT NVL(MAX(R.HEATER_ID), 'SKIP') AS RESULT 
                FROM (
                    SELECT HEATER.HEATER_ID, MATCHING.TRANS_TIME, 
                        ROW_NUMBER() OVER (ORDER BY MATCHING.TRANS_TIME DESC) AS RNK
                    FROM MIGHTY.ADC_P3_RESISTANCE_TEST_HISTORY HEATER
                    INNER JOIN MIGHTY.ADC_P3_MATCHING_HISTORY MATCHING 
                        ON MATCHING.HEATER_ID = HEATER.HEATER_ID
                    INNER JOIN MIGHTY.ADC_P3_PBA_FUNCTION_HISTORY PBA 
                        ON PBA.PBA_QR_CODE = MATCHING.PBA_ID
                    WHERE PBA.MCU_ID = :mcu_id
                ) R
                WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_data_heater_P4(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
                MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT SLEEP.TOTAL_JUDGMENT, SLEEP.TRANS_TIME, RANK() OVER (ORDER BY SLEEP.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P4_RESISTANCE_TEST_HISTORY SLEEP
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

def get_heater_id_P4(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.HEATER_ID), 'SKIP') AS RESULT 
            FROM (
                SELECT HEATER.HEATER_ID, HEATER.TRANS_TIME, RANK() OVER (ORDER BY HEATER.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P4_RESISTANCE_TEST_HISTORY HEATER
                INNER JOIN MIGHTY.ADC_P4_ID_MATCHING_HISTORY MATCHING ON MATCHING.HEATER_ID = HEATER.HEATER_ID
                INNER JOIN MIGHTY.ADC_P4_PBA_FUNCTION_HISTORY PBA ON PBA.PBA_QR_CODE = MATCHING.PBA_ID
                WHERE PBA.MCU_ID = :mcu_id
            ) R
            WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_data_heater_P1(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
                MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT SLEEP.TOTAL_JUDGMENT, SLEEP.TRANS_TIME, RANK() OVER (ORDER BY SLEEP.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_RESISTANCE_TEST_HISTORY SLEEP
                INNER JOIN MIGHTY.ADC_ID_MATCHING_HISTORY MATCHING ON MATCHING.HEATER_ID = SLEEP.HEATER_ID
                INNER JOIN MIGHTY.ADC_P1VX_FUNCTION_HISTORY PBA ON PBA.BARCODE = MATCHING.PBA_ID
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

def get_heater_id_P1(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.HEATER_ID), 'SKIP') AS RESULT 
            FROM (
                SELECT HEATER.HEATER_ID, HEATER.TRANS_TIME, RANK() OVER (ORDER BY HEATER.TRANS_TIME DESC) AS RNK
	            FROM MIGHTY.ADC_RESISTANCE_TEST_HISTORY HEATER
	            INNER JOIN MIGHTY.ADC_ID_MATCHING_HISTORY MATCHING ON MATCHING.HEATER_ID = HEATER.HEATER_ID
	            INNER JOIN MIGHTY.ADC_P1VX_FUNCTION_HISTORY PBA ON PBA.BARCODE = MATCHING.PBA_ID
                WHERE PBA.MCU_ID = :mcu_id
            ) R
            WHERE R.RNK = 1
        """
        cursor.execute(query, {'mcu_id': mcu_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()