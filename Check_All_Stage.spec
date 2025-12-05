# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Check_All_Stage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Resource', 'Resource'),  # Include all Resource files
        ('config.json', '.'),       # Include config file
        ('login_info.ini', '.'),    # Include login info if exists
    ],
    hiddenimports=[
        # Core modules
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.font',
        
        # Database drivers
        'oracledb',
        'oracledb.thin_impl',
        'oracledb.base_impl',
        'cx_Oracle',
        
        # Cryptography for oracledb (CRITICAL!)
        'cryptography',
        'cryptography.hazmat',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.ciphers',
        'cryptography.hazmat.primitives.ciphers.algorithms',
        'cryptography.hazmat.primitives.ciphers.modes',
        'cryptography.hazmat.backends',
        'cryptography.hazmat.backends.openssl',
        'cryptography.hazmat.backends.openssl.backend',
        '_cffi_backend',
        
        # Image processing
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'qrcode',
        'qrcode.image.pure',
        'qrcode.image.pil',
        
        # UI modules
        'ui.creategui_P1',
        'ui.creategui_P1_v2',
        'ui.creategui_P4',
        'ui.creategui_P4_v2',
        'ui.creategui_P230',
        'ui.creategui_P230_v2',
        'ui.creategui_P140',
        'ui.creategui_P140_v2',
        
        # Utils modules
        'utils.utils',
        'utils.db_config',
        'utils.config_manager',
        'utils.log',
        'utils.date',
        'utils.Checkping',
        'utils.thread_utils',
        
        # Data modules
        'data.calibration',
        'data.cartridge',
        'data.charge',
        'data.final',
        'data.firmware',
        'data.get_mcu_id',
        'data.heater',
        'data.heater_module',
        'data.inductive',
        'data.lcdled',
        'data.leak',
        'data.matching',
        'data.Packing',
        'data.pba',
        'data.puffing',
        'data.sensor',
        'data.sleep',
        'data.smart_mmi',
        'data.snwriting',
        'data.verification',
        'data.weigh',
        
        # Standard library
        'configparser',
        'subprocess',
        'urllib',
        'urllib.request',
        'json',
        'os',
        'sys',
        'threading',
        'queue',
        'datetime',
        'socket',
    ],
    hookspath=['.'],  # Use custom hooks from current directory
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'test',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Check_All_Stage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Resource\\Icon.ico',
)
