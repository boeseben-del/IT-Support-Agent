"""
cx_Freeze setup script for building a Windows MSI installer.

Usage (on Windows):
    python setup_msi.py bdist_msi

This will create an MSI installer in the dist/ folder.
Builds two executables:
  - OCP_IT_Helpdesk.exe        (tray app, Win32GUI)
  - OCP_IT_Helpdesk_Service.exe (Windows Service, Win32Service)
"""

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "customtkinter",
        "pystray",
        "keyboard",
        "pyautogui",
        "PIL",
        "requests",
        "psutil",
        "tkinter",
        "io",
        "threading",
        "socket",
        "platform",
        "ctypes",
        "json",
        "win32serviceutil",
        "win32service",
        "win32event",
        "win32ts",
        "win32security",
        "win32process",
        "win32profile",
        "win32con",
        "win32api",
        "pywintypes",
        "servicemanager",
        "logging",
        "logging.handlers",
    ],
    "includes": [
        "src.it_agent",
        "src.it_agent.sysinfo",
        "src.it_agent.screenshot",
        "src.it_agent.gui",
        "src.it_agent.tray",
        "src.it_agent.api",
        "src.it_agent.service",
    ],
    "include_files": [
        ("assets", "assets"),
        ("service_manager.py", "service_manager.py"),
    ],
    "excludes": ["test", "unittest"],
}

bdist_msi_options = {
    "upgrade_code": "{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\OCP_IT_Helpdesk",
}

base_gui = None
base_svc = None
if sys.platform == "win32":
    base_gui = "Win32GUI"
    base_svc = "Win32Service"

executables = [
    Executable(
        "main.py",
        base=base_gui,
        target_name="OCP_IT_Helpdesk.exe",
        shortcut_name="OCP IT Helpdesk",
        shortcut_dir="DesktopFolder",
        icon="assets/ocp_icon.ico",
    ),
    Executable(
        "src/it_agent/service.py",
        base=base_svc,
        target_name="OCP_IT_Helpdesk_Service.exe",
        icon="assets/ocp_icon.ico",
    ),
]

setup(
    name="OCP IT Helpdesk",
    version="1.1.0",
    description="OCP IT Helpdesk - Background desktop tool for capturing screenshots and IT tickets",
    author="OCP IT",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
