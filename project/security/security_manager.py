import subprocess
from typing import Optional
import os
from config import ANTIVIRUS_PATH

class SecurityManager:
    @staticmethod
    def run_antivirus_scan() -> tuple[bool, Optional[str]]:
        
        try:
            if os.path.exists(ANTIVIRUS_PATH):
                subprocess.run([ANTIVIRUS_PATH, "/scannow"], check=True)
                return True, "Antivirus scan started successfully."
            else:
                return False, "Antivirus software not found."
        except subprocess.CalledProcessError as e:
            return False, f"Error running antivirus scan: {e}"

    @staticmethod
    def check_system_security() -> dict:
        
        security_status = {
            'firewall_active': SecurityManager._check_firewall(),
            'antivirus_running': SecurityManager._check_antivirus(),
            'updates_pending': SecurityManager._check_updates()
        }
        return security_status

    @staticmethod
    def _check_firewall() -> bool:
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"], 
                capture_output=True, 
                text=True
            )
            return "ON" in result.stdout
        except:
            return False

    @staticmethod
    def _check_antivirus() -> bool:
        try:
            return os.path.exists(ANTIVIRUS_PATH)
        except:
            return False

    @staticmethod
    def _check_updates() -> bool:
        try:
            result = subprocess.run(
                ["wmic", "qfe", "list", "brief"], 
                capture_output=True, 
                text=True
            )
            return "KB" in result.stdout
        except:
            return False
