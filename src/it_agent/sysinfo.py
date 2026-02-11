"""System information gathering utilities."""

import socket
import platform
import os
import psutil
import requests as req_lib


def get_hostname():
    return socket.gethostname()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "N/A"


def get_public_ip():
    try:
        response = req_lib.get("https://api.ipify.org", timeout=3)
        return response.text
    except Exception:
        return "N/A"


def get_current_user():
    try:
        return os.getlogin()
    except Exception:
        return os.environ.get("USERNAME", os.environ.get("USER", "Unknown"))


def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)


def get_ram_usage():
    return psutil.virtual_memory().percent


def get_os_info():
    return f"{platform.system()} {platform.release()}"


def get_active_window_title():
    """Get the title of the currently active window (Windows-specific)."""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value if buf.value else "Unknown"
    except Exception:
        try:
            import subprocess
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True, text=True, timeout=2
            )
            return result.stdout.strip() if result.stdout.strip() else "Unknown"
        except Exception:
            return "Unknown"


def gather_all():
    """Gather all system information into a dictionary."""
    return {
        "hostname": get_hostname(),
        "local_ip": get_local_ip(),
        "public_ip": get_public_ip(),
        "username": get_current_user(),
        "cpu_usage": get_cpu_usage(),
        "ram_usage": get_ram_usage(),
        "os_info": get_os_info(),
        "active_window": get_active_window_title(),
    }
