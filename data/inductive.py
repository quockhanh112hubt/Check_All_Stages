import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from utils.db_config import get_db_connection

def get_data_inductive(mcu_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT NVL(MAX(A.TOTAL_JUDGMENT), 'SKIP') AS RESULT, 
            MAX(A.TRANS_TIME) AS TRANS_TIME 
            FROM
            (
                SELECT MCU_ID, TOTAL_JUDGMENT, TRANS_TIME, 
                    RANK() OVER (PARTITION BY MCU_ID ORDER BY TRANS_TIME DESC) AS RNK
                FROM MIGHTY.ADC_P3_INDUCTIVE_TEST_HISTORY
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

