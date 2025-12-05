import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_device_id(Device_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.MCU_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, DEVICE_ID, TRANS_TIME, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P3_SNRW_HISTORY
                WHERE DEVICE_ID = :device_id
            ) A 
            WHERE A.RNK = 1
        """
        cursor.execute(query, {'device_id': Device_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_device_id_P4(Device_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.MCU_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, DEVICE_ID, TRANS_TIME, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P4_SNRW_HISTORY
                WHERE DEVICE_ID = :device_id
            ) A 
            WHERE A.RNK = 1
        """
        cursor.execute(query, {'device_id': Device_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_device_id_P1(Device_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.MCU_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, DEVICE_ID, TRANS_TIME, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P1VX_SNRW_HISTORY
                WHERE DEVICE_ID = :device_id
            ) A 
            WHERE A.RNK = 1
        """
        cursor.execute(query, {'device_id': Device_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_device_id_P140(Device_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.MCU_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, DEVICE_ID, TRANS_TIME, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P140_SNRW_HISTORY
                WHERE DEVICE_ID = :device_id
            ) A 
            WHERE A.RNK = 1
        """
        cursor.execute(query, {'device_id': Device_id})
        result = cursor.fetchone()
        return result[0] if result else 'NO DATA'
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
