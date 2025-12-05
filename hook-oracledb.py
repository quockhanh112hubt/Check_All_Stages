"""
PyInstaller hook for oracledb to ensure cryptography is properly included
"""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all oracledb submodules
hiddenimports = collect_submodules('oracledb')

# Also collect cryptography modules (required for thin mode)
hiddenimports += collect_submodules('cryptography')
hiddenimports += [
    'cryptography.hazmat.primitives.ciphers.algorithms',
    'cryptography.hazmat.primitives.ciphers.modes',
    'cryptography.hazmat.backends.openssl',
    '_cffi_backend',
]

# Collect data files if any
datas = collect_data_files('oracledb')
datas += collect_data_files('cryptography')
