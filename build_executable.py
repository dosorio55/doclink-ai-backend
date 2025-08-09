#!/usr/bin/env python3
import os
import platform
import subprocess
import shutil

def build_executable():
    """Build the executable for the current platform"""
    print("Building DocLink AI Converter executable...")
    
    # Create a directory for pre-downloaded models if it doesn't exist
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docling_cache')
    os.makedirs(models_dir, exist_ok=True)
    
    # Run PyInstaller
    cmd = [
        'pyinstaller',
        '--clean',
        'doclink_app.spec'
    ]
    
    subprocess.run(cmd, check=True)
    
    print("\nBuild completed successfully!")
    print(f"Executable can be found in: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'doclink_converter')}")
    print("\nNotes:")
    print("1. The first run may still download some models if they weren't cached during build")
    print("2. Make sure to distribute the entire 'doclink_converter' directory, not just the executable")
    print("3. The application will create 'uploads', 'processed', and 'docling_cache' folders next to the executable")

if __name__ == "__main__":
    build_executable()
