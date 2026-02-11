# OCP IT Helpdesk

## Overview
A Windows Desktop Agent built in Python that captures screenshots and creates IT support tickets via a global hotkey (F8). The app runs silently in the system tray and pops up a modern ticket form when triggered. Tickets are submitted to HappyFox under the logged-in user's identity.

**Target Platform:** Windows (designed for PyInstaller packaging)  
**Development Environment:** Replit (Linux) - GUI runs in console/VNC mode for testing  
**GitHub Repo:** https://github.com/boeseben-del/OCP-IT-Help-Center

## Project Architecture

### Directory Structure
```
main.py                     # Entry point - ITAgentApp class
setup_msi.py                # cx_Freeze MSI build configuration
.github/workflows/
  build-msi.yml             # GitHub Actions workflow for automated MSI/EXE builds
src/
  it_agent/
    __init__.py
    sysinfo.py              # System info: hostname, IP, MAC, CPU, RAM, disk, OS, uptime, battery
    screenshot.py           # Screenshot capture and thumbnail utilities
    gui.py                  # CustomTkinter ticket form UI (TicketWindow)
    tray.py                 # System tray icon and F8 hotkey listener (TrayManager)
    api.py                  # HappyFox API integration (reads creds from env vars)
```

### Key Libraries
- **customtkinter** - Modern themed Tkinter GUI (DarkBlue theme)
- **pystray** - System tray icon management
- **keyboard** - Global hotkey listener (F8)
- **pyautogui / PIL** - Screenshot capture
- **requests** - HTTP API calls to HappyFox
- **psutil** - CPU/RAM/disk usage, uptime, battery monitoring
- **cx_Freeze** - MSI installer generation (build only)

### System Info Gathered
- Hostname, Local IP, Public IP, MAC Address
- CPU Usage %, RAM Usage % (+ Total RAM), Disk Usage %
- Logical Processor Count
- System Uptime (days/hours/minutes)
- Battery Status (percent + charging/on battery)
- OS (correctly detects Windows 11 via build number)
- Active Window Title, Current Username, User Email

### Flow
1. App starts silently -> minimizes to system tray
2. User presses F8 -> screenshot captured immediately -> ticket form opens
3. Form auto-fills system info (including uptime), shows screenshot thumbnail
4. User fills description, sets priority, submits
5. Ticket sent to HappyFox API under the logged-in user's identity

### API Configuration
- HappyFox credentials stored as Replit secrets: HAPPYFOX_API_KEY, HAPPYFOX_AUTH_CODE
- api.py reads credentials from environment variables at runtime
- HAPPYFOX_ENDPOINT env var can override the default endpoint URL
- Tickets are created with the logged-in user's name and email

### Building for Windows
MSI Installer (cx_Freeze):
```
python setup_msi.py bdist_msi
```

Standalone EXE (PyInstaller):
```
pyinstaller --noconsole --onefile --name "OCP_IT_Helpdesk" main.py
```

### GitHub Actions Build
The `.github/workflows/build-msi.yml` workflow automatically builds both MSI and EXE on push to main. Artifacts are downloadable from the Actions tab.

## Recent Changes
- 2026-02-11: Initial project creation with full architecture
- 2026-02-11: Secured HappyFox API credentials as environment variables
- 2026-02-11: Pushed code to GitHub repo, created MSI build workflow
- 2026-02-11: Added MAC address and disk usage to system info
- 2026-02-11: Fixed Windows 11 detection (build number check)
- 2026-02-11: Rebranded to "OCP IT Helpdesk"
- 2026-02-11: Submit button moved to bottom right, made more prominent
- 2026-02-11: Tickets now created under the logged-in user's identity
- 2026-02-11: Added system uptime, battery status, total RAM, logical processor count

## User Preferences
- Modern dark theme UI (DarkBlue)
- Professional, clean layout
- Windows-focused deployment
- GitHub-based CI/CD for MSI compilation
- Branding: OCP IT Helpdesk
