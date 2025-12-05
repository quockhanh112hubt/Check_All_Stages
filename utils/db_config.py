import oracledb
from tkinter import messagebox
from utils.config_manager import get_db_config

# Import cx_Oracle if available
try:
    import cx_Oracle
    CX_ORACLE_AVAILABLE = True
except ImportError:
    CX_ORACLE_AVAILABLE = False
    print("cx_Oracle not available. Only oracledb will be used.")

# Database connection configuration
# Using python-oracledb (thin mode - pure Python, no Oracle Client needed)
# Configuration is now loaded from config.json
def get_db_config_dict():
    """Get database configuration from config.json"""
    return get_db_config()

DB_CONFIG = get_db_config_dict()

def get_db_connection():
    """
    Create and return a database connection using centralized configuration.
    Supports both oracledb (thin mode) and cx_Oracle connections.
    Reloads config from file each time to get latest settings.
    
    Returns:
        Connection: Database connection object (oracledb.Connection or cx_Oracle.Connection)
        
    Raises:
        DatabaseError: If connection fails
    """
    try:
        # Reload config to get latest settings
        db_config = get_db_config_dict()
        connection_type = db_config.get('connection_type', 'oracledb')
        
        if connection_type == 'cx_oracle':
            if not CX_ORACLE_AVAILABLE:
                messagebox.showerror("Connection Error", "cx_Oracle is not installed. Please install it or use oracledb connection type.")
                raise ImportError("cx_Oracle not available")
            
            # cx_Oracle connection using DSN
            cx_config = db_config['cx_oracle']
            connection = cx_Oracle.connect(
                user=cx_config['user'],
                password=cx_config['password'],
                dsn=cx_config['dsn']
            )
            return connection
        else:
            # oracledb thin mode connection (default)
            oracle_config = db_config['oracledb']
            connection = oracledb.connect(
                user=oracle_config['user'],
                password=oracle_config['password'],
                host=oracle_config['host'],
                port=oracle_config['port'],
                service_name=oracle_config['service_name']
            )
            return connection
            
    except (oracledb.DatabaseError, cx_Oracle.DatabaseError if CX_ORACLE_AVAILABLE else Exception) as e:
        messagebox.showerror("Database Connection Error", f"Cannot connect to database: {str(e)}")
        raise

def execute_query(query, params=None):
    """
    Execute a SELECT query and return results.
    Automatically handles connection and cursor management.
    Works with both oracledb and cx_Oracle connections.
    
    Args:
        query (str): SQL query string
        params (dict, optional): Query parameters
        
    Returns:
        tuple: Query result or None if error
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        result = cursor.fetchone()
        return result
    except Exception as e:
        messagebox.showerror("Database Query Error", str(e))
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
