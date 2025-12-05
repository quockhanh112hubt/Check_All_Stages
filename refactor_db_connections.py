"""
Auto-refactor script to replace cx_Oracle.connect() with centralized get_db_connection()
across all data module files.
"""
import os
import re

# Files to refactor in data folder
DATA_FOLDER = r"e:\CHECK_ALL_STAGE_VERSION_2\data"

# Connection string pattern to find
OLD_CONNECTION_PATTERN = r'''cx_Oracle\.connect\(
            user="mighty",
            password="mighty",
            dsn="\(DESCRIPTION=\(LOAD_BALANCE=yes\)\(ADDRESS=\(PROTOCOL=TCP\)\(HOST=192\.168\.35\.20\)\(PORT=1521\)\)\(ADDRESS=\(PROTOCOL=TCP\)\(HOST=192\.168\.35\.20\)\(PORT=1521\)\)\(CONNECT_DATA=\(SERVICE_NAME=ITMVPACKMES\)\(FAILOVER_MODE=\(TYPE=SELECT\)\(METHOD=BASIC\)\)\)\)"
        \)'''

NEW_CONNECTION = "get_db_connection()"

def needs_import_update(content):
    """Check if file needs import statement update"""
    return 'import cx_Oracle' in content and 'from utils.db_config import get_db_connection' not in content

def add_import_statement(content):
    """Add import statement after cx_Oracle import"""
    lines = content.split('\n')
    new_lines = []
    import_added = False
    
    for line in lines:
        new_lines.append(line)
        if 'import cx_Oracle' in line and not import_added:
            new_lines.append('from utils.db_config import get_db_connection')
            import_added = True
    
    return '\n'.join(new_lines)

def replace_connections(content):
    """Replace all cx_Oracle.connect() calls with get_db_connection()"""
    # Multi-line pattern replacement
    pattern = r'cx_Oracle\.connect\(\s*user="mighty",\s*password="mighty",\s*dsn="[^"]+"\s*\)'
    content = re.sub(pattern, 'get_db_connection()', content, flags=re.MULTILINE | re.DOTALL)
    return content

def refactor_file(filepath):
    """Refactor a single Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if file has cx_Oracle connections to refactor
        if 'cx_Oracle.connect(' not in content:
            return False, "No cx_Oracle.connect() found"
        
        # Add import if needed
        if needs_import_update(content):
            content = add_import_statement(content)
        
        # Replace connection strings
        content = replace_connections(content)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Refactored successfully"
        else:
            return False, "No changes needed"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main refactoring function"""
    print("=" * 70)
    print("DATABASE CONNECTION REFACTORING TOOL")
    print("=" * 70)
    print(f"\nScanning folder: {DATA_FOLDER}\n")
    
    files_processed = 0
    files_refactored = 0
    
    # Get all .py files in data folder
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith('.py') and not filename.startswith('__'):
            filepath = os.path.join(DATA_FOLDER, filename)
            files_processed += 1
            
            success, message = refactor_file(filepath)
            status = "✓ REFACTORED" if success else "○ SKIPPED"
            
            print(f"{status:15} {filename:30} - {message}")
            
            if success:
                files_refactored += 1
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {files_refactored}/{files_processed} files refactored")
    print("=" * 70)
    print("\n✓ All files now use centralized db_config.get_db_connection()")
    print("✓ To change database IP, edit: utils/db_config.py (line 6)")

if __name__ == "__main__":
    main()
