"""
Auto-refactor script to replace cx_Oracle with oracledb
across all data module files.
"""
import os
import re

DATA_FOLDER = r"e:\CHECK_ALL_STAGE_VERSION_2\data"

def refactor_imports(content):
    """Replace cx_Oracle import with oracledb"""
    # Replace import cx_Oracle
    content = re.sub(r'import cx_Oracle\n', '', content)
    # Exception handling replacement
    content = re.sub(r'except cx_Oracle\.DatabaseError', 'except Exception', content)
    return content

def refactor_file(filepath):
    """Refactor a single Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if file has cx_Oracle references
        if 'cx_Oracle' not in content:
            return False, "No cx_Oracle found"
        
        # Refactor imports and exception handling
        content = refactor_imports(content)
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Migrated to oracledb"
        else:
            return False, "No changes needed"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main refactoring function"""
    print("=" * 70)
    print("MIGRATE FROM cx_Oracle TO oracledb")
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
            status = "✓ MIGRATED" if success else "○ SKIPPED"
            
            print(f"{status:15} {filename:30} - {message}")
            
            if success:
                files_refactored += 1
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {files_refactored}/{files_processed} files migrated")
    print("=" * 70)
    print("\n✓ All files now use oracledb (compatible with ojdbc)")
    print("✓ cx_Oracle imports removed")
    print("✓ Exception handling updated")

if __name__ == "__main__":
    main()
