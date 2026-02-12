# OCP IT Helpdesk

## Overview
A Windows Desktop Agent built in Python that captures screenshots and creates IT support tickets via a global hotkey (F8). The app runs as a **Windows Service** that auto-starts on boot and launches a tray application in the logged-in user's desktop session. Tickets are submitted to HappyFox under the logged-in user's identity.

**Target Platform:** Windows (designed for PyInstaller packaging + Windows Service)  
**Development Environment:** Replit (Linux) - GUI runs in console/VNC mode for testing  
**GitHub Repo:** https://github.com/boeseben-del/OCP-IT-Helpdesk

## Project Architecture

### Directory Structure
```
main.py                     # Entry point - ITAgentApp class (tray app)
service_manager.py           # CLI helper to install/uninstall/start/stop the service
setup_msi.py                # cx_Freeze MSI build config (builds both tray + service EXEs)
.github/workflows/
  build-msi.yml             # GitHub Actions: builds MSI, tray EXE, and service EXE
src/
  it_agent/
    __init__.py
    service.py              # Windows Service (OCPITHelpdesk) - launches tray app in user session
    sysinfo.py              # System info: hostname, IP, MAC, CPU, RAM, disk, OS, uptime, battery
    screenshot.py           # Screenshot capture and thumbnail utilities
    gui.py                  # CustomTkinter ticket form UI (TicketWindow) with OCP branding
    tray.py                 # System tray icon and F8 hotkey listener (TrayManager)
    api.py                  # HappyFox API integration (reads creds from env vars)
assets/
  ocp_logo.png              # OCP company logo (GUI header)
  ocp_tray.png              # System tray icon
  ocp_icon.ico              # Windows icon (EXE, window, installer)
```

### Service Architecture
The app uses a two-part design for reliability:

1. **Windows Service** (`OCP_IT_Helpdesk_Service.exe`) - Runs as LocalSystem, auto-starts on boot
   - Monitors the active user session
   - Launches the tray app via CreateProcessAsUser in the user's desktop session
   - Restarts the tray app automatically if it crashes
   - Manageable via services.msc, sc.exe, or PDQ Connect
   - Logs to `C:\ProgramData\OCP_IT_Helpdesk\service.log`

2. **Tray App** (`OCP_IT_Helpdesk.exe`) - The user-facing GUI
   - System tray icon with F8 hotkey
   - Ticket form with screenshot and system info
   - Launched by the service, not directly by the user

### Service Management
```
service_manager.py install    # Install service (auto-start, auto-restart on failure)
service_manager.py uninstall  # Remove the service
service_manager.py start      # Start the service
service_manager.py stop       # Stop the service
service_manager.py restart    # Restart the service
service_manager.py status     # Check service status
```
All commands require Administrator privileges.

### Key Libraries
- **customtkinter** - Modern themed Tkinter GUI with OCP brand colors
- **pystray** - System tray icon management
- **keyboard** - Global hotkey listener (F8)
- **pyautogui / PIL** - Screenshot capture
- **requests** - HTTP API calls to HappyFox
- **psutil** - CPU/RAM/disk usage, uptime, battery monitoring
- **pywin32** - Windows Service (win32serviceutil, CreateProcessAsUser)
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
1. Windows Service starts on boot -> waits for user login
2. Service launches tray app in user's desktop session
3. User presses F8 -> screenshot captured immediately -> ticket form opens
4. Form auto-fills system info (including uptime), shows screenshot thumbnail
5. User fills description, sets priority, submits
6. Ticket sent to HappyFox API under the logged-in user's identity
7. If tray app crashes, service automatically restarts it

### API Configuration
- HappyFox credentials stored as Replit secrets: HAPPYFOX_API_KEY, HAPPYFOX_AUTH_CODE
- api.py reads credentials from environment variables at runtime
- HAPPYFOX_ENDPOINT env var can override the default endpoint URL
- Tickets are created with the logged-in user's name and email

### Building for Windows
MSI Installer (cx_Freeze - includes both tray app + service):
```
python setup_msi.py bdist_msi
```

Standalone EXEs (PyInstaller):
```
pyinstaller --noconsole --onefile --name "OCP_IT_Helpdesk" --icon "assets/ocp_icon.ico" --add-data "assets;assets" main.py
pyinstaller --onefile --name "OCP_IT_Helpdesk_Service" --icon "assets/ocp_icon.ico" --hidden-import win32timezone src/it_agent/service.py
```

### GitHub Actions Build
The `.github/workflows/build-msi.yml` workflow automatically builds MSI, tray EXE, and service EXE on push to main. Artifacts downloadable from the Actions tab:
- `OCP_IT_Helpdesk_MSI` - MSI installer (includes both executables)
- `OCP_IT_Helpdesk_EXE` - Standalone tray app
- `OCP_IT_Helpdesk_Service_EXE` - Standalone service
- `OCP_IT_Helpdesk_Complete` - All files bundled together

### Deployment with PDQ Connect
1. Download `OCP_IT_Helpdesk_Complete` from GitHub Actions
2. Deploy `OCP_IT_Helpdesk.exe` and `OCP_IT_Helpdesk_Service.exe` to target machines
3. Run `OCP_IT_Helpdesk_Service.exe install` (as admin) to register the service
4. Run `sc start OCPITHelpdesk` or use services.msc to start
5. To restart remotely: `sc stop OCPITHelpdesk && sc start OCPITHelpdesk`

## Recent Changes
- 2026-02-11: Initial project creation with full architecture
- 2026-02-11: Secured HappyFox API credentials as environment variables
- 2026-02-11: Pushed code to GitHub repo, created MSI build workflow
- 2026-02-11: Added MAC address and disk usage to system info
- 2026-02-11: Fixed Windows 11 detection (build number check)
- 2026-02-11: Rebranded to "OCP IT Helpdesk" with company logo
- 2026-02-11: Submit button moved to bottom right, made more prominent
- 2026-02-11: Tickets now created under the logged-in user's identity
- 2026-02-11: Added system uptime, battery status, total RAM, logical processor count
- 2026-02-12: Added OCP brand colors (navy, blue, cyan, silver) and logo throughout GUI
- 2026-02-12: Fixed asset path resolution for PyInstaller and cx_Freeze builds
- 2026-02-12: **Pivoted to Windows Service architecture** for reliability and remote management
- 2026-02-12: Created service.py (Windows Service using pywin32/CreateProcessAsUser)
- 2026-02-12: Created service_manager.py (install/uninstall/start/stop helper)
- 2026-02-12: Updated build pipeline to produce service EXE alongside tray app
- 2026-02-12: Added PDQ Connect deployment documentation

## User Preferences
- Modern dark theme UI with OCP brand colors (navy #002E56, blue #478FCC, cyan #5FC8EB, silver #A6A8AB)
- Professional, clean layout
- Windows-focused deployment as a Windows Service
- GitHub-based CI/CD for MSI/EXE compilation
- Remote management via PDQ Connect
- Branding: OCP IT Helpdesk
