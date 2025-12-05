import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_data_deviceid(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.DEVICE_ID), 'SKIP') AS RESULT,
            MAX(A.DEVICE_ATTACH_DATE) AS TRANS_TIME
            FROM
            (
                SELECT MCU_ID, DEVICE_ID, DEVICE_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY DEVICE_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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

def get_data_giftbox(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.GIFT_BOX_ID), 'SKIP') AS RESULT, 
            MAX(A.GBOX_ATTACH_DATE) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, GIFT_BOX_ID, GBOX_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY GBOX_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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

def get_data_film(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.FILM_ID), 'SKIP') AS RESULT, 
            MAX(A.FILM_ATTACH_DATE) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, FILM_ID, FILM_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY FILM_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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

def get_data_sleeve(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.SLEEVE_ID), 'SKIP') AS RESULT, 
            MAX(A.SLEEVE_ATTACH_DATE) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, SLEEVE_ID, SLEEVE_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY SLEEVE_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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

def get_data_cartonbox(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.CARTON_BOX_ID), 'SKIP') AS RESULT, 
            MAX(A.CBOX_ATTACH_DATE) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, CARTON_BOX_ID, CBOX_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY CBOX_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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

def get_data_pallet(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.PALLET_ID), 'SKIP') AS RESULT, 
            MAX(A.PALLET_ATTACH_DATE) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, PALLET_ID, PALLET_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY PALLET_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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

def get_data_shiping(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.SHIPMENT_ID), 'SKIP') AS RESULT, 
            MAX(A.SHIP_DATE) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, SHIPMENT_ID, SHIP_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY SHIP_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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


#Check Information
def get_info_deviceid(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.DEVICE_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, DEVICE_ID, DEVICE_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY DEVICE_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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


def get_info_giftbox(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.GIFT_BOX_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, GIFT_BOX_ID, GBOX_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY GBOX_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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


def get_info_cartonbox(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.CARTON_BOX_ID), 'SKIP') AS RESULT
            FROM
            (
                SELECT MCU_ID, CARTON_BOX_ID, CBOX_ATTACH_DATE, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY CBOX_ATTACH_DATE DESC) AS RNK
                FROM MIGHTY.ASFC_SUBLOT_INFO
                WHERE MCU_ID = :mcu_id
            ) A 
            WHERE A.RNK = 1
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
