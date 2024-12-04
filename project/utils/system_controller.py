import subprocess
import psutil
import platform
import os
import webbrowser
import pyautogui
from typing import Dict, Optional, Tuple

class SystemController:
    # Website mappings
    WEBSITES = {
        'youtube': 'https://www.youtube.com',
        'google': 'https://www.google.com',
        'gmail': 'https://mail.google.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://twitter.com',
        'linkedin': 'https://www.linkedin.com',
        'github': 'https://github.com',
        'amazon': 'https://www.amazon.com',
        'netflix': 'https://www.netflix.com',
        'spotify': 'https://open.spotify.com'
    }

    # Microsoft Office applications
    OFFICE_APPS = {
        'word': 'WINWORD.EXE',
        'excel': 'EXCEL.EXE',
        'powerpoint': 'POWERPNT.EXE',
        'outlook': 'OUTLOOK.EXE',
        'onenote': 'ONENOTE.EXE',
        'teams': 'Teams.exe'
    }

    @staticmethod
    def get_system_info() -> Dict:
        return {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'battery': psutil.sensors_battery().percent if psutil.sensors_battery() else None,
            'temperature': SystemController._get_temperature()
        }

    @staticmethod
    def control_wifi(enable: bool) -> Tuple[bool, str]:
        try:
            if platform.system() == "Windows":
                action = "enable" if enable else "disable"
                subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", action], check=True)
                return True, f"WiFi has been {'enabled' if enable else 'disabled'}"
            else:
                return False, "WiFi control is only supported on Windows"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to control WiFi: {str(e)}"

    @staticmethod
    def control_bluetooth(enable: bool) -> Tuple[bool, str]:
        try:
            if platform.system() == "Windows":
                action = "start" if enable else "stop"
                subprocess.run(["net", action, "bthserv"], check=True)
                return True, f"Bluetooth has been {'enabled' if enable else 'disabled'}"
            else:
                return False, "Bluetooth control is only supported on Windows"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to control Bluetooth: {str(e)}"

    @staticmethod
    def set_brightness(level: int) -> Tuple[bool, str]:
        try:
            if platform.system() == "Windows":
                level = max(0, min(100, level))
                subprocess.run(["powershell", "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1," + str(level) + ")"], check=True)
                return True, f"Brightness set to {level}%"
            else:
                return False, "Brightness control is only supported on Windows"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to set brightness: {str(e)}"

    @staticmethod
    def control_volume(level: Optional[int] = None, mute: Optional[bool] = None) -> Tuple[bool, str]:
        try:
            if platform.system() == "Windows":
                if level is not None:
                    level = max(0, min(100, level))
                    subprocess.run(["powershell", f"Set-AudioDevice -Volume {level}"], check=True)
                    return True, f"Volume set to {level}%"
                elif mute is not None:
                    action = "Mute" if mute else "Unmute"
                    subprocess.run(["powershell", f"Set-AudioDevice -{action}"], check=True)
                    return True, f"Audio {'muted' if mute else 'unmuted'}"
            return False, "Volume control is only supported on Windows"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to control volume: {str(e)}"

    @staticmethod
    def open_website(site_name: str) -> Tuple[bool, str]:
        site_name = site_name.lower()
        if site_name in SystemController.WEBSITES:
            webbrowser.open(SystemController.WEBSITES[site_name])
            return True, f"Opening {site_name}"
        else:
            # Try to open as direct URL if it contains a domain
            if '.' in site_name and ' ' not in site_name:
                url = f"https://{site_name}" if not site_name.startswith('http') else site_name
                webbrowser.open(url)
                return True, f"Opening {url}"
            return False, f"Website {site_name} not recognized"

    @staticmethod
    def open_office_app(app_name: str) -> Tuple[bool, str]:
        app_name = app_name.lower()
        if app_name in SystemController.OFFICE_APPS:
            try:
                program_files = os.environ.get('PROGRAMFILES', 'C:/Program Files')
                office_path = os.path.join(program_files, 'Microsoft Office/root/Office16')
                app_path = os.path.join(office_path, SystemController.OFFICE_APPS[app_name])

                if os.path.exists(app_path):
                    subprocess.Popen([app_path])
                    return True, f"Opening Microsoft {app_name.capitalize()}"
                else:
                    return False, f"Microsoft {app_name.capitalize()} not found"
            except Exception as e:
                return False, f"Failed to open {app_name}: {str(e)}"
        return False, f"Application {app_name} not supported"

    @staticmethod
    def control_cursor(action: str, amount: Optional[int] = None) -> Tuple[bool, str]:
        try:
            if action == "move_up":
                pyautogui.moveRel(0, -amount if amount else -10)
            elif action == "move_down":
                pyautogui.moveRel(0, amount if amount else 10)
            elif action == "move_left":
                pyautogui.moveRel(-amount if amount else -10, 0)
            elif action == "move_right":
                pyautogui.moveRel(amount if amount else 10, 0)
            elif action == "click":
                pyautogui.click()
            elif action == "double_click":
                pyautogui.doubleClick()
            elif action == "right_click":
                pyautogui.rightClick()
            return True, f"Cursor {action} performed"
        except Exception as e:
            return False, f"Failed to control cursor: {str(e)}"

    @staticmethod
    def _get_temperature() -> Optional[float]:
        try:
            if platform.system() == "Windows":
                import wmi
                w = wmi.WMI(namespace=r"root\OpenHardwareMonitor")  # Fixed with raw string
                temperature_infos = w.Sensor()
                for sensor in temperature_infos:
                    if sensor.SensorType == 'Temperature':
                        return sensor.Value
            return None
        except:
            return None
