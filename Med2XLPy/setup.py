from cx_Freeze import setup, Executable
# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "includes": ["xlsxwriter","cmath"],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
}

build_app_options = {
    "iconfile": "/Users/11nho/Developer/MedPC/Med2XLPy/assets/icon.icns",
    "bundle_name": "Med2XLPy"
}

build_appimage_options = {
    "target_name" : "Med2XLPy.AppImage"
}

setup(
    name="Med2XLPy",
    version="0.1.0",
    description="Convert MedPC Files",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": build_app_options,
        "bdist_appimage": build_appimage_options
    },
    executables=[Executable("GUI.py", base="gui",icon="/Users/11nho/Developer/MedPC/Med2XLPy/Med2XLPy/icon2")],
)