import json
import os

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    "program_settings": {
        "program_directory": "C:\\Check_All_Stage",
        "ftp_server": "10.62.102.5",
        "ftp_user": "update",
        "ftp_password": "update",
        "ftp_directory": "KhanhDQ/Update_Program/Check_All_Stage/"
    },
    "database_settings": {
        "connection_type": "oracledb",
        "oracledb": {
            "user": "mighty",
            "password": "mighty",
            "host": "10.162.200.20",
            "port": 1521,
            "service_name": "ITMVPACKMES"
        },
        "cx_oracle": {
            "user": "mighty",
            "password": "mighty",
            "dsn": "(DESCRIPTION=(LOAD_BALANCE=yes)(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.35.20)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.35.20)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=ITMVPACKMES)(FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC))))"
        }
    }
}

def load_config():
    """Load configuration from JSON file. Create default if not exists."""
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Migrate old config format to new format
        if 'database_settings' in config:
            db_settings = config['database_settings']
            # Check if old format (without connection_type)
            if 'connection_type' not in db_settings:
                # Convert old format to new format
                config['database_settings'] = {
                    "connection_type": "oracledb",
                    "oracledb": {
                        "user": db_settings.get('user', 'mighty'),
                        "password": db_settings.get('password', 'mighty'),
                        "host": db_settings.get('host', '10.162.200.20'),
                        "port": db_settings.get('port', 1521),
                        "service_name": db_settings.get('service_name', 'ITMVPACKMES')
                    },
                    "cx_oracle": DEFAULT_CONFIG['database_settings']['cx_oracle']
                }
                save_config(config)
        
        # Migrate old FTP format (ftp_base_url) to new format
        if 'program_settings' in config:
            prog_settings = config['program_settings']
            if 'ftp_base_url' in prog_settings and 'ftp_server' not in prog_settings:
                # Parse old ftp_base_url format: ftp://user:pass@host/path/
                ftp_url = prog_settings.get('ftp_base_url', '')
                try:
                    # Simple parsing for ftp://user:pass@host/path/
                    if ftp_url.startswith('ftp://'):
                        ftp_url = ftp_url[6:]  # Remove 'ftp://'
                        if '@' in ftp_url:
                            auth, rest = ftp_url.split('@', 1)
                            user, password = auth.split(':', 1) if ':' in auth else (auth, 'update')
                            if '/' in rest:
                                server, directory = rest.split('/', 1)
                            else:
                                server, directory = rest, ''
                            
                            config['program_settings']['ftp_server'] = server
                            config['program_settings']['ftp_user'] = user
                            config['program_settings']['ftp_password'] = password
                            config['program_settings']['ftp_directory'] = directory
                            # Remove old format
                            del config['program_settings']['ftp_base_url']
                            save_config(config)
                except:
                    # If parsing fails, use defaults
                    config['program_settings'].update({
                        'ftp_server': '10.62.102.5',
                        'ftp_user': 'update',
                        'ftp_password': 'update',
                        'ftp_directory': 'KhanhDQ/Update_Program/Check_All_Stage/'
                    })
                    if 'ftp_base_url' in config['program_settings']:
                        del config['program_settings']['ftp_base_url']
                    save_config(config)
        
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to JSON file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_program_directory():
    """Get program directory from config."""
    config = load_config()
    return config['program_settings']['program_directory']

def get_ftp_settings():
    """Get FTP settings from config."""
    config = load_config()
    return {
        'server': config['program_settings'].get('ftp_server', '10.62.102.5'),
        'user': config['program_settings'].get('ftp_user', 'update'),
        'password': config['program_settings'].get('ftp_password', 'update'),
        'directory': config['program_settings'].get('ftp_directory', 'KhanhDQ/Update_Program/Check_All_Stage/')
    }

def get_db_config():
    """Get database configuration from config."""
    config = load_config()
    return config['database_settings']
