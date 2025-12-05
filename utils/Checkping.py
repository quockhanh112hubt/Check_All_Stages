import subprocess
import threading
from utils.config_manager import load_config

def check_ping(status_label):
    """
    Check database connection by pinging the configured DB host.
    Automatically detects which DB type is being used (oracledb or cx_Oracle)
    and pings the corresponding host.
    """
    def ping():
        try:
            # Check if widget still exists before proceeding
            if not status_label.winfo_exists():
                return
            
            # Load config to get active database settings
            config = load_config()
            db_settings = config.get('database_settings', {})
            connection_type = db_settings.get('connection_type', 'oracledb')
            
            # Get hostname based on connection type
            if connection_type == 'cx_oracle':
                # For cx_Oracle, parse host from DSN string
                dsn = db_settings.get('cx_oracle', {}).get('dsn', '')
                # Extract host from DSN: (DESCRIPTION=...HOST=xxx.xxx.xxx.xxx...
                hostname = None
                if 'HOST=' in dsn:
                    start = dsn.index('HOST=') + 5
                    end = dsn.index(')', start) if ')' in dsn[start:] else len(dsn)
                    hostname = dsn[start:end].strip()
                
                if not hostname:
                    hostname = "192.168.35.20"  # Fallback
                db_type_label = "cx_Oracle"
            else:
                # For oracledb, get host directly
                hostname = db_settings.get('oracledb', {}).get('host', '10.162.200.20')
                db_type_label = "oracledb"
            
            # Perform ping
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            response = subprocess.call(
                ["ping", "-n", "1", hostname], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                startupinfo=startupinfo
            )
            
            # Check again before updating UI
            if not status_label.winfo_exists():
                return
            
            # Update status label
            if response == 0:
                status_label.after(0, lambda: status_label.config(
                    text=f"🟢 Database Connected ({db_type_label} @ {hostname})",
                    foreground='#10b981'  # Green
                ))
            else:
                status_label.after(0, lambda: status_label.config(
                    text=f"🔴 Database Disconnected ({db_type_label} @ {hostname})",
                    foreground='#ef4444'  # Red
                ))
            
            # Schedule next check only if widget still exists
            if status_label.winfo_exists():
                status_label.after(3000, check_ping, status_label)
        except Exception as e:
            # Silently ignore errors if widget was destroyed
            if status_label.winfo_exists():
                status_label.after(0, lambda: status_label.config(
                    text=f"⚠️ Database Status Unknown",
                    foreground='#f59e0b'  # Orange
                ))
    
    threading.Thread(target=ping, daemon=True).start()