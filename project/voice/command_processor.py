from typing import Dict, Any, Tuple
import re
from utils.system_controller import SystemController
import openai

class CommandProcessor:
    def __init__(self):
        self.system_controller = SystemController()
        self.command_patterns = {
            'system_info': r'(system|computer|laptop) (status|info|information)',
            'wifi': r'(enable|disable|turn on|turn off) (wifi|wi-fi)',
            'bluetooth': r'(enable|disable|turn on|turn off) bluetooth',
            'brightness': r'(set |change |adjust )?brightness( level)? (to )?(\d+)( percent)?',
            'volume': r'(set |change |adjust )?(volume|sound)( level)? (to )?(\d+)( percent)?',
            'mute': r'(mute|unmute)( sound| volume)?',
            'website': r'(open|go to|visit) (?:the )?([\w\s.]+?)(?:\s+website)?$',
            'office': r'(open|launch|start) (?:microsoft )?(word|excel|powerpoint|outlook|onenote|teams)',
            'cursor': r'(move cursor|click|right click|double click)(?: (up|down|left|right))?(?: (\d+))?'
        }

    def process_command(self, command: str) -> Tuple[bool, str]:
        
        command = command.lower()

        # System information
        if re.search(self.command_patterns['system_info'], command):
            info = self.system_controller.get_system_info()
            return True, self._format_system_info(info)

        # WiFi control
        wifi_match = re.search(self.command_patterns['wifi'], command)
        if wifi_match:
            enable = any(action in wifi_match.group(1) for action in ['enable', 'turn on'])
            return self.system_controller.control_wifi(enable)

        # Bluetooth control
        bluetooth_match = re.search(self.command_patterns['bluetooth'], command)
        if bluetooth_match:
            enable = any(action in bluetooth_match.group(1) for action in ['enable', 'turn on'])
            return self.system_controller.control_bluetooth(enable)

        # Brightness control
        brightness_match = re.search(self.command_patterns['brightness'], command)
        if brightness_match:
            level = int(brightness_match.group(4))
            return self.system_controller.set_brightness(level)

        # Volume control
        volume_match = re.search(self.command_patterns['volume'], command)
        if volume_match:
            level = int(volume_match.group(5))
            return self.system_controller.control_volume(level=level)

        # Mute control
        mute_match = re.search(self.command_patterns['mute'], command)
        if mute_match:
            mute = mute_match.group(1) == 'mute'
            return self.system_controller.control_volume(mute=mute)

        # Website opening
        website_match = re.search(self.command_patterns['website'], command)
        if website_match:
            site_name = website_match.group(2).strip()
            return self.system_controller.open_website(site_name)

        # Microsoft Office apps
        office_match = re.search(self.command_patterns['office'], command)
        if office_match:
            app_name = office_match.group(2).strip()
            return self.system_controller.open_office_app(app_name)

        # Cursor control
        cursor_match = re.search(self.command_patterns['cursor'], command)
        if cursor_match:
            action = cursor_match.group(1)
            direction = cursor_match.group(2) if cursor_match.group(2) else None
            amount = int(cursor_match.group(3)) if cursor_match.group(3) else None
            
            if "click" in action:
                return self.system_controller.control_cursor(action.replace(" ", "_"))
            elif direction:
                return self.system_controller.control_cursor(f"move_{direction}", amount)

        # If no system command matched, use ChatGPT for general conversation
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are REVA, a helpful desktop assistant."},
                    {"role": "user", "content": command}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return True, response.choices[0].message.content
        except Exception as e:
            return False, f"Sorry, I couldn't process that request: {str(e)}"

    def _format_system_info(self, info: Dict[str, Any]) -> str:
        
        response = "Here's your system status: "
        response += f"CPU usage is {info['cpu_usage']}%, "
        response += f"Memory usage is {info['memory_usage']}%, "
        response += f"Disk usage is {info['disk_usage']}%"
        
        if info['battery']:
            response += f", Battery level is {info['battery']}%"
        if info['temperature']:
            response += f", CPU temperature is {info['temperature']}°C"
            
        return response
