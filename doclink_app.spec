# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=(
        __import__('PyInstaller.utils.hooks', fromlist=['collect_data_files']).collect_data_files('docling', include_py_files=False)
        + __import__('PyInstaller.utils.hooks', fromlist=['collect_data_files']).collect_data_files('docling_parse', include_py_files=False)
        # Include distribution metadata so entry-points work in frozen app
        + __import__('PyInstaller.utils.hooks', fromlist=['copy_metadata']).copy_metadata('docling')
        + __import__('PyInstaller.utils.hooks', fromlist=['copy_metadata']).copy_metadata('docling-parse')
        + __import__('PyInstaller.utils.hooks', fromlist=['copy_metadata']).copy_metadata('easyocr')
    ),
    hiddenimports=(
        [
            'flask',
            'flask_cors',
            'docling',
            'docling.document_converter',
            'werkzeug',
            'transformers',
            'easyocr',
            'scikit-image',
            'tokenizers',
        ]
        + __import__('PyInstaller.utils.hooks', fromlist=['collect_submodules']).collect_submodules('docling')
        + __import__('PyInstaller.utils.hooks', fromlist=['collect_submodules']).collect_submodules('docling_parse')
        + __import__('PyInstaller.utils.hooks', fromlist=['collect_submodules']).collect_submodules('easyocr')
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add any additional data files needed
a.datas += [
    ('README.md', 'README.md', 'DATA'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='doclink_converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='doclink_converter',
)
