import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_data_weigh(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(R.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
            MAX(R.TRANS_TIME) AS TRANS_TIME 
            FROM (
                SELECT WEIGHT.TOTAL_JUDGMENT, WEIGHT.TRANS_TIME, RANK() OVER (ORDER BY WEIGHT.TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_WEIGHT_HISTORY WEIGHT
                INNER JOIN MIGHTY.ASFC_SUBLOT_INFO MATCHING ON MATCHING.GIFT_BOX_ID = WEIGHT.GIFT_BOX_ID
                WHERE MATCHING.MCU_ID = :mcu_id
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
