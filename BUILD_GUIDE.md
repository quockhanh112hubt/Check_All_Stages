# BUILD INSTRUCTIONS FOR CHECK_ALL_STAGE

## Prerequisites
1. Python 3.8 or higher installed
2. pip package manager installed

## Method 1: Quick Build (Recommended)
Simply double-click on `build_exe.bat` file.
This will:
- Clean previous build
- Install/update all required packages
- Build the executable
- Copy the .exe to root folder

## Method 2: Manual Build

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Clean previous build (optional)
```bash
rmdir /s /q build
rmdir /s /q dist
```

### Step 3: Build with PyInstaller
```bash
pyinstaller --clean Check_All_Stage.spec
```

### Step 4: Find your executable
The executable will be in: `dist\Check_All_Stage.exe`

## Important Notes

### Required Files/Folders (must be in same directory as .exe):
- `Resource/` folder - Contains images, icons, backgrounds
- `config.json` - Configuration file (auto-created if missing)
- `login_info.ini` - Login info (auto-created if missing)

### Build Output:
- **Single File EXE**: All dependencies bundled in one file
- **No Console Window**: Application runs with GUI only
- **Icon**: Uses Resource\Icon.ico

### Common Issues:

1. **Import errors during build**
   - Solution: Add missing module to `hiddenimports` in Check_All_Stage.spec

2. **Missing Resource files**
   - Solution: Ensure Resource folder is in `datas` section of .spec file

3. **cx_Oracle not found**
   - Solution: This is optional, only needed if using cx_Oracle connection type
   - Can skip if only using oracledb

4. **Large file size**
   - Normal: ~100-150 MB due to bundled libraries
   - Can reduce by excluding unused modules in `excludes` section

## Testing the Build

After building:
1. Copy these to the same folder as Check_All_Stage.exe:
   - Resource folder
   - config.json (or it will be auto-created)
   
2. Run Check_All_Stage.exe
3. Test login functionality
4. Test database connection in Settings
5. Test all product types (P1, P4, P230, P140)

## Distribution

To distribute the application:
1. Create a folder structure:
   ```
   Check_All_Stage/
   ├── Check_All_Stage.exe
   ├── config.json
   ├── Resource/
   │   ├── background.jpg
   │   ├── Icon.ico
   │   └── (all other resource files)
   └── (optional) login_info.ini
   ```

2. Zip the entire folder
3. Users only need to extract and run Check_All_Stage.exe

## Build Environment Info
- PyInstaller: Creates standalone executable
- Compression: UPX enabled for smaller file size
- Python Mode: Optimized bytecode (optimize=0 for debugging)
- Console: Disabled (GUI only)

## Troubleshooting Build Errors

### Error: Module not found
Add to `hiddenimports` in .spec file

### Error: Can't find Resource files
Check `datas` section in .spec file

### Error: oracledb/cx_Oracle import error
Make sure the packages are installed:
```bash
pip install oracledb cx-Oracle
```

For more help, check PyInstaller documentation:
https://pyinstaller.org/en/stable/
